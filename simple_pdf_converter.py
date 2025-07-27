#!/usr/bin/env python3
"""
Simple script to convert REVISION_NOTES.md to PDF using reportlab
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import re
import os

def clean_markdown_for_pdf(content):
    """Clean markdown content for PDF conversion"""
    
    # Remove markdown table of contents links
    content = re.sub(r'\[([^\]]+)\]\(#[^)]+\)', r'\1', content)
    
    # Convert markdown headers to simpler format
    content = re.sub(r'^#{6}\s+(.+)$', r'<h6>\1</h6>', content, flags=re.MULTILINE)
    content = re.sub(r'^#{5}\s+(.+)$', r'<h5>\1</h5>', content, flags=re.MULTILINE)
    content = re.sub(r'^#{4}\s+(.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
    content = re.sub(r'^#{3}\s+(.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^#{2}\s+(.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^#{1}\s+(.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    
    # Convert code blocks
    content = re.sub(r'```python\n(.*?)\n```', r'<pre>\1</pre>', content, flags=re.DOTALL)
    content = re.sub(r'```\n(.*?)\n```', r'<pre>\1</pre>', content, flags=re.DOTALL)
    
    # Convert inline code
    content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
    
    # Convert bold
    content = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', content)
    
    # Convert italic
    content = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', content)
    
    # Clean up emojis and special characters
    content = re.sub(r'[📚🎯🛠️📊🔍💻🔑⚠️🎤🚀🔧📝]', '', content)
    
    # Remove horizontal rules
    content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)
    
    return content

def create_pdf_from_markdown(md_file, pdf_file):
    """Create PDF from markdown file"""
    
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean content
    content = clean_markdown_for_pdf(content)
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=30,
        textColor=HexColor('#2c3e50'),
        alignment=TA_CENTER
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        textColor=HexColor('#2c3e50')
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        textColor=HexColor('#34495e')
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        textColor=HexColor('#2c3e50')
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        leftIndent=20,
        rightIndent=20,
        spaceAfter=12,
        backColor=HexColor('#f8f9fa')
    )
    
    # Story for PDF content
    story = []
    
    # Split content into sections
    lines = content.split('\n')
    current_paragraph = []
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                if para_text:
                    story.append(Paragraph(para_text, styles['Normal']))
                    story.append(Spacer(1, 6))
                current_paragraph = []
            continue
        
        # Handle headers
        if line.startswith('<h1>'):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                story.append(Paragraph(para_text, styles['Normal']))
                current_paragraph = []
            
            header_text = re.sub(r'</?h1>', '', line)
            if 'PhonePe EDA Project - Revision Notes' in header_text:
                story.append(Paragraph(header_text, title_style))
            else:
                story.append(Paragraph(header_text, heading1_style))
            story.append(Spacer(1, 12))
            
        elif line.startswith('<h2>'):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                story.append(Paragraph(para_text, styles['Normal']))
                current_paragraph = []
            
            header_text = re.sub(r'</?h2>', '', line)
            story.append(Paragraph(header_text, heading2_style))
            story.append(Spacer(1, 10))
            
        elif line.startswith('<h3>'):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                story.append(Paragraph(para_text, styles['Normal']))
                current_paragraph = []
            
            header_text = re.sub(r'</?h3>', '', line)
            story.append(Paragraph(header_text, heading3_style))
            story.append(Spacer(1, 8))
            
        elif line.startswith('<pre>') and line.endswith('</pre>'):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                story.append(Paragraph(para_text, styles['Normal']))
                current_paragraph = []
            
            code_text = re.sub(r'</?pre>', '', line)
            if code_text.strip():
                story.append(Paragraph(code_text, code_style))
                story.append(Spacer(1, 6))
            
        else:
            # Regular paragraph content
            current_paragraph.append(line)
    
    # Add any remaining paragraph
    if current_paragraph:
        para_text = ' '.join(current_paragraph)
        if para_text:
            story.append(Paragraph(para_text, styles['Normal']))
    
    # Build PDF
    try:
        doc.build(story)
        print(f"✅ Successfully created PDF: {pdf_file}")
        return True
    except Exception as e:
        print(f"❌ Error creating PDF: {str(e)}")
        return False

if __name__ == "__main__":
    md_file = "REVISION_NOTES.md"
    pdf_file = "PhonePe_EDA_Revision_Notes.pdf"
    
    if not os.path.exists(md_file):
        print(f"❌ Error: {md_file} not found!")
        exit(1)
    
    success = create_pdf_from_markdown(md_file, pdf_file)
    
    if success:
        print(f"📄 PDF saved as: {pdf_file}")
        file_size = os.path.getsize(pdf_file) / 1024
        print(f"📏 File size: {file_size:.1f} KB")
    else:
        print("❌ PDF conversion failed!")
