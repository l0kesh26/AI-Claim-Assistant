import streamlit as st
import pandas as pd
import tempfile
import os
import re
import json
import requests
import unicodedata
from paddleocr import PaddleOCR

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


# CONFIG

st.set_page_config(page_title="Insurance AI System", layout="centered")

USER_DB = {"admin": "123", "harsha": "password123"}
SENDER_A = "ramtgemini@gmail.com"
SENDER_B = "rameshapk24@gmail.com"


# LOAD CSV

@st.cache_data
def load_policies():
    df = pd.read_csv("test.csv")
    df.columns = df.columns.str.strip()
    return df

policy_df = load_policies()


# OCR INIT

@st.cache_resource
def load_ocr():
    return PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, enable_mkldnn=False)

ocr = load_ocr()


# OCR FUNCTION

def get_ocr_text(image_path):
    result = ocr.ocr(image_path, cls=True)
    texts = []
    for line in result:
        for word in line:
            texts.append(word[1][0])
    return " ".join(texts)


# LLM CALL

def call_model(prompt, primary="mistral", fallback="phi3"):
    url = "http://localhost:11434/api/generate"

    payload = {"model": primary, "prompt": prompt, "stream": False, "temperature": 0}

    try:
        res = requests.post(url, json=payload, timeout=120)
        if res.status_code == 200:
            return res.json().get("response", "")
    except:
        pass

    try:
        payload["model"] = fallback
        res = requests.post(url, json=payload, timeout=120)
        if res.status_code == 200:
            return res.json().get("response", "")
    except:
        pass

    return ""


# SAFE JSON

def safe_parse(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    return {
        "patient_name": "",
        "doctor_name": "",
        "doctor_valid": False,
        "hospital_name": "",
        "total_claim_amount": 0,
        "date": "",
        "medicines": ""
    }


# LLM EXTRACTION

def run_llm(text):
    text = text[:3000]

    prompt = f"""
Extract insurance claim data.

Return ONLY JSON:
{{
"patient_name":"",
"doctor_name":"",
"doctor_valid":true,
"hospital_name":"",
"total_claim_amount":0,
"date":"",
"medicines":""
}}

OCR:
{text}
"""

    output = call_model(prompt)
    st.text_area("🧠 LLM OUTPUT", output, height=150)

    if not output:
        return safe_parse("")

    return safe_parse(output)


# Name Matching Function

def normalize_name(name):
    name = unicodedata.normalize("NFKD", str(name)).lower()
    name = re.sub(r'\b(mr|ms|mrs|dr)\b', '', name)
    name = re.sub(r'[^a-z\s]', ' ', name)
    return " ".join(name.split())

def is_name_match(a, b):
    a, b = normalize_name(a), normalize_name(b)
    return a == b or a in b or b in a


# CLAIM_CALCULATION

def calculate_claim(data, policy_data):
    score = 0

    if data.get("patient_name"):
        score += 20
    if data.get("doctor_name"):
        score += 20
    if data.get("doctor_valid"):
        score += 20
    if data.get("hospital_name"):
        score += 20

    total = float(data.get("total_claim_amount", 0))
    claim_type = str(policy_data.get("Claim Type", "")).strip().lower()

    valid_types = ["basic", "premium", "ultra"]

    if claim_type not in valid_types:
        return {"score": score, "insurance_amount": 0, "claim_type": "invalid"}

    multiplier = {"basic": 0.6, "premium": 0.8, "ultra": 1.0}[claim_type]
    amount = total * multiplier

    return {
        "score": score,
        "insurance_amount": round(amount, 2),
        "claim_type": claim_type
    }


# PDF_part

def generate_pdf(policy_data, data, result):
    file = "report.pdf"
    doc = SimpleDocTemplate(file, pagesize=A4)
    styles = getSampleStyleSheet()

    holder = policy_data.get("Name", "N/A")
    policy_number = policy_data.get("Policy Number", "N/A")
    claim_type = policy_data.get("Claim Type", "N/A")

    patient = data.get("patient_name", "N/A")
    hospital = data.get("hospital_name", "N/A")
    doctor = data.get("doctor_name", "N/A")
    date = data.get("date", "Not Available")
    medicines = data.get("medicines", "Not Available")

    content = []

    content.append(Paragraph("Insurance Claim Report", styles["Title"]))
    content.append(Spacer(1, 15))

    content.append(Paragraph("Policy Details", styles["Heading2"]))
    content.append(Paragraph(f"Name: {holder}", styles["Normal"]))
    content.append(Paragraph(f"Policy Number: {policy_number}", styles["Normal"]))
    content.append(Paragraph(f"Claim Type: {claim_type}", styles["Normal"]))
    content.append(Spacer(1, 15))

    content.append(Paragraph("Claim Details", styles["Heading2"]))

    if normalize_name(patient) != normalize_name(holder):
        content.append(Paragraph(f"Patient Name: {patient}", styles["Normal"]))

    content.append(Paragraph(f"Hospital Name: {hospital}", styles["Normal"]))
    content.append(Paragraph(f"Doctor Name: {doctor}", styles["Normal"]))
    content.append(Paragraph(f"Date: {date}", styles["Normal"]))
    content.append(Paragraph(f"Medicines: {medicines}", styles["Normal"]))
    content.append(Spacer(1, 15))

    content.append(Paragraph("Final Decision", styles["Heading2"]))
    content.append(Paragraph(f"Claim Score: {result['score']}", styles["Normal"]))
    content.append(Paragraph(f"Claim Amount: ₹{result['insurance_amount']}", styles["Normal"]))

    doc.build(content)
    return file


# EMAIL

def send_email(to, subject, body, file=None):
    sender = "venkatalokeshwar@gmail.com"
    password = " "  # 🔴 Add app password

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body))

    if file:
        with open(file, "rb") as f:
            part = MIMEApplication(f.read())
            part.add_header("Content-Disposition", "attachment", filename="report.pdf")
            msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()


# SESSION

if "page" not in st.session_state:
    st.session_state.page = "login"

# LOGIN

if st.session_state.page == "login":
    st.title("Login")

    u = st.text_input("User")
    p = st.text_input("Pass", type="password")

    if st.button("Login"):
        if u in USER_DB and USER_DB[u] == p:
            st.session_state.page = "policy"
            st.rerun()
        else:
            st.error("Invalid")


# POLICY

elif st.session_state.page == "policy":
    policy = st.text_input("Policy Number")

    if st.button("Verify"):
        df = policy_df[policy_df["Policy Number"].astype(str) == policy]

        if not df.empty:
            st.session_state.policy_data = df.iloc[0]
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Not found")


# DASHBOARD

elif st.session_state.page == "dashboard":
    st.title("Dashboard")

    holder = st.session_state.policy_data["Name"]
    claim_type = st.session_state.policy_data.get("Claim Type")

    st.write("Holder:", holder)
    st.write("Policy Type:", claim_type)

    file = st.file_uploader("Upload Bill")

    if file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            path = tmp.name

        text = get_ocr_text(path)
        os.remove(path)

        st.text_area("📄 OCR TEXT", text, height=200)

        data = run_llm(text)
        st.json(data)

        if st.button("Validate"):
            if is_name_match(data["patient_name"], holder):
                st.session_state.claim_data = data
                st.session_state.page = "claim"
                st.rerun()
            else:
                st.error("Name mismatch")

# CLAIM

elif st.session_state.page == "claim":
    st.title("Result")

    res = calculate_claim(
        st.session_state.claim_data,
        st.session_state.policy_data
    )

    if res["claim_type"] == "invalid":
        st.error("❌ User does not belong to any valid claim type")
        st.stop()

    st.subheader("Policy Type")
    st.success(res["claim_type"].upper())

    st.metric("Score", res["score"])
    st.metric("Amount", res["insurance_amount"])

    if st.button("Process"):
        pdf = generate_pdf(
            st.session_state.policy_data,
            st.session_state.claim_data,
            res
        )

        if res["score"] >= 80:
            send_email(SENDER_A, "Medical Insurance Report ", "This is summarized report of medical insurance report ", pdf)
            send_email(SENDER_B, "Update on Medical Insurance ", "The claim as successfully started ", None)
            st.success("Approved flow")
        else:
            send_email(SENDER_B, "Update on Medical Insurance ", "The claim as failed please re-submit your claim.", None)
            st.error("Rejected flow")

    if st.button("Back"):
        st.session_state.page = "dashboard"
        st.rerun()