# 📚 StudyMate Mini (Prompt Engineering Demo)

StudyMate Mini is a Streamlit-based web app that uses OpenAI GPT-3.5 to analyze study content or documents. It generates a concise summary and a short Q&A section to help users understand the material better.

## 🔧 Features
- Upload and analyze TXT, PDF, or DOCX files
- Paste custom study content directly
- GPT-3.5 powered summaries and Q&A generation
- Session logging with summaries and questions
- Word limit enforcement for GPT-3.5 context safety

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key
In your environment variables or in `.env`:
```bash
export OPENAI_API_KEY=sk-your-api-key
```

### 3. Run the App
```bash
streamlit run app.py
```

## 📂 File Structure
- `app.py`: Main Streamlit application
- `prompts/`: Prompt templates
- `logs/`: JSON file logging all session data
- `requirements.txt`: Dependency list
- `.gitignore`: Files/folders to exclude from Git

## 🧠 Prompt Engineering
Two custom templates are used:
- Summary
- Question & Answer

These are injected dynamically with your input.

- ✅ **Mini Demo (prompt-based)**  
- 🚀 **Full Flagship (multi-component StudyMate GPT)**

---

Built with 💡 by Rehan Shafi.
