# 📄 GenAI Document Assistant

A smart, document-aware assistant that uses **Google Gemini** to:

- Read PDF or TXT files  
- Generate contextual summaries  
- Answer free-form questions  
- Pose logic-based challenge questions  
- Evaluate answers with justification from the document  

Built with 🧠 Google Gemini + 💻 Streamlit.

---

## 🚀 Features

- ✅ Upload PDF/TXT documents  
- ✅ Auto-generates a concise summary  
- ✅ "Ask Anything" mode (free-form QA)  
- ✅ "Challenge Me" mode: generates 3 contextual questions  
- ✅ Evaluates user responses with feedback grounded in the document  
- ✅ No OpenAI dependency (100% Gemini-powered)

---

## 🧰 Setup Instructions

1. **Clone this repository**
```bash
git clone https://github.com/yourusername/genai-doc-assistant.git
cd genai-doc-assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Add your Gemini API key**

Create a `.env` file or replace this line in `app.py`:

```python
genai.configure(api_key="YOUR_GEMINI_API_KEY")
```

> 🔐 You can get a Gemini API key from [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

4. **Run the Streamlit app**

```bash
streamlit run app.py
```

---

## 🧠 Architecture & Reasoning Flow

### 📦 1. Document Upload
- PDF or TXT uploaded via `streamlit.file_uploader`
- Saved to `uploaded_docs/`
- Text extracted using PyMuPDF (for PDF) or simple `.read()` (for TXT)

### 🧠 2. Summary
- First ~2000 characters sent to a summarization model (`facebook/bart-large-cnn`)  
- Summary is shown immediately

### 💬 3. Ask Anything (QA Mode)
- User asks free-form question
- Gemini is prompted with:
  ```
  Document: <text>
  Question: <user input>
  Answer based only on document.
  ```
- Gemini responds with contextually grounded answer

### 🎯 4. Challenge Me (Logic Questions)
- Gemini is asked to generate exactly 3 logical questions:
  ```
  Generate 3 logic-based questions based on the document. Number them.
  ```
- Streamlit form collects user's answers

### ✅ 5. Feedback & Evaluation
- Each answer is sent with:
  ```
  Document: <text>
  Question: <q>
  User Answer: <a>
  Evaluate: Is it correct? Justify based only on the document.
  ```
- Gemini returns correctness + justification

---

## 📁 Project Structure

```
.
├── app.py                     # Main Streamlit app
├── requirements.txt
├── README.md
└── backend/
    ├── utils.py              # PDF/TXT handling
    ├── summarizer.py         # HuggingFace summarizer
    └── qa_engine.py          # Gemini question generation + evaluation
```

---

## 📸 Screenshot

![alt text](https://github.com/Dyno098/GenAI-Document-Assistant/blob/master/Screenshot%202025-06-21%20170809.png)
![alt text](https://github.com/Dyno098/GenAI-Document-Assistant/blob/master/Screenshot%202025-06-21%20101755.png)
![alt text](https://github.com/Dyno098/GenAI-Document-Assistant/blob/master/Screenshot%202025-06-21%20101822.png)

---

## 📌 Notes

- Make sure your Gemini key has access to `gemini-1.5-flash`
- Avoid uploading extremely large files (>30K tokens)
