# text_processor.py
import re
import logging

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
