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
