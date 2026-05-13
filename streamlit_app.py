import streamlit as st
import tempfile
import os

from ocr_module import get_ocr_text
from llm import run_llm, is_name_match, calculate_claim, generate_pdf
from email_service import send_email

from config import USER_DB, SENDER_A, SENDER_B, policy_df


# login part
def login_page():
    st.title("Login")

    u = st.text_input("User")
    p = st.text_input("Pass", type="password")

    if st.button("Login"):
        if u in USER_DB and USER_DB[u] == p:
            st.session_state.page = "policy"
            st.rerun()
        else:
            st.error("Invalid")


# policy part
def policy_page():
    policy = st.text_input("Policy Number")

    if st.button("Verify"):
        df = policy_df[policy_df["Policy Number"].astype(str) == policy]

        if not df.empty:
            st.session_state.policy_data = df.iloc[0]
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Not found")


#dashborad part
def dashboard_page():
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


#claim_function
def claim_page():
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