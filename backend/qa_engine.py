import google.generativeai as genai

# Assumes genai.configure() has already been done in app.py
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_questions(text, num=3):
    prompt = (
        f"Based only on the document below, generate exactly {num} challenging, logic-based, context-grounded questions."
        f"Number them clearly like 1., 2., 3. and do not include any intro text.\n\n"
        f"Document:\n{text[:15000]}"
    )
    response = model.generate_content(prompt)
    raw = response.text.strip().split("\n")

    questions = []
    for line in raw:
        line = line.strip()
        if line and any(line.startswith(f"{i}.") for i in range(1, num + 2)):
            # Extract after "1. ", "2. ", etc.
            q = line.split(". ", 1)[-1].strip()
            if q:
                questions.append(q)

    return questions[:num]

def evaluate_answer(document_text, question, user_answer):
    eval_prompt = (
        f"Document:\n{document_text[:15000]}\n\n"
        f"Question: {question}\n"
        f"User Answer: {user_answer}\n\n"
        f"Evaluate the answer based only on the document. Say if it is correct, incorrect, or partially correct. "
        f"Explain briefly and cite relevant evidence from the document."
    )
    response = model.generate_content(eval_prompt)
    return response.text
