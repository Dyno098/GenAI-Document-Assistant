import streamlit as st
import os
from backend.utils import extract_text_from_pdf, extract_text_from_txt, save_uploaded_file
from backend.summarizer import get_summary
from backend.qa_engine import generate_questions, evaluate_answer
import google.generativeai as genai

# Gemini API Key
genai.configure(api_key="AIzaSyAGSX9k1-3IjgKFCz-vXZmXPL53zDzM9IQ")  # replace with your actual key

# Page settings
st.set_page_config(page_title="GenAI Document Assistant", layout="wide")
st.title("📄 GenAI Document Assistant")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)

    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_txt(file_path)

    st.subheader("📜 Extracted Text (Preview)")
    st.write(text[:1000] + "...")

    # Summary
    st.subheader("🧠 Document Summary")
    summary = get_summary(text)
    st.success(summary)

    # Mode selection
    st.subheader("🤖 Choose Interaction Mode:")
    mode = st.radio("", ["Ask Anything", "Challenge Me"], horizontal=True)

    if mode == "Ask Anything":
        question = st.text_input("💬 Ask a question about the document:")
        if question:
            prompt = f"Based on the following document, answer this question:\n\nDocument:\n{text[:15000]}\n\nQuestion: {question}"
            response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
            st.markdown(f"**Answer:** {response.text}")

    elif mode == "Challenge Me":
        # Reset state for new document
        if "doc_hash" not in st.session_state or st.session_state.doc_hash != hash(text):
            st.session_state.doc_hash = hash(text)
            st.session_state.questions = generate_questions(text, num=3)
            st.session_state.answers = [""] * 3
            st.session_state.feedback = [""] * 3
            st.session_state.submitted = False

        st.subheader("🧠 Answer These Questions:")

        with st.form("challenge_form"):
            for i, q in enumerate(st.session_state.questions):
                st.markdown(f"**Q{i+1}:** {q}")
                st.session_state.answers[i] = st.text_input(
                    f"Your Answer for Q{i+1}", 
                    value=st.session_state.answers[i], 
                    key=f"answer_{i}"
                )
            submitted = st.form_submit_button("Submit Answers")
            if submitted:
                st.session_state.submitted = True

        if st.session_state.submitted:
            st.subheader("📝 Feedback")

            for i, (q, a) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
                if not a.strip():
                    st.warning(f"⚠️ Please provide an answer for Q{i+1}.")
                    continue

                with st.spinner(f"Evaluating Q{i+1}..."):
                    feedback = evaluate_answer(text, q, a)
                    st.session_state.feedback[i] = feedback
                    st.markdown(f"**🔍 Feedback for Q{i+1}:**\n{feedback}")

        if st.button("🔁 Try New Questions"):
            for key in ["questions", "answers", "feedback", "submitted", "doc_hash"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

else:
    st.info("👆 Please upload a PDF or TXT file to begin.")
    st.image(
        "https://images.unsplash.com/photo-1506880018603-83d5b814b5a6",
        width=600,
        caption="Upload a document to analyze its content"
    )
