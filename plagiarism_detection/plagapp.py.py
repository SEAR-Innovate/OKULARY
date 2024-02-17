import os
import glob
import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import zipfile
import shutil
import streamlit as st
from zipfile import ZipFile
from PyPDF2 import PdfReader
from difflib import SequenceMatcher

# Color Scheme
PAGE_BG_COLOR = "#8CB9BD"
CONTENT_BG_COLOR = "#ECB159"
TEXT_COLOR = "#ECB159"

def calculate_similarity(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def process_zip(zip_file):
    with ZipFile(zip_file, 'r') as zip_ref:
        texts = []
        for file_name in zip_ref.namelist():
            if file_name.endswith('.pdf'):
                with zip_ref.open(file_name) as file:
                    text = extract_text_from_pdf(file)
                    texts.append(text)
    return texts

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
        st.write(f"Similarity between '{file1}' and '{file2}': {similarity_score}")
        if similarity_score > 0.9:
            st.write(f"Complete plagiarism detected between '{file1}' and '{file2}'!")
        else:
            st.write(f"Potential plagiarism detected between '{file1}' and '{file2}'!")

def main(folder_or_zip_path):
    """
    Main function to compare PDF files either in a folder or within a zip file.
    
    Args:
    folder_or_zip_path (str): Path to the folder containing PDF files or to the zip file.
    """
    if folder_or_zip_path.endswith('.zip'):
        # Unzip the file
        output_folder = './zip_outputs'
        unzipped_folder = unzip_file(folder_or_zip_path, output_folder)
        folder_path = os.path.join(unzipped_folder, 'pdfs')
    else:
        folder_path = folder_or_zip_path
    
    # Get all PDF files in the folder
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    num_files = len(pdf_files)
    
    st.write(f"Found {num_files} PDF files in the folder.")
    
    if num_files == 0:
        st.write("No PDF files found in the specified folder.")
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

def main():
    st.title("Plagiarism Detector")

    # Custom CSS to apply background color and color scheme
    st.markdown(f"""
        <style>
            body {{
                background-color: {PAGE_BG_COLOR};
                color: {TEXT_COLOR};
            }}
            .stApp {{
                background-color: {PAGE_BG_COLOR};
            }}
            .stContent {{
                background-color: {CONTENT_BG_COLOR};
            }}
            .stBlockContainer {{
                background-color: {CONTENT_BG_COLOR};
                padding: 10px;
                border-radius: 10px;
            }}
            .stButton:focus {{
                background-color: {CONTENT_BG_COLOR};
            }}
            .stButton:hover {{
                background-color: {CONTENT_BG_COLOR};
            }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.header("Upload Documents or Zip File")

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        st.subheader("Upload Individual PDF Documents")
        file1 = st.file_uploader("Upload first document", type=['pdf'], key='file1')
        file2 = st.file_uploader("Upload second document", type=['pdf'], key='file2')

    with col2:
        st.markdown("<h2 style='text-align: center; color: #0080ff;'>OR</h2>", unsafe_allow_html=True)

    with col3:
        st.subheader("Upload Zip File with PDF Documents")
        zip_file = st.file_uploader("Upload zip file with documents", type=['zip'])

    st.markdown("---")

    plagiarism_button = st.button("Calculate Plagiarism", key='calculate_button', help="Click to check for plagiarism")

    if plagiarism_button:
        if (file1 and file2) or zip_file:
            if file1 and file2:
                text1 = extract_text_from_pdf(file1)
                text2 = extract_text_from_pdf(file2)
                similarity_score = calculate_similarity(text1, text2)
                st.success("Plagiarism Percentage: {}%".format(round(similarity_score * 100, 2)))
            elif zip_file:
                texts = process_zip(zip_file)
                if texts:
                    similarity_score = calculate_similarity(texts[0], texts[1])
                    st.success("Plagiarism Percentage: {}%".format(round(similarity_score * 100, 2)))
                else:
                    st.warning("No .pdf files found in the uploaded zip file or no files uploaded.")
        else:
            st.warning("Please upload at least two PDF documents or one zip file.")

if __name__ == "__main__":
    main()
