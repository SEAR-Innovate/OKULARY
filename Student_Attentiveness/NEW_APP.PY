import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load the dataset
data = pd.read_csv("./synthetic_data_with_all_subjects.csv")

def mean_scores_subject_gender(subject):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='gender', y=subject + ' score', data=data)
    plt.title(f'Mean {subject} Score by Gender')
    plt.xlabel('Gender')
    plt.ylabel(f'Mean {subject} Score')
    plt.savefig('./requested_plots/mean_scores_subject_gender.png')
    st.pyplot()

def course_and_scores_relations(subject):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='test preparation course', y=subject + ' score', data=data)
    plt.title('Reading Score Distribution by Test Preparation Course')
    plt.xlabel('Test Preparation Course')
    plt.ylabel(f'{subject} Score')
    plt.savefig('./requested_plots/course_and_score_relations.png')
    st.pyplot()

def plot_mean_scores():
    mean_scores = data[['math score', 'reading score', 'writing score', 'physics score', 'computer science score']].mean()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=mean_scores.index, y=mean_scores.values)
    plt.title('Mean Scores for Each Subject')
    plt.xlabel('Subject')
    plt.ylabel('Mean Score')
    plt.xticks(rotation=45)
    plt.savefig('./requested_plots/mean_scores.png')
    st.pyplot()

def plot_median_scores():
    median_scores = data[['math score', 'reading score', 'writing score', 'physics score', 'computer science score']].median()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=median_scores.index, y=median_scores.values)
    plt.title('Median Scores for Each Subject')
    plt.xlabel('Subject')
    plt.ylabel('Median Score')
    plt.xticks(rotation=45)
    plt.savefig('./requested_plots/median_scores.png')
    st.pyplot()

def plot_highest_scores_each_subject():
    plt.figure(figsize=(10, 6))
    highest_scores = data[['math score', 'reading score', 'writing score', 'physics score', 'computer science score']].max()
    sns.barplot(x=highest_scores.index, y=highest_scores.values)
    plt.title('Highest Scores for Each Subject')
    plt.xlabel('Subject')
    plt.ylabel('Highest Score')
    plt.xticks(rotation=45)
    plt.savefig('./requested_plots/highest_scores.png')
    st.pyplot()

def plot_lowest_scores_each_subject():
    plt.figure(figsize=(10, 6))
    lowest_scores = data[['math score', 'reading score', 'writing score', 'physics score', 'computer science score']].min()
    sns.barplot(x=lowest_scores.index, y=lowest_scores.values)
    plt.title('Lowest Scores for Each Subject')
    plt.xlabel('Subject')
    plt.ylabel('Lowest Score')
    plt.xticks(rotation=45)
    plt.savefig('./requested_plots/lowest_scores.png')
    st.pyplot()

def plot_scores_individual(name):
    student_data = data[data['name'] == name]
    if len(student_data) == 0:
        print("Student not found.")
        return

    subjects = ['math score', 'reading score', 'writing score', 'physics score', 'computer science score']
    scores = [student_data[subject].values[0] for subject in subjects]

    plt.figure(figsize=(10, 6))
    plt.bar(subjects, scores, color=['blue', 'green', 'red', 'orange', 'purple'])
    plt.title(f'Scores for {name}')
    plt.xlabel('Subjects')
    plt.ylabel('Scores')
    plt.ylim(0, 100)  # Assuming scores are out of 100
    plt.savefig('./requested_plots/individual_scores.png')
    st.pyplot()

def plot_individual_semester_line(subjects,exam_scores):
    plt.figure(figsize=(10, 6))
    for subject in subjects:
        sns.lineplot(x='Semester', y=subject, data=exam_scores, label=subject)
    plt.title('Exam Scores Over Semesters')
    plt.xlabel('Semester')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.savefig('./requested_plots/line_plot.png')
    st.pyplot()

def plot_individual_semester_box(exam_scores):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=exam_scores.drop('Semester', axis=1))
    plt.title('Distribution of Exam Scores for Each Subject')
    plt.xlabel('Subject')
    plt.ylabel('Score')
    plt.savefig('./requested_plots/box_plot.png')
    st.pyplot()

def increase_decrease(subjects,exam_scores):
    for subject in subjects:
        exam_scores_diff = exam_scores[[subject]].diff()

        # Find semester with most improvement and decline
        most_improved_semester = exam_scores_diff.idxmax()[0]
        most_declined_semester = exam_scores_diff.idxmin()[0]

        print(f"For {subject}:")
        print(f"Most Improvement: Semester {most_improved_semester}, Score Increase: {exam_scores_diff.loc[most_improved_semester][0]}")
        print(f"Quality Decline: Semester {most_declined_semester}, Score Decrease: {exam_scores_diff.loc[most_declined_semester][0]}\n")

def default_dashboard_class():
    remove_files_in_directory('./requested_plots')
    data = pd.read_csv("synthetic_data_with_all_subjects.csv")
    subject = str(input('enter subject:'))
    mean_scores_subject_gender(subject)
    course_and_scores_relations(subject)
    plot_mean_scores()
    plot_median_scores()
    plot_highest_scores_each_subject()
    plot_highest_scores_each_subject()
    
def default_dashboard_student(name:str, subjects = ['maths', 'computer science', 'reading', 'writing', 'physics']):
    remove_files_in_directory('./requested_plots')
    exam_scores = pd.read_csv(f"{name}.csv")
    plot_scores_individual(name,exam_scores)
    plot_individual_semester_line(subjects,exam_scores)
    plot_individual_semester_box(exam_scores)
    increase_decrease(subjects,exam_scores)
    
def plot_dashboard_class(selected_options:list,subject:str):
    remove_files_in_directory('./requested_plots')
    data = pd.read_csv("synthetic_data_with_all_subjects.csv")
    option_to_function = {
    "Scores with respect to gender": (mean_scores_subject_gender,(subject,)),
    "Impact of course completion on grades": (course_and_scores_relations,(subject,)),
    "Mean Scores": (plot_mean_scores,()),
    "Median Scores": (plot_median_scores,()),
    "Highest Scores": (plot_highest_scores_each_subject,()),
    "Lowest Scores": (plot_lowest_scores_each_subject,()),
    }
    for option in selected_options:
        function, params = option_to_function.get(option)
        if function:
           function(*params)

def plot_dashboard_student(selected_options:list,name:str,subjects:list):
    remove_files_in_directory('./requested_plots/')
    exam_scores = pd.read_csv(f"{name}.csv")
    option_to_function = {
    "Plot Scores for the student": (plot_scores_individual,(name,exam_scores)),
    "Plot Individual Semester Progress(Line Plot)": (plot_individual_semester_line,(subjects,exam_scores)),
    "Plot Individual Semester Progress (Box Plot)": (plot_individual_semester_box,(exam_scores)),
    "Improvements and Decline of Marks": (increase_decrease,(subjects,exam_scores)),
    }
    for option in selected_options:
        function, params = option_to_function.get(option)
        if function:
           function(*params)
def remove_files_in_directory(directory):
    # Get the list of files in the directory
    files = os.listdir(directory)
    
    # Iterate over each file and remove it
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
           
plot_dashboard_class(['Scores with respect to gender','Highest Scores'],'maths')
