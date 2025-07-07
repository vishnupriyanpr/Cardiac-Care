# utils/summarizer.py

from transformers import pipeline
import re

# Load the summarization pipeline (you can replace with another model if needed)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text, max_length=300, min_length=100):
    cleaned_text = text.replace("\n", " ").strip()

    if len(cleaned_text.split()) < 50:
        return "Text too short to summarize."

    # If too long for the model, split into smaller chunks (for PDFs)
    if len(cleaned_text.split()) > 800:  # Approximate token limit
        chunks = []
        words = cleaned_text.split()
        chunk_size = 400
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            result = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            if result and 'summary_text' in result[0]:
                chunks.append(result[0]['summary_text'])
        combined = " ".join(chunks)
        return format_summary(combined)

    # Normal summarization for images/small text
    summary = summarizer(cleaned_text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
    return format_summary(summary)


def format_summary(text):
    # Fix extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Capitalize first letter of each sentence
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s[0].upper() + s[1:] if len(s) > 1 else s for s in sentences]
    formatted = '\n\n'.join(sentences)

    # Convert + signs and lists into bullet points
    formatted = re.sub(r"(including, but not limited to:|risks include:)", r"\1\n -", formatted)
    formatted = re.sub(r"\s*\+\s*", r"\n - ", formatted)

    return formatted.strip()
