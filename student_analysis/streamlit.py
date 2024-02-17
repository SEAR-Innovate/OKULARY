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
        image_folder = './requested_plots/'
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
    image_folder = "./requested_plots"
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
