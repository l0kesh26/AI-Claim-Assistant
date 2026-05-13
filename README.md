# AI Claim Assistant

## Overview
AI Claim Assistant is an AI-powered insurance claim verification system designed to reduce manual effort and speed up claim processing.  
The system uses OCR, AI models, and document analysis to verify insurance claims and generate intelligent summaries.

Traditional insurance claim processing can take several days because documents are manually verified.  
This project automates the process using Artificial Intelligence and Local LLMs.

---

# Problem Statement

1. Insurance companies take more time to verify and process claims.
2. Manual verification increases workload and delays approval.
3. Traditional claim processing usually takes around 7–15 days.
4. Detecting fraudulent or incomplete claims manually is difficult.
5. Large document handling consumes significant time.

---

# Solution

AI Claim Assistant automates insurance claim verification using:
- OCR for extracting text from documents
- Local LLMs using Ollama
- AI-based summarization
- Intelligent document analysis
- Faster claim verification workflow

The system analyzes uploaded claim documents and provides:
- Claim summary
- Important extracted information
- Verification support
- Faster processing assistance

---

# Features

- Upload insurance claim documents
- OCR-based text extraction
- AI-powered claim summarization
- Local LLM integration using Ollama
- Faster document verification
- Fraud detection support
- Automated workflow assistance
- User-friendly interface

---

# Technologies Used

## Frontend
- Streamlit

## Backend
- Python

## AI/ML
- Ollama
- LLaVA Model
- NLP

## OCR
- EasyOCR

## Libraries
- Pandas
- NumPy
- PyPDF2
- Pillow
- Requests

---

# Project Workflow

1. User uploads insurance documents
2. OCR extracts text from scanned files/images
3. Extracted content is sent to Ollama LLM
4. AI model analyzes the claim
5. System generates summary and verification response
6. Output is displayed to the user

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/AI-Claim-Assistant.git
cd AI-Claim-Assistant
