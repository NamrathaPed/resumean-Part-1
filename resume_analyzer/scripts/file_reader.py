# file_reader.py
import pdfplumber
from docx import Document
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

