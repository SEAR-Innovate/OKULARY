import streamlit as st
from streamlit_option_menu import option_menu

import sys
sys.path.append('./student_analysis')

st.markdown("<h1 style='text-align: center; color: #FF5733;'>📚 OKULARY: Empowering Educators with Innovative Solutions </h1>", unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options= ["Home","Plagiarism Checker","Teacher Resources","Teacher Community","AI Course Outcomes and Answer Checking","Student Performance Tracking"],
    default_index=0,
    orientation="horizontal",
    styles={
    "container": {"padding": "0!important"},
    "icon": {"color": "#FF5733", "font-size": "12px"}, 
    "nav-link": {"font-size": "10px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "#FF5733"},
    }
)


if selected == 'Home':
    st.markdown('''
Welcome to **OKULARY**, the ultimate teacher helper website designed to revolutionize the teaching experience. Our platform is built to address the diverse needs of educators by providing a comprehensive suite of resources, teaching methodologies, community support, AI-driven assessments, and performance analytics. 

🎯 Our aim is to develop an all-encompassing educational platform tailored for teachers, providing comprehensive resources, teaching methodologies, community support, AI-driven assessments, and performance analytics.

🔧 Our platform is designed to empower educators with the tools and resources they need to excel in their profession. Whether you're a seasoned teacher looking for new teaching strategies or a new teacher seeking guidance, **OKULARY** has something for everyone. Sign up now and start your journey towards becoming a more effective and successful educator.''')

    st.markdown('''
## **Key Features:**

- **📚 Resource Repository:** Access to a vast repository of educational resources.
- **📝 Teaching Methodologies:** Guidance on effective teaching techniques and methodologies.
- **👩‍🏫 Teacher Community:** A supportive online community for collaboration and sharing experiences.
- **🤖 AI Course Outcomes and Answer Checking:** Automated assessment of course outcomes and answer checking using AI.
- **🕵️‍♂️ Cheating and Malpractice Detection:** AI-powered tools to detect cheating and malpractice.
- **📊 Student Performance Tracking:** Monitoring and tracking individual student performance.
- **📈 Class Performance Analytics:** Data analytics to analyze class performance trends and patterns.
- **👀 AI Class Monitoring:** Innovative system to monitor student attentiveness and manage attendance using AI technology.
''')

    st.markdown('''
## **Get Started with OKULARY Today!**

Join **OKULARY** today and take your teaching to the next level. Our platform is designed to empower educators with the tools and resources they need to excel in their profession. Whether you're a seasoned teacher looking for new teaching strategies or a new teacher seeking guidance, **OKULARY** has something for everyone. Sign up now and start your journey towards becoming a more effective and successful educator.''')


elif selected == 'Plagiarism Checker':
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
    # PAGE_BG_COLOR = "#8CB9BD"
    # CONTENT_BG_COLOR = "#ECB159"
    # TEXT_COLOR = "#ECB159"
    
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
    
        # # Custom CSS to apply background color and color scheme
        # st.markdown(f"""
        #     <style>
        #         body {{
        #             background-color: {PAGE_BG_COLOR};
        #             color: {TEXT_COLOR};
        #         }}
        #         .stApp {{
        #             background-color: {PAGE_BG_COLOR};
        #         }}
        #         .stContent {{
        #             background-color: {CONTENT_BG_COLOR};
        #         }}
        #         .stBlockContainer {{
        #             background-color: {CONTENT_BG_COLOR};
        #             padding: 10px;
        #             border-radius: 10px;
        #         }}
        #         .stButton:focus {{
        #             background-color: {CONTENT_BG_COLOR};
        #         }}
        #         .stButton:hover {{
        #             background-color: {CONTENT_BG_COLOR};
        #         }}
        #     </style>
        # """, unsafe_allow_html=True)
    
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
    
elif selected == 'AI Class Monitoring':
    pass
elif selected == 'Teacher Community':
    import streamlit as st
    import pandas as pd
    from datetime import datetime
    
    csv_file_path = "questions.csv"
    
    def load_questions():
        try:
            return pd.read_csv(csv_file_path, converters={'Answers': eval})
        except FileNotFoundError:
            return pd.DataFrame(columns=['Question', 'Upvotes', 'Downvotes', 'Answers'])
    
    def save_data_to_csv(df):
        df.to_csv(csv_file_path, index=False)
    
    def upvote_question(index, questions_df):
        questions_df.at[index, 'Upvotes'] += 1
        save_data_to_csv(questions_df)
    
    def downvote_question(index, questions_df):
        questions_df.at[index, 'Downvotes'] += 1
        save_data_to_csv(questions_df)
    
    def add_answer(index, answer, questions_df):
        questions_df.at[index, 'Answers'].append(answer)
        save_data_to_csv(questions_df)
        st.success("Answer posted successfully!")
    
    def display_question_with_answers(index, question, upvotes, downvotes, answers, questions_df):
        st.markdown(f"<h3 style='color:darkblue;'>{index + 1}. {question}</h3>", unsafe_allow_html=True)
        st.markdown(f"👍 **{upvotes}**  👎 **{downvotes}**")
        st.markdown("**Answers:**")
        
        if answers:
            for ans in answers:
                st.markdown(f"- {ans}")
        else:
            st.markdown("- No answers yet.")
        
        st.markdown('---')
        col1, col2 = st.columns([1, 10])
        with col1:
            upvote_button = st.button(label="👍", key=f'upvote_{index}')
        with col2:
            downvote_button = st.button(label="👎", key=f'downvote_{index}')
        if upvote_button:
            upvote_question(index, questions_df)
        if downvote_button:
            downvote_question(index, questions_df)
        answer_key = f'answer_{index}_{datetime.now().strftime("%Y%m%d%H%M%S")}'
        answer = st.text_area(label="Your Answer:", key=answer_key)
        answer_button = st.button(label="Post Answer", key=f'post_answer_{index}')
        
        
        if answer_button and answer:
            add_answer(index, answer, questions_df)
            
            questions_df = load_questions()
            st.markdown(f"- {answer}", unsafe_allow_html=True) 
    
    def main():
        st.title("Teaching Q&A Forum")
        st.markdown("***")
        questions_df = load_questions()
        st.sidebar.header("Post a New Question")
        new_question = st.sidebar.text_area(label="Enter your question here:", height=100)
        post_question_button = st.sidebar.button(label="Post Question")
    
        if post_question_button and new_question:
            new_row = pd.DataFrame({'Question': [new_question], 'Upvotes': [0], 'Downvotes': [0], 'Answers': [[]]})
            questions_df = pd.concat([questions_df, new_row], ignore_index=True)
            save_data_to_csv(questions_df)
            st.sidebar.success("Question posted successfully!")
        
        st.header("Existing Questions")
        for i, row in questions_df.iterrows():
            display_question_with_answers(i, row['Question'], row['Upvotes'], row['Downvotes'], row['Answers'], questions_df)
    
        existing_question_index = st.sidebar.selectbox("Select a question to answer:", questions_df.index.tolist())
        answer_key = f'answer_{existing_question_index}'
        answer_to_existing_question = st.sidebar.text_area(label="Your Answer:", key=answer_key)
        post_answer_to_existing_question_button = st.sidebar.button(label="Post Answer", key=f'post_answer_to_existing_question_{existing_question_index}')
        
        if post_answer_to_existing_question_button and answer_to_existing_question:
            add_answer(existing_question_index, answer_to_existing_question, questions_df)
            
            questions_df = load_questions()
    
    if __name__ == "__main__":
        main()
elif selected == 'Student Performance Tracking':
    import streamlit as st
    import pandas as pd
    import os
    
    # Assuming these are the functions you've defined
    from main import (
        default_dashboard_class, 
        default_dashboard_student, 
        plot_dashboard_class, 
        plot_dashboard_student,
    )
    from download_report import create_pdf
    
    # List of student names
    student_names = ["Brian Freeman", "Eric Wilson", "Charles Carpenter", "Joseph Lara", "Sara Rivera", "Penny White"]
    
    # List of available subjects
    subjects = ['maths', 'computer science', 'reading', 'writing', 'physics']
    
    # Dictionary for options in each mode
    student_default_options = {
        "Plot Scores for the student": "Plot Scores for the student",
        "Plot Individual Semester Progress(Line Plot)": "Plot Individual Semester Progress(Line Plot)",
        "Plot Individual Semester Progress (Box Plot)": "Plot Individual Semester Progress (Box Plot)",
        "Improvements and Decline of Marks": "Improvements and Decline of Marks",
    }
    
    class_default_options = {
        "Scores with respect to gender": "Scores with respect to gender",
        "Impact of course completion on grades": "Impact of course completion on grades",
        "Mean Scores": "Mean Scores",
        "Median Scores": "Median Scores",
        "Highest Scores": "Highest Scores",
        "Lowest Scores": "Lowest Scores",
    }
    
    # Streamlit app
    def main():
        st.title("Student Dashboards")
        dashboard_type = st.radio("Choose Dashboard Type", ("Student", "Class"))
    
        if dashboard_type == "Student":
            st.subheader("Student Dashboard")
            selected_student = st.selectbox("Select Student", student_names)
            dashboard_mode = st.radio("Dashboard Mode", ("Default", "Custom"))
            
            st.subheader("Download Student Report")
            image_folder = './student_analysis/requested_plots'
            pdf_bytes = None
            output_file = None
            
            if st.button("Generate Report"):
                if selected_student and image_folder:
                    output_file = create_pdf(selected_student, image_folder)
                    with open(output_file, "rb") as f:
                        pdf_bytes = f.read()
            if pdf_bytes is not None and output_file is not None:
                st.download_button(label="Download Report", data=pdf_bytes, file_name=output_file, mime="application/pdf")
                st.success("Report generated successfully!")
    
            if dashboard_mode == "Default":
                default_dashboard_student(selected_student)
            else:
                selected_plots = st.multiselect("Select Plots", list(student_default_options.keys()))
                plot_dashboard_student(selected_plots, selected_student, subjects)
            
            
    
        else:  # Class dashboard
            st.subheader("Class Dashboard")
            class_mode = st.radio("Dashboard Mode", ("Default", "Custom"))
            subject = st.selectbox("Select Subject", subjects)
    
            if class_mode == "Default":
                
                default_dashboard_class(subject)
            else:
                selected_plots = st.multiselect("Select Plots", list(class_default_options.keys()))
                plot_dashboard_class(selected_plots, subject)
                
        st.header("Requested Plots")
        image_folder = "./student_analysis/requested_plots"
        if os.path.exists(image_folder):
            image_files = os.listdir(image_folder)
            for image_file in image_files:
                if image_file.endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(image_folder, image_file)
                    st.image(image_path, caption=image_file, use_column_width=True)
        else:
            st.write("Image folder not found.")
    
    if __name__ == "__main__":
        main()

elif selected == 'AI Course Outcomes and Answer Checking':
    import streamlit as st
    from openai import OpenAI
    import json
    import os
    
    # Set up OpenAI client
    client = OpenAI(api_key='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')
    
    # Function to read file contents
    def read_file_contents(filename):
        with open(filename, 'r') as f:
            contents = f.read()
        return contents
    
    # Function to generate GPT-3 response
    def generate_gpt3_response(text1, text2):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assignment grading assistant. at the beginning of every user input, you will be provided with the answers the teachers want followed by ### indicating that the student answers have started. You shall judge the student answers on a priority basis out of the teacher's sample answers and  for a lower priority, add your own judgement for the correctness of each answer. Each Answer is worth 5 marks. Return only a json output in the following format {\"grades\":{question_number(integer):marks_allotted to the question(integer)},{\"2\":5}}, for example for the marks of first two questions you can output{\"grades\":{\"1\":4},{\"2\":5}} where the first element of the grades is the question number and the value is the marks allotted"},
                {"role": "user", "content": 'Teacher Sample Answers: \n' + text1 + '\n' + '###' + '\n' + 'Student Answers: \n ' + text2},
            ]
        )
        output = response.choices[0].message.content
        return output
    
    # Function to convert JSON to answer
    def json_to_answer(name, json_string):
        data = json.loads(json_string)
        questions = list(data['grades'].keys())
        marks = list(data['grades'].values())
        result = f'Name: {name}\n'
        for i in range(len(questions)):
            result += f'Question No. {i+1}\n'
            result += f'Marks: {marks[i]}\n'
        result += f'Total Marks: {sum(marks)}'
        return result
    
    # Main function for Streamlit app
    def main():
        st.title("Assignment Grading Assistant")
        st.write("Upload the teacher and student files in .txt format")
    
        # File upload
        teacher_file = st.file_uploader("Upload Teacher File", type=['txt'])
        student_file = st.file_uploader("Upload Student File", type=['txt'])
    
        if teacher_file and student_file:
            # Get student name
            student_name = os.path.splitext(os.path.basename(student_file.name))[0]
    
            # Grade button
            if st.button("Grade"):
                # Read file contents
                teacher_text = teacher_file.read().decode('utf-8')
                student_text = student_file.read().decode('utf-8')
    
                # Generate GPT-3 response
                gpt_response = generate_gpt3_response(teacher_text, student_text)
    
                # Convert JSON to answer
                answer = json_to_answer(student_name, gpt_response)
    
                # Display answer
                st.subheader("Grading Result:")
                st.text_area("Result", value=answer, height=400)
    
    # Run the app
    if __name__ == "__main__":
        main()
elif selected == 'Teacher Resources':
    import streamlit as st
    import base64
    import sqlite3
    from openai import OpenAI
    
    
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    
    def create_table_if_not_exists():
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uploaded_pdfs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                data BLOB NOT NULL
            )
        """)
    
    create_table_if_not_exists()
    
    def faq_section():
        st.markdown("<h2 style='color: #ECB159;'>FAQ Section</h2>", unsafe_allow_html=True)
        faq = {
            "How can I effectively engage my students?": "Engaging students can involve various strategies such as using interactive activities, incorporating technology, and providing real-world examples.",
            "What are some tips for classroom management?": "Establishing clear expectations, fostering a positive classroom environment, and implementing consistent discipline strategies can help with classroom management.",
            "How can I differentiate instruction to meet the needs of all learners?": "Differentiation involves tailoring instruction to accommodate the diverse learning needs of students. This can include providing varied learning activities, offering flexible grouping, and adjusting the pace of instruction.",
            "What are some ways to assess student learning?": "Assessment methods can include quizzes, tests, projects, presentations, and discussions. Formative assessment provides ongoing feedback to guide instruction, while summative assessment evaluates student learning at the end of a unit or course.",
            "How can I support student social-emotional development?": "Supporting social-emotional development involves fostering a positive classroom climate, teaching social-emotional skills such as empathy and self-regulation, and providing opportunities for student reflection and expression."
        }
        for question, answer in faq.items():
            with st.expander(question):
                st.write(answer)
    
    def youtube_links_section():
        st.markdown("<h2 style='color: #ECB159;'>YouTube Links for Teachers</h2>", unsafe_allow_html=True)
        st.subheader("Useful YouTube Channels and Videos")
        st.write("1. [Teaching Channel](https://www.youtube.com/user/TeachingChannel)", unsafe_allow_html=True)
        st.write("2. [Edutopia](https://www.youtube.com/user/edutopia)", unsafe_allow_html=True)
        st.write("3. [CrashCourse](https://www.youtube.com/user/crashcourse)", unsafe_allow_html=True)
        st.write("4. [TED-Ed](https://www.youtube.com/user/TEDEducation)", unsafe_allow_html=True)
        st.write("5. [Khan Academy](https://www.youtube.com/user/khanacademy)", unsafe_allow_html=True)
        st.write("6. [National Geographic Education](https://www.youtube.com/user/NatGeoEducation)", unsafe_allow_html=True)
        st.write("7. [PBS LearningMedia](https://www.youtube.com/user/PBSLearningMedia)", unsafe_allow_html=True)
        st.write("8. [SciShow](https://www.youtube.com/user/scishow)", unsafe_allow_html=True)
    
    def chatbot_section():
        client = OpenAI(api_key='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')
        st.markdown("<h2 style='color: #ECB159;'>Teacher Chatbot</h2>", unsafe_allow_html=True)
        st.subheader("Ask Questions and Get Answers")
    
        user_input = st.text_input("You:", "")
        if st.button("Send"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful chat assistant"},
                        {"role": "user", "content": user_input}
                    ]
                )
                chatbot_response = response.choices[0].message.content
                st.text_area("Chatbot:", chatbot_response)
            st.write("Conversation History:")
            st.write(f"User: {user_input}")
            st.write(f"Chatbot: {chatbot_response}")
    
    def upload_pdf_section():
        st.markdown("<h2 style='color: #ECB159;'>Upload PDF</h2>", unsafe_allow_html=True)
        uploaded_files = st.file_uploader("Upload PDF", type=["pdf"], accept_multiple_files=True)
        uploaded_pdfs = {}
    
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                pdf_data = uploaded_file.getvalue()
                filename = uploaded_file.name
                cursor.execute("INSERT INTO uploaded_pdfs (filename, data) VALUES (?, ?)", (filename, pdf_data))
                conn.commit()
    
                uploaded_pdfs[filename] = pdf_data
    
        return uploaded_pdfs
    
    def display_pdf_from_database(pdf_id):
        cursor.execute("SELECT filename, data FROM uploaded_pdfs WHERE id = ?", (pdf_id,))
        filename, pdf_data = cursor.fetchone()
    
        st.markdown(f"<h3 style='color: #ECB159;'>{filename}</h3>", unsafe_allow_html=True)
        st.markdown(f'<embed src="data:application/pdf;base64,{base64.b64encode(pdf_data).decode()}" width="300" height="300" type="application/pdf">', unsafe_allow_html=True)
    
    def useful_docs_section(uploaded_pdfs):
        st.markdown("<h2 style='color: #ECB159;'>Useful Documents for Teachers</h2>", unsafe_allow_html=True)
    
        cursor.execute("SELECT id, filename FROM uploaded_pdfs")
        for pdf_id, filename in cursor.fetchall():
            
            display_pdf_from_database(pdf_id)
    
    def main():
        st.title("Teacher Resources Page")
        st.markdown(
            """
            <style>
                body {
                    background-color: #8CB9BD;
                    color: #ECB159;
                    font-family: Arial, sans-serif;
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #ECB159;
                }
                .stButton:focus {
                    background-color: #B67352;
                    color: #ffffff;
                }
                .stButton:hover {
                    background-color: #B67352;
                    color: #ffffff;
                }
                .st-expander-content {
                    background-color: #ECB159;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        faq_section()
        youtube_links_section()
        chatbot_section()
        uploaded_pdfs = upload_pdf_section()
        useful_docs_section(uploaded_pdfs)
    
        conn.close() 
    
    if __name__ == "__main__":
        main()