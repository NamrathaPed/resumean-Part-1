import os

def create_project_structure(base_dir):
    # Define the structure as a dictionary
    structure = {
        "data": ["resumes/", "skills/"],
        "logs": ["app.log"],
        "output": ["results.json"],
        "scripts": ["__init__.py", "file_reader.py", "text_processor.py", "skills_extractor.py", "csv_loader.py"],
        "tests": ["__init__.py", "test_resume_analyzer.py"],
    }
    
    # Create the base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for folder, files in structure.items():
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)  # Create folder
        
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if not file_name.endswith("/"):  # It's a file
                with open(file_path, "w") as f:
                    if file_name == "__init__.py":
                        f.write("# Init file for the package\n")
                    else:
                        f.write(f"# Placeholder for {file_name}\n")

    # Create standalone files in the base directory
    standalone_files = ["main.py", "requirements.txt", "README.md"]
    for file_name in standalone_files:
        file_path = os.path.join(base_dir, file_name)
        with open(file_path, "w") as f:
            if file_name == "requirements.txt":
                f.write("# Add your project dependencies here\n")
            elif file_name == "README.md":
                f.write("# Project Title\n\nWrite a brief description of your project here.\n")
            else:
                f.write("# Entry point of the project\n\nif __name__ == '__main__':\n    print('Hello, Resume Analyzer!')\n")

    print(f"Project structure created at: {base_dir}")

# Set the base directory for the project
base_directory = "resume_analyzer"
create_project_structure(base_directory)
