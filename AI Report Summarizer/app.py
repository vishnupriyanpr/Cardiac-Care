from flask import Flask, request, render_template, redirect, url_for, flash
import os
from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import textwrap
from werkzeug.utils import secure_filename
from datetime import datetime
from utils.ocr_handler import extract_text_tesseract
from utils.summarizer import generate_summary
from utils.entity_highlighter import highlight_medical_entities

# Setup
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{original_filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Run OCR → Get extracted text
        extracted_text = extract_text_tesseract(filepath)

        # Run Summarization
        summary = generate_summary(extracted_text)

        # Highlight medical terms in extracted text
        highlighted_text = highlight_medical_entities(extracted_text)

        return render_template(
            'summary.html',
            extracted_text=highlighted_text,
            summary=summary
        )
    else:
        flash('File type not allowed (only PDF, PNG, JPG, JPEG)')
        return redirect(url_for('index'))


from flask import request, send_file
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

@app.route('/export-pdf', methods=['POST'])
def export_pdf():
    extracted_text = request.form.get("extracted_text", "")
    summary = request.form.get("summary", "")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=72, bottomMargin=72)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomTitle', fontSize=16, leading=20, spaceAfter=16, fontName='Helvetica-Bold', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='CustomBody', fontSize=11, leading=14, alignment=TA_LEFT))

    story = []

    story.append(Paragraph("Medical Report Summary", styles['CustomTitle']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("📑 Extracted Text", styles['CustomTitle']))
    story.append(Paragraph(extracted_text.replace('\n', '<br/>'), styles['CustomBody']))
    story.append(PageBreak())

    story.append(Paragraph("📝 AI-Generated Summary", styles['CustomTitle']))
    story.append(Paragraph(summary.replace('\n', '<br/>'), styles['CustomBody']))

    doc.build(story)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="Medical_Report_Summary.pdf", mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)
