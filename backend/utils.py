import os
import fitz  # PyMuPDF

def save_uploaded_file(uploaded):
    folder = "uploaded_docs"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, uploaded.name)
    with open(path, "wb") as f:
        f.write(uploaded.getbuffer())
    return path

def extract_text_from_pdf(path):
    text = ""
    for page in fitz.open(path):
        text += page.get_text()
    return text

def extract_text_from_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
