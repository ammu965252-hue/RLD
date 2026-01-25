from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
import os

def generate_pdf(data, file_path):
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.spaceAfter = 6
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=normal_style,
        leftIndent=20,
        bulletIndent=10
    )
    
    story = []
    
    # Title
    story.append(Paragraph("RiceGuard AI - Disease Detection Report", title_style))
    story.append(Spacer(1, 12))
    
    # Detection Details
    story.append(Paragraph("Detection Details", heading_style))
    story.append(Paragraph(f"<b>Disease:</b> {data['disease']}", normal_style))
    story.append(Paragraph(f"<b>Confidence:</b> {data['confidence']}%", normal_style))
    story.append(Paragraph(f"<b>Severity:</b> {data['severity']}", normal_style))
    story.append(Paragraph(f"<b>Description:</b> {data['description']}", normal_style))
    story.append(Paragraph(f"<b>Date:</b> {data.get('timestamp', 'N/A')}", normal_style))
    
    # Images
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
    original_path = os.path.join(base_dir, data['original_image'].lstrip('/'))
    result_path = os.path.join(base_dir, data['result_image'].lstrip('/'))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("Original Image", heading_style))
    if os.path.exists(original_path):
        img = Image(original_path, 4*inch, 3*inch)
        story.append(img)
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("Detection Result", heading_style))
    if os.path.exists(result_path):
        img = Image(result_path, 4*inch, 3*inch)
        story.append(img)
    
    # Symptoms
    if data.get('symptoms'):
        story.append(Spacer(1, 20))
        story.append(Paragraph("Symptoms Identified", heading_style))
        for symptom in data['symptoms']:
            story.append(Paragraph(f"• {symptom}", bullet_style))
    
    # Treatment
    if data.get('treatment'):
        story.append(Spacer(1, 20))
        story.append(Paragraph("Recommended Treatment", heading_style))
        for treatment in data['treatment']:
            story.append(Paragraph(f"• {treatment}", bullet_style))
    
    # Prevention
    if data.get('prevention'):
        story.append(Spacer(1, 20))
        story.append(Paragraph("Prevention Measures", heading_style))
        for prevention in data['prevention']:
            story.append(Paragraph(f"• {prevention}", bullet_style))
    
    doc.build(story)