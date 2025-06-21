from transformers import pipeline

# Load summarization pipeline using BART
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def get_summary(text, max_length=150):
    """
    Generate a summary of the text (<=150 words).
    """
    if len(text.split()) < 100:
        return text  # Skip summarization for short documents
    
    # Huggingface expects short input, so truncate if too long
    input_text = text[:3000] if len(text) > 3000 else text
    result = summarizer(input_text, max_length=max_length, min_length=40, do_sample=False)
    return result[0]['summary_text']