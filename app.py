import streamlit as st
import openai
import json
import os
from docx import Document
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load prompt templates
with open("prompts/summary_template.txt", "r") as f:
    summary_template = f.read()

with open("prompts/qa_template.txt", "r") as f:
    qa_template = f.read()

def generate_completion(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        text = ""
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

# Streamlit UI
st.title("📚 StudyMate GPT")
st.markdown("Upload a study document or paste your content below. The assistant will generate a summary and a few questions to help you understand it better.")

uploaded_file = st.file_uploader("📂 Upload a document (TXT, PDF, DOCX)", type=["txt", "pdf", "docx"])
user_input = st.text_area("✍️ Or paste your study content:", height=200)

# Determine source of content
content = ""
if uploaded_file:
    content = extract_text_from_file(uploaded_file)
    if len(content.split()) > 1000:
        st.warning("This document is long. Only the first 1000 words are used for analysis.")
    content = " ".join(content.split()[:1000])  # Limit to 1000 words
elif user_input:
    content = user_input

if st.button("Generate Summary & Q&A") and content:
    with st.spinner("Thinking..."):
        summary_prompt = summary_template.replace("{text}", content)
        qa_prompt = qa_template.replace("{text}", content)

        summary = generate_completion(summary_prompt)
        qa = generate_completion(qa_prompt)

        result = {
            "input": content,
            "summary": summary,
            "qa": qa
        }

        # Append to log file safely
        log_file_path = "logs/session_log.json"
        try:
            with open(log_file_path, "r") as log_file:
                existing_data = json.load(log_file)
                if isinstance(existing_data, dict):
                    log_data = [existing_data]
                elif isinstance(existing_data, list):
                    log_data = existing_data
                else:
                    log_data = []
        except (FileNotFoundError, json.JSONDecodeError):
            log_data = []

        log_data.append(result)

        with open(log_file_path, "w") as log_file:
            json.dump(log_data, log_file, indent=2)

        st.subheader("📝 Summary")
        st.write(summary)

        st.subheader("❓ Q&A")
        for line in qa.split("\n"):
            if line.strip().startswith("Q:"):
                st.markdown(f"**{line}**")
            else:
                st.write(line)

        st.success("Done! Response saved to logs/session_log.json")
