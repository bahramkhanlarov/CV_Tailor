# CV Modification Tool

A web application that automatically adapts your CV and generates a motivation letter based on job descriptions using Google's Gemini AI.

## Features

- Adapts your CV to match specific job descriptions
- Generates tailored motivation letters
- Supports both English and French job descriptions
- Creates downloadable PDF documents
- Simple and intuitive web interface

## Installation

1. Clone the repository:
   
```bash
git clone https://github.com/bahramkhanlarov/CV_Tailor.git
cd CV_Tailor
'''

2. Install the required dependencies:

pip install -r requirements.txt

3. Create a .env file in the root directory with your Gemini API key:

GEMINI_API_KEY=your_api_key_here

## Usage
1. Start the application:

python app/app.py

2. Open your web browser and navigate to:

http://127.0.0.1:5002

3. Paste a job description into the text area and click "Generate Documents"
4. View and download your adapted CV and motivation letter


## Project Structure
- app/app.py : Main Flask application
- app/cv_formatter.py : Fallback CV formatting logic
- app/pdf_generator.py : PDF generation utilities
- cv_template.txt : Your CV template
- templates/ : HTML templates for the web interface

## Requirements
- Python 3.8+
- Flask
- Google Generative AI Python SDK
- FPDF
- python-dotenv

## License
MIT

## Author
Bahram Khanlarov
