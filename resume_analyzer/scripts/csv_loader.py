# Placeholder for csv_loader.py
import pandas as pd
import logging

def load_csv(file_path, dataset_name):
    try:
        logging.info(f"Attempting to load {dataset_name} from {file_path}")
        df = pd.read_csv(file_path)
        logging.info(f"Successfully loaded {dataset_name}. Shape: {df.shape}")
        logging.info(f"Columns: {df.columns.tolist()}")
        logging.info(f"Sample Data:\n{df.head()}\n")
        return df
    except Exception as e:
        logging.error(f"Error loading {dataset_name}: {e}")
        return None
