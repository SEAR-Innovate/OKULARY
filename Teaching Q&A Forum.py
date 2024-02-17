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
