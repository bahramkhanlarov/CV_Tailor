from fpdf import FPDF
import os
import tempfile
import re

def create_professional_cv_pdf(cv_content, filename):
    """
    Creates a professionally formatted PDF from CV content
    
    Args:
        cv_content (str): The CV content to convert to PDF
        filename (str): The name for the PDF file (without extension)
        
    Returns:
        str: The path to the created PDF file
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Set default font
    pdf.set_font("Arial", size=10)
    
    # Process content by sections
    lines = cv_content.split('\n')
    
    for i, line in enumerate(lines):
        # Check if line is a header (all caps or followed by dashes)
        if line.isupper() or (i < len(lines) - 1 and lines[i+1].startswith('---')):
            pdf.set_font("Arial", 'B', 12)  # Bold, size 12
        # Check if line might be a subheader or job title
        elif re.match(r'^[A-Z][\w\s]+([-|]|:)', line):
            pdf.set_font("Arial", 'B', 11)  # Bold, size 11
        # Check if line is a bullet point
        elif line.strip().startswith('•'):
            pdf.set_font("Arial", '', 10)  # Regular, size 10
            # Add some indentation for bullet points
            pdf.cell(10)
        else:
            pdf.set_font("Arial", '', 10)  # Regular, size 10
        
        # Handle special characters
        safe_line = line.encode('latin-1', 'replace').decode('latin-1')
        
        # Add the line to the PDF
        pdf.cell(0, 6, txt=safe_line, ln=True)
        
        # Add extra space after section headers
        if i < len(lines) - 1 and lines[i+1].startswith('---'):
            pdf.ln(2)
    
    # Create a temporary file
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, f"{filename}.pdf")
    pdf.output(pdf_path)
    
    return pdf_path