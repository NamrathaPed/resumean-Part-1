#skills extractor
import re
import spacy
import logging
from text_processor import tokenize_words

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

def extract_name(cleaned_text):
    try:
        lines = cleaned_text.split("\n")
        for line in lines:
            if line.strip():
                potential_name = line.strip().title()
                if len(potential_name.split()) >= 2 and all(word.isalpha() for word in potential_name.split()):
                    return potential_name

        doc = nlp(cleaned_text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text

        return "Name not found"
    except Exception as e:
        logging.error(f"Error extracting name: {e}")
        return "Name not found"

def extract_email(cleaned_text):
    try:
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_matches = re.findall(email_pattern, cleaned_text)
        return email_matches[0] if email_matches else None
    except Exception as e:
        logging.error(f"Error extracting email: {e}")
        return None

def extract_phone(cleaned_text):
    try:
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_matches = re.findall(phone_pattern, cleaned_text)
        return phone_matches[0] if phone_matches else None
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

def extract_skills_with_context(cleaned_text, skills_list, skill_synonyms):
    doc = nlp(cleaned_text)
    extracted_skills = set()
    
    for token in doc:
        if token.text in skills_list:
            extracted_skills.add(token.text)
        elif token.text in skill_synonyms:
            extracted_skills.add(skill_synonyms[token.text])

    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower()
        for skill in skills_list:
            if skill.lower() in chunk_text:
                extracted_skills.add(skill)

    return list(extracted_skills)

def extract_combined_skills(cleaned_text, skills_list):
    try:
        basic_skills = extract_skills(cleaned_text, skills_list)
        contextual_skills = extract_skills_with_context(cleaned_text, skills_list, skill_synonyms)
        combined_skills = list(set(basic_skills + contextual_skills))
        return combined_skills
    except Exception as e:
        logging.error(f"Error in combined skill extraction: {e}")
        return []
