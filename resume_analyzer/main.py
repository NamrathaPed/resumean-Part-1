from file_reader import read_file
from text_processor import clean_text, tokenize_words, tokenize_sentences
from skill_extractor import extract_name, extract_email, extract_phone, extract_skills, extract_skills_with_context, extract_combined_skills
from data_loader import load_csv

# File paths for the two Kaggle CSV files
file_path1 = '/path/to/job_skills.csv'  # Replace with the actual path
file_path2 = '/path/to/linkedin_job_postings.csv' # Replace with the actual path

# Load the datasets
kaggle_df1 = load_csv(file_path1, "Kaggle Dataset 1")
kaggle_df2 = load_csv(file_path2, "Kaggle Dataset 2")

# Check if datasets were loaded successfully
if kaggle_df1 is None or kaggle_df2 is None:
    logging.error("One or both Kaggle datasets failed to load. Please check the file paths and formats.")
else:
    logging.info("Both datasets loaded successfully!")

# Usage example
file_text = read_file('/path/to/resume.docx')  # Replace with actual resume file path
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
print("Phone_number:", phone)

skills = extract_skills(cleaned, skills_list)
print("Skills:", skills)

skills_with_context = extract_skills_with_context(cleaned, skills_list, skill_synonyms)
print("Extracted Skills:", skills_with_context)

combined_skills = extract_combined_skills(cleaned, skills_list)
print("Extracted Skills (Combined):", combined_skills)
