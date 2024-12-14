import os
import pdfplumber
from docx import Document
import re
import spacy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of predefined skills
skills_list = [
    "Python", "Java", "c++", "SQL", "Machine Learning", "Data Analysis",
    "Communication", "Leadership", "Problem-Solving", "DevOps"
]
# Synonym and abbreviation mapping
skill_synonyms = {
    "ML": "Machine Learning",
    "AI": "Artificial Intelligence",
    "NLP": "Natural Language Processing",
    "DB": "Database",
    "SQL Server": "SQL",
    "C-sharp": "C#",
    "JS": "JavaScript"
}


# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")


def read_file(filepath):
    try:
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".pdf":
            logging.info("Processing PDF file.")
            return read_pdf(filepath)
        elif ext == ".docx":
            logging.info("Processing DOCX file.")
            return read_docx(filepath)
        raise ValueError(f"Unsupported file format: {ext}")
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return ''


def read_pdf(filepath):
    try:
        extracted_text = ''
        with pdfplumber.open(filepath) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                extracted_text += f"--- Page {page_num + 1} ---\n{page_text}\n" if page_text else ''
        return extracted_text
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
        return ''


def read_docx(filepath):
    try:
        extracted_text = ''
        doc = Document(filepath)
        for paragraph in doc.paragraphs:
            extracted_text += paragraph.text + '\n'
        return extracted_text
    except Exception as e:
        logging.error(f"Error reading DOCX: {e}")
        return ''


def clean_text(extracted_text):
    try:
        return re.sub(r'\s+', ' ', extracted_text).strip().lower()
    except Exception as e:
        logging.error(f"Error cleaning text: {e}")
        return ''


def tokenize_words(cleaned_text):
    try:
        return cleaned_text.split()
    except Exception as e:
        logging.error(f"Error tokenizing words: {e}")
        return []


def tokenize_sentences(cleaned_text):
    try:
        sentences = re.split(r'[.!?]+', cleaned_text)
        return [sentence.strip() for sentence in sentences if sentence.strip()]
    except Exception as e:
        logging.error(f"Error tokenizing sentences: {e}")
        return []


def extract_name(cleaned_text):
    try:
        # Step 1: Attempt manual extraction from the first line
        lines = cleaned_text.split("\n")
        for line in lines:
            if line.strip():  # Check for a non-empty line
                potential_name = line.strip().title()  # Title-case the name
                if len(potential_name.split()) >= 2 and all(word.isalpha() for word in potential_name.split()):
                    return potential_name

        doc = nlp(cleaned_text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":  # Look for PERSON entities
                return ent.text

        return "Name not found"
    except Exception as e:
        logging.error(f"Error extracting name: {e}")
        return "Name not found"



def extract_email(cleaned_text):
    try:
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_matches = re.findall(email_pattern, cleaned_text)
        return email_matches[0]
    except Exception as e:
        logging.error(f"Error extracting email: {e}")
        return None


def extract_phone(cleaned_text):
    try:
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_matches = re.findall(phone_pattern, cleaned_text)
        return phone_matches[0]
    except Exception as e:
        logging.error(f"Error extracting phone number: {e}")
        return None


def extract_skills(cleaned_text, skills_list):
    try:
        tokens = tokenize_words(cleaned_text)
        return [skill for skill in skills_list if skill.lower() in tokens]
    except Exception as e:
        logging.error(f"Error extracting skills: {e}")
        return []

from spacy.matcher import Matcher

def extract_skills_with_context(cleaned_text, skills_list, skill_synonyms):
    """
    Extracts skills using contextual NLP and maps synonyms/abbreviations to standardized skill names.
    """
    # Tokenize and analyze text with Spacy NLP
    doc = nlp(cleaned_text)
    extracted_skills = set()
    
    for token in doc:
        # Match skills in the predefined list or their synonyms
        if token.text in skills_list:
            extracted_skills.add(token.text)
        elif token.text in skill_synonyms:
            extracted_skills.add(skill_synonyms[token.text])  # Map synonym to standard skill name

    # Check for multi-word skills using Spacy's noun chunking
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower()
        for skill in skills_list:
            if skill.lower() in chunk_text:
                extracted_skills.add(skill)

    return list(extracted_skills)


def extract_combined_skills(cleaned_text, skills_list):
    try:
        # Basic extraction
        basic_skills = extract_skills(cleaned_text, skills_list)
        
        # Contextual extraction
        contextual_skills = extract_skills_with_context(cleaned_text, skills_list)
        
        # Combine results, removing duplicates
        combined_skills = list(set(basic_skills + contextual_skills))
        
        return combined_skills
    except Exception as e:
        logging.error(f"Error in combined skill extraction: {e}")
        return []





# usage
file_text = read_file('/Users/namratha/Downloads/Fathima Khader final resume.docx')
print("Extracted Text:\n", file_text)

# Clean
cleaned = clean_text(file_text)
print("\nCleaned Text:\n", cleaned)

# Tokenize into words
words = tokenize_words(cleaned)
print("\nWords:", words)

# Tokenize into sentences
sentences = tokenize_sentences(cleaned)
print("\nSentences:", sentences)

name = extract_name(cleaned)
print("Extracted Name:", name)

email = extract_email(cleaned)
print("Email:", email)

phone = extract_phone(cleaned)
print ("Phone_number:", phone)

skills = extract_skills(cleaned, skills_list)
print("Skills:", skills)

skills_with_context = extract_skills_with_context(cleaned, skills_list, skill_synonyms)
print("Extracted Skills:", skills_with_context)

combined_skills = extract_combined_skills(cleaned, skills_list)
print("Extracted Skills (Combined):", combined_skills)


