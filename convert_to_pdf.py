#!/usr/bin/env python3
"""
Script to convert REVISION_NOTES.md to PDF format
"""

import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os

def markdown_to_pdf(md_file, pdf_file):
    """
    Convert Markdown file to PDF with custom styling
    """
    
    # Read the markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content, 
        extensions=['tables', 'fenced_code', 'toc', 'codehilite']
    )
    
    # Custom CSS for better PDF formatting
    css_content = """
    @page {
        size: A4;
        margin: 2cm;
        @bottom-center {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 12px;
            color: #666;
        }
    }
    
    body {
        font-family: 'Helvetica', 'Arial', sans-serif;
        line-height: 1.6;
        color: #333;
        font-size: 11px;
    }
    
    h1 {
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        margin-top: 30px;
        font-size: 24px;
    }
    
    h2 {
        color: #34495e;
        border-bottom: 2px solid #95a5a6;
        padding-bottom: 5px;
        margin-top: 25px;
        font-size: 18px;
    }
    
    h3 {
        color: #2c3e50;
        margin-top: 20px;
        font-size: 14px;
    }
    
    code {
        background-color: #f8f9fa;
        padding: 2px 5px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
        font-size: 10px;
    }
    
    pre {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 5px;
        padding: 15px;
        overflow-x: auto;
        margin: 15px 0;
        font-size: 9px;
    }
    
    pre code {
        background-color: transparent;
        padding: 0;
        font-size: 9px;
    }
    
    blockquote {
        border-left: 4px solid #3498db;
        margin: 20px 0;
        padding-left: 20px;
        color: #555;
        font-style: italic;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
        font-size: 10px;
    }
    
    table, th, td {
        border: 1px solid #ddd;
    }
    
    th, td {
        padding: 8px;
        text-align: left;
    }
    
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    
    ul, ol {
        margin: 10px 0;
        padding-left: 30px;
    }
    
    li {
        margin: 5px 0;
    }
    
    .toc {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 5px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .toc ul {
        list-style-type: none;
        padding-left: 0;
    }
    
    .toc li {
        margin: 8px 0;
    }
    
    .toc a {
        text-decoration: none;
        color: #3498db;
    }
    
    .highlight {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    
    /* Emoji styling */
    .emoji {
        font-size: 1.2em;
    }
    
    /* Page breaks */
    .page-break {
        page-break-before: always;
    }
    
    /* Better spacing for sections */
    hr {
        border: none;
        border-top: 2px solid #ecf0f1;
        margin: 30px 0;
    }
    """
    
    # Wrap HTML content with proper structure
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>PhonePe EDA Project - Revision Notes</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Create font configuration
    font_config = FontConfiguration()
    
    # Convert to PDF
    try:
        HTML(string=full_html).write_pdf(
            pdf_file,
            stylesheets=[CSS(string=css_content)],
            font_config=font_config
        )
        print(f"✅ Successfully converted {md_file} to {pdf_file}")
        return True
    except Exception as e:
        print(f"❌ Error converting to PDF: {str(e)}")
        return False

if __name__ == "__main__":
    # File paths
    md_file = "REVISION_NOTES.md"
    pdf_file = "PhonePe_EDA_Revision_Notes.pdf"
    
    # Check if markdown file exists
    if not os.path.exists(md_file):
        print(f"❌ Error: {md_file} not found!")
        exit(1)
    
    # Convert to PDF
    success = markdown_to_pdf(md_file, pdf_file)
    
    if success:
        print(f"📄 PDF saved as: {pdf_file}")
        print(f"📏 File size: {os.path.getsize(pdf_file) / 1024:.1f} KB")
    else:
        print("❌ Conversion failed!")
