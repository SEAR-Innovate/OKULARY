import os
import glob
import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import zipfile
import shutil

def read_pdf(file_path):
    """
    Read text content from a PDF file.
    
    Args:
    file_path (str): Path to the PDF file.
    
    Returns:
    str: Text content of the PDF.
    """
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

def text_similarity(text1, text2):
    """
    Compute the cosine similarity between two texts.
    
    Args:
    text1 (str): The first text.
    text2 (str): The second text.
    
    Returns:
    float: The cosine similarity between the two texts.
    """
    # Create a CountVectorizer instance
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    
    # Calculate cosine similarity
    similarity = cosine_similarity(vectorizer)
    
    # Since there are only 2 texts, similarity[0, 1] or similarity[1, 0] gives the similarity
    return similarity[0, 1]

def compare_pdfs(pdf_file1, pdf_file2):
    """
    Compare two PDF files for similarity.
    
    Args:
    pdf_file1 (str): Path to the first PDF file.
    pdf_file2 (str): Path to the second PDF file.
    """
    text1 = read_pdf(pdf_file1)
    text2 = read_pdf(pdf_file2)
    file1 = pdf_file1.split('/')[-1]
    file2 = pdf_file2.split('/')[-1]
    similarity_score = text_similarity(text1, text2)
    if similarity_score > 0.75:
        print(f"Similarity between '{file1}' and '{file2}': {similarity_score}")
        if similarity_score > 0.9:
            print(f"Complete plagiarism detected between '{file1}' and '{file2}'!")
        else:
            print(f"Potential plagiarism detected between '{file1}' and '{file2}'!")

def main(folder_or_zip_path):
    """
    Main function to compare PDF files either in a folder or within a zip file.
    
    Args:
    folder_or_zip_path (str): Path to the folder containing PDF files or to the zip file.
    """
    if folder_or_zip_path.endswith('.zip'):
        # Unzip the file
        output_folder = '/Users/rishit/Documents/innovate_you/plagiarism_detection/plagiarism_rishit/zip_outputs'
        unzipped_folder = unzip_file(folder_or_zip_path, output_folder)
        folder_path = os.path.join(unzipped_folder, 'pdfs')
    else:
        folder_path = folder_or_zip_path
    
    # Get all PDF files in the folder
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    num_files = len(pdf_files)
    
    print(f"Found {num_files} PDF files in the folder.")
    
    if num_files == 0:
        print("No PDF files found in the specified folder.")
        return
    
    # Compare similarity for all pairs of PDF files
    for i in range(num_files):
        for j in range(i+1, num_files):
            compare_pdfs(pdf_files[i], pdf_files[j])

def unzip_file(zip_file, output_folder):
    """
    Unzip a zip file to the specified output folder.
    
    Args:
    zip_file (str): Path to the zip file.
    output_folder (str): Path to the output folder where the contents will be extracted.
    
    Returns:
    str: Path to the folder containing the extracted files.
    """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Empty the output folder if it already exists
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    
    # Extract the zip file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
    
    return output_folder

# Example usage:
input_path = input("Enter the path to the folder containing PDF files or to the zip file: ").strip()
main(input_path)
