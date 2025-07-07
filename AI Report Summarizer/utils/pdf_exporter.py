from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf(output_path, extracted_text, summary_text):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    margin = 50
    y = height - margin

    def draw_multiline(text, title, y):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, title)
        y -= 20
        c.setFont("Helvetica", 10)
        for line in text.split('\n'):
            for wrapped in split_line(line, 90):
                if y <= margin:
                    c.showPage()
                    y = height - margin
                    c.setFont("Helvetica", 10)
                c.drawString(margin, y, wrapped)
                y -= 14
        return y

    def split_line(text, max_chars):
        return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

    y = draw_multiline(extracted_text, "Extracted Text", y)
    y = draw_multiline(summary_text, "Summary", y - 20)

    c.save()
