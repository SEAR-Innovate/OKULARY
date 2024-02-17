import os
import zipfile
from model import scan_for_plagiarism

def main():

    # Ask for the path to the ZIP file
    zip_file_path = input("Enter the path to the ZIP file: ").strip()

    if not zipfile.is_zipfile(zip_file_path):
        print("Error: The provided file is not a valid ZIP file. Please provide a valid ZIP file.")
        return

    # Ask whether to use Level 4 (OpenAI based Paraphrasing Detection)
    use_level4 = input("Do you want to use Level 4 (OpenAI based Paraphrasing Detection) (Alpha Mode)? (yes/no): ").strip().lower()
    if use_level4 == 'yes':
        use_level4 = True
    else:
        use_level4 = False

    # Define the extraction destination as the directory of the current Python script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    extraction_dest = os.path.join(script_directory)

    folder_name, _ = os.path.splitext(os.path.basename(zip_file_path))
    destination_folder = os.path.join(extraction_dest, folder_name)

    # Check whether the folder uploaded already exist in the directory, if not then extract it
    if not os.path.exists(destination_folder):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            os.makedirs(extraction_dest, exist_ok=True)
            zip_ref.extractall(extraction_dest)

    # Run plagiarism detection
    print("Running plagiarism detection...")
    scan_for_plagiarism('plagiarism_detection/plagiarism_rishit/handwriting', use_level4)
    print("Plagiarism detection completed.")

if __name__ == "__main__":
    main()
