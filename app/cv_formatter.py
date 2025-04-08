import re

def format_cv_according_to_guidelines(cv_content, job_description):
    """
    Formats the CV according to the provided guidelines
    
    Args:
        cv_content (str): The original CV content
        job_description (str): The job description to adapt to
        
    Returns:
        str: The formatted CV content
    """
    # This is a fallback function when the Gemini API call fails
    
    # Detect language of job description (simple check)
    is_french = any(word in job_description.lower() for word in 
                   ['emploi', 'poste', 'entreprise', 'travail', 'expérience'])
    
    # Extract key terms from job description
    job_terms = set(re.findall(r'\b\w{4,}\b', job_description.lower()))
    
    # Process CV content
    sections = cv_content.split('\n\n')
    formatted_sections = []
    
    for section in sections:
        # Keep section if it contains keywords from job description
        section_terms = set(re.findall(r'\b\w{4,}\b', section.lower()))
        relevance = len(section_terms.intersection(job_terms))
        
        if relevance > 0 or "SUMMARY" in section or "EDUCATION" in section or "EXPERIENCE" in section:
            formatted_sections.append(section)
    
    # Add a note that this is a fallback formatting
    if is_french:
        note = "\n\nNote: Ce CV a été formaté automatiquement sans l'API Gemini."
    else:
        note = "\n\nNote: This CV was automatically formatted without the Gemini API."
    
    return "\n\n".join(formatted_sections) + note