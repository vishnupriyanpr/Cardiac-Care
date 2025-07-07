import spacy
import re

# Load SciSpaCy model
nlp = spacy.load("en_core_sci_sm")

def highlight_medical_entities(text):
    """
    Highlight medical entities (from SciSpaCy) + numeric measurements in text,
    wrapping them with <mark> tags for frontend display.
    """

    doc = nlp(text)
    entities = []

    # Collect all medical entity spans
    for ent in doc.ents:
        if len(ent.text.strip()) > 1:  # ignore very short entities
            entities.append({
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char
            })

    # Also extract key numeric values and percentages (e.g., "13.5%", "120 mg/dL", "98.6°F")
    # Regex: numbers possibly with decimals + optional units or % sign
    numeric_pattern = r'\b\d{1,3}(?:\.\d+)?\s?(?:%|mg/dL|g/dL|°F|°C|mmHg|units)?\b'
    for match in re.finditer(numeric_pattern, text):
        entities.append({
            "text": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    # Remove duplicates (by text & positions)
    seen = set()
    unique_entities = []
    for ent in entities:
        key = (ent["text"].lower(), ent["start"], ent["end"])
        if key not in seen:
            unique_entities.append(ent)
            seen.add(key)

    # Sort entities by start position (ascending)
    unique_entities.sort(key=lambda e: e["start"])

    # Highlight text by injecting <mark> tags without messing up indices
    # We'll build the new text incrementally:
    highlighted_text = ""
    last_index = 0

    for ent in unique_entities:
        # Append text before entity
        highlighted_text += text[last_index:ent["start"]]
        # Append highlighted entity text
        highlighted_text += f"<mark>{text[ent['start']:ent['end']]}</mark>"
        last_index = ent["end"]

    # Append remaining text after last entity
    highlighted_text += text[last_index:]

    return highlighted_text
