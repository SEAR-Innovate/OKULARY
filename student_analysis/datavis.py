# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv("synthetic_data_with_all_subjects.csv")  # Replace "your_dataset.csv" with the path to your dataset file

# Display the first few rows of the dataset
data.head()

# %%
# Bar plot of mean scores by gender
plt.figure(figsize=(10, 6))
sns.barplot(x='gender', y='math score', data=data)
plt.title('Mean Math Score by Gender')
plt.xlabel('Gender')
plt.ylabel('Mean Math Score')
plt.show()

# %%
# Box plot of scores distribution by test preparation course
plt.figure(figsize=(10, 6))
sns.boxplot(x='test preparation course', y='reading score', data=data)
plt.title('Reading Score Distribution by Test Preparation Course')
plt.xlabel('Test Preparation Course')
plt.ylabel('Reading Score')
plt.show()

# %%
# Violin plot of writing scores by parental level of education
plt.figure(figsize=(12, 8))
sns.violinplot(x='parental level of education', y='writing score', data=data)
plt.title('Writing Score Distribution by Parental Level of Education')
plt.xlabel('Parental Level of Education')
plt.ylabel('Writing Score')
plt.xticks(rotation=45)
plt.show()

# %%
# Pair plot of all scores
sns.pairplot(data[['math score', 'reading score', 'writing score', 'physics score', 'computer science score']])
plt.show()


# %%
mean_scores = data[['math score', 'reading score', 'writing score', 'physics score', 'computer science score']].mean()
median_scores = data[['math score', 'reading score', 'writing score', 'physics score', 'computer science score']].median()

# Plot mean scores

# %%
plt.figure(figsize=(10, 6))
sns.barplot(x=mean_scores.index, y=mean_scores.values)
plt.title('Mean Scores for Each Subject')
plt.xlabel('Subject')
plt.ylabel('Mean Score')
plt.xticks(rotation=45)
plt.show()

# %%
plt.figure(figsize=(10, 6))
sns.barplot(x=median_scores.index, y=median_scores.values)
plt.title('Median Scores for Each Subject')
plt.xlabel('Subject')
plt.ylabel('Median Score')
plt.xticks(rotation=45)
plt.show()



# %%
highest_scores = data[['math score', 'reading score', 'writing score', 'physics score', 'computer science score']].max()
lowest_scores = data[['math score', 'reading score', 'writing score', 'physics score', 'computer science score']].min()


# %%
plt.figure(figsize=(10, 6))
sns.barplot(x=highest_scores.index, y=highest_scores.values)
plt.title('Highest Scores for Each Subject')
plt.xlabel('Subject')
plt.ylabel('Highest Score')
plt.xticks(rotation=45)
plt.show()

# %%
plt.figure(figsize=(10, 6))
sns.barplot(x=lowest_scores.index, y=lowest_scores.values)
plt.title('Lowest Scores for Each Subject')
plt.xlabel('Subject')
plt.ylabel('Lowest Score')
plt.xticks(rotation=45)
plt.show()

# %%
highest_scorers = data[['math score', 'reading score', 'writing score', 'physics score', 'computer science score']].idxmax(axis=0)

# Plot highest scorers
plt.figure(figsize=(10, 6))
sns.countplot(highest_scorers)
plt.title('Highest Scorer in Each Subject')
plt.xlabel('Subject')
plt.ylabel('Number of Students')
plt.xticks(rotation=45)
plt.show()

# %% [markdown]
# ### STUDENT INDIVIDUAL DATA VSI

# %%
student_data = data.iloc[0]

# Plot individual student performance
plt.figure(figsize=(10, 6))
sns.barplot(x=student_data.index[5:], y=student_data.values[5:])
plt.title('Individual Student Performance')
plt.xlabel('Subject')
plt.ylabel('Score')
plt.xticks(rotation=45)
plt.show()

# %%
sns.pairplot(data.iloc[:1][['math score', 'reading score', 'writing score', 'physics score', 'computer science score']])
plt.show()


# %%
import pandas as pd
import numpy as np

# Generate synthetic data for exam scores
np.random.seed(42)  # for reproducibility

# Number of semesters
num_semesters = 6

# Number of subjects
num_subjects = 5

# Create a DataFrame to store the data
exam_scores = pd.DataFrame(np.random.randint(0, 101, size=(num_semesters, num_subjects)),
                           columns=['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5'])

# Add semester column
exam_scores['Semester'] = range(1, num_semesters + 1)

# Save the data to a CSV file
exam_scores.to_csv("student_exam_scores.csv", index=False)

# Display the first few rows of the dataset
print(exam_scores.head())

# %%
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
exam_scores = pd.read_csv("student_exam_scores.csv")

# Line plot of exam scores over semesters for each subject
plt.figure(figsize=(10, 6))
for subject in ['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5']:
    sns.lineplot(x='Semester', y=subject, data=exam_scores, label=subject)
plt.title('Exam Scores Over Semesters')
plt.xlabel('Semester')
plt.ylabel('Score')
plt.legend()
plt.grid(True)
plt.show()

# Box plot of exam scores distribution for each subject
plt.figure(figsize=(10, 6))
sns.boxplot(data=exam_scores.drop('Semester', axis=1))
plt.title('Distribution of Exam Scores for Each Subject')
plt.xlabel('Subject')
plt.ylabel('Score')
plt.show()


# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
exam_scores = pd.read_csv("student_exam_scores.csv")

# Separate plots for each subject
for subject in ['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5']:
    # Line plot of exam scores over semesters for the subject
    plt.figure(figsize=(8, 5))
    sns.lineplot(x='Semester', y=subject, data=exam_scores)
    plt.title(f'{subject} Exam Scores Over Semesters')
    plt.xlabel('Semester')
    plt.ylabel('Score')
    plt.grid(True)
    plt.show()

    # Calculate difference between consecutive semesters
    exam_scores_diff = exam_scores[[subject]].diff()

    # Find semester with most improvement and decline
    most_improved_semester = exam_scores_diff.idxmax()[0]
    most_declined_semester = exam_scores_diff.idxmin()[0]

    print(f"For {subject}:")
    print(f"Most Improvement: Semester {most_improved_semester}, Score Increase: {exam_scores_diff.loc[most_improved_semester][0]}")
    print(f"Quality Decline: Semester {most_declined_semester}, Score Decrease: {exam_scores_diff.loc[most_declined_semester][0]}\n")



