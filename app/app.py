from flask import Flask, render_template, request, send_file
import google.generativeai as genai
import os
import tempfile
from fpdf import FPDF
from dotenv import load_dotenv
from cv_formatter import format_cv_according_to_guidelines
from pdf_generator import create_professional_cv_pdf

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure the Gemini API with key from .env file
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


def test_gemini_api():
    """Test the Gemini API connection."""
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Hello, please respond with 'API is working' if you can read this message.")
        return True, response.text
    except Exception as e:
        return False, str(e)


def load_cv_template():
    """Load the CV template from file."""
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to the CV template in the app directory
    template_path = os.path.join(current_dir, 'cv_template.txt')
    
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        # Provide a fallback template if the file doesn't exist
        print(f"Warning: CV template file not found at {template_path}")
        return """Bahram Khanlarov
Avenue des Alpes 102, 1820 Montreux, Switzerland
📧 bahram.khanlarov@glion.ch | 📱 +41 79 253 56 99
🔗 linkedin.com/in/bahramkhanlarov | 📂 github.com/bahramkhanlarov

SUMMARY
-----------------
Data Analyst with a Master of Science in Applied Information and Data Science and experience in database management, statistical analysis, and quality control. Proficient in developing and implementing data validation protocols using Python, SQL, and visualization tools like Tableau and Power BI to identify trends and anomalies.

TECHNICAL SKILLS
-----------------
• Programming: Python, SQL
• Database Management: Database design, data integrity and validation
• Data Visualization: Tableau, Power BI, interactive dashboards
• Statistical Analysis: Trend identification, anomaly detection
• Quality Control: Data validation protocols, accuracy verification
• Tools: Git, GitHub, Excel (advanced)

WORK EXPERIENCE
-----------------
International Academy Montreux - Business Development Manager
Jan 2023 - Present
• Designed and implemented database quality control protocols
• Applied statistical modeling techniques to identify trends

EDUCATION
-----------------
Master of Science in Applied Information and Data Science
Lucerne University of Applied Sciences and Arts
Sep 2021 - Dec 2023

CERTIFICATIONS
-----------------
• Oracle Cloud Infrastructure 2024 Generative AI Certified Professional
• Azure Data Scientist Associate
• Power BI Data Analyst Associate
"""


def adapt_cv(cv_template, job_description):
    """
    Adapt the CV to match the job description using Gemini API.
    
    Args:
        cv_template (str): The original CV content
        job_description (str): The job description to adapt to
        
    Returns:
        str: The adapted CV content
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        prompt = f"""
        Adapt this CV to match the following job description, following these guidelines:
        
        1. Keep any job-unrelated material to a minimum
        2. Maintain the exact same formatting and style as the original CV
        3. Structure: personal details, profile summary, key skills, work experience, education
        4. Profile summary: brief statement summarizing journey and key skills for this specific job
        5. Key skills: be selective, focus only on those relevant to the job
        6. Work experience: highlight specific achievements (team size, project scope, efficiency gains)
        7. Keep it concise: aim for maximum 2 pages
        8. Use bullet points with action verbs, avoid narrative style
        9. Tailor wording to match keywords from the job description
        10. IMPORTANT: If the job description is in French, adapt the CV in French. If the job description is in English, adapt the CV in English.
        11. Maintain the exact same section headers, bullet point style, and overall layout
        12. Keep the same formatting for dates, locations, and job titles
        13. Preserve the same style for contact information and personal details
        
        CV:
        {cv_template}
        
        Job Description:
        {job_description}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error using Gemini API: {e}")
        # Fallback to basic formatting if API fails
        return format_cv_according_to_guidelines(cv_template, job_description)


def generate_motivation_letter(cv_template, job_description):
    """
    Generate a motivation letter using Gemini API.
    
    Args:
        cv_template (str): The CV content
        job_description (str): The job description
        
    Returns:
        str: The generated motivation letter
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        prompt = f"""
        Write a professional motivation letter for a job application based on this CV and job description.
        The letter should be concise, compelling, and highlight how the candidate's experience and skills
        match the job requirements. Use a professional tone and format.
        
        IMPORTANT: If the job description is in French, write the motivation letter in French. If the job description is in English, write the motivation letter in English.
        
        CV:
        {cv_template}
        
        Job Description:
        {job_description}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error using Gemini API: {e}")
        # Fallback to basic letter if API fails
        return f"""Dear Hiring Manager,

I am writing to express my interest in the position described in your job posting.

[This would be a personalized motivation letter generated by Gemini API based on your CV and the specific job description]

Sincerely,
Bahram Khanlarov
"""


def create_motivation_letter_pdf(content, filename):
    """
    Create a professionally formatted PDF for the motivation letter.
    
    Args:
        content (str): The motivation letter content
        filename (str): The name for the PDF file (without extension)
        
    Returns:
        str: The path to the created PDF file
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Set default font
    pdf.set_font("Arial", size=11)
    
    # Process content by sections
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Check if line is a header (like "Dear Hiring Manager")
        if i == 0 and ("Dear" in line or "Madame" in line or "Monsieur" in line):
            pdf.set_font("Arial", 'B', 12)  # Bold, size 12
        # Check if line is a signature
        elif i > len(lines) - 3 and ("Sincerely" in line or "Cordialement" in line):
            pdf.set_font("Arial", 'I', 11)  # Italic, size 11
        # Regular text
        else:
            pdf.set_font("Arial", '', 11)  # Regular, size 11
        
        # Handle special characters
        safe_line = line.encode('latin-1', 'replace').decode('latin-1')
        
        # Add the line to the PDF with proper spacing
        if line.strip() == "":
            pdf.ln(5)  # Add extra space for empty lines
        else:
            pdf.multi_cell(0, 6, txt=safe_line, align='L')
    
    # Create a temporary file
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, f"{filename}.pdf")
    pdf.output(pdf_path)
    
    return pdf_path


@app.route('/')
def index():
    """Render the index page with API status."""
    api_working, message = test_gemini_api()
    return render_template('index.html', api_working=api_working, api_message=message)


@app.route('/process', methods=['POST'])
def process():
    """Process the job description and generate adapted documents."""
    job_description = request.form['job_description']
    
    # Load the CV template
    cv_template = load_cv_template()
    
    # Adapt CV based on job description
    adapted_cv = adapt_cv(cv_template, job_description)
    
    # Generate motivation letter
    motivation_letter = generate_motivation_letter(cv_template, job_description)
    
    # Create PDF files
    cv_pdf_path = create_professional_cv_pdf(adapted_cv, "Adapted_CV")
    letter_pdf_path = create_motivation_letter_pdf(motivation_letter, "Motivation_Letter")
    
    # Print paths for debugging
    print(f"CV PDF Path: {cv_pdf_path}")
    print(f"Letter PDF Path: {letter_pdf_path}")
    
    # Store just the filenames for the download route
    return render_template('result.html', 
                          cv=adapted_cv, 
                          letter=motivation_letter,
                          cv_pdf=cv_pdf_path,
                          letter_pdf=letter_pdf_path)


@app.route('/download/<path:filename>')
def download(filename):
    """Download a file."""
    # The filename should be the full path to the temporary file
    if os.path.exists(filename):
        # Get just the filename without the path for the download name
        download_name = os.path.basename(filename)
        return send_file(filename, as_attachment=True, download_name=download_name)
    else:
        # If file doesn't exist, return an error message
        return f"Error: File {filename} not found", 404


if __name__ == '__main__':
    app.run(debug=True, port=5002)