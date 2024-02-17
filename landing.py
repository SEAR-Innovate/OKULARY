import streamlit as st
from streamlit_option_menu import option_menu

st.markdown("<h1 style='text-align: center;'>OKULARY: Empowering Educators with Innovative Solutions</h1>", unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options= ["Home","Plagerism Checker","AI Class Monitoring","Teacher Community","AI Course Outcomes and Answer Checking","Cheating and Malpractice Detection","Student Performance Tracking","Class Performance Analytics"],
    default_index=0,
    orientation="horizontal",
    styles={
    "container": {"padding": "0!important"},
    "icon": {"color": "orange", "font-size": "12px"}, 
    "nav-link": {"font-size": "10px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "red"},
    }
)

st.markdown('''
Welcome to OKULARY, the ultimate teacher helper website designed to revolutionize the teaching experience. Our platform is built to address the diverse needs of educators by providing a comprehensive suite of resources, teaching methodologies, community support, AI-driven assessments, and performance analytics. 

## **Problem Statement:**

Teaching is a demanding profession that requires educators to juggle multiple responsibilities, from lesson planning and assessment to classroom management and student engagement. With the increasing demands of modern education, teachers often find themselves overwhelmed and in need of support. OKULARY aims to bridge this gap by offering a one-stop solution that empowers educators with the tools and resources they need to excel in their profession.

## **Aim:**

Our aim is to develop an all-encompassing educational platform tailored for teachers, providing comprehensive resources, teaching methodologies, community support, AI-driven assessments, and performance analytics.

## **Objective:**

We aim to create a multifaceted solution that addresses the diverse needs of educators by offering resources, teaching strategies, and a supportive community, while also leveraging AI technology for automated assessment, detection of cheating and malpractice, tracking individual student performance, and providing insightful class analytics. Additionally, we seek to introduce a novel AI class monitoring system that evaluates student attentiveness based on posture and facial expressions, enabling efficient attendance management.

## **Unique Approach:**

What sets our platform apart is its integration of various features essential for effective teaching and classroom management, along with innovative AI capabilities. By combining resources, teaching methodologies, and community support, we foster a holistic environment for educators to enhance their teaching practices. Furthermore, our AI-driven assessment tools not only automate grading but also detect cheating and malpractice, ensuring academic integrity. The inclusion of student performance tracking and class analytics provides valuable insights for educators to tailor their teaching approaches and interventions. Additionally, our pioneering AI class monitoring system introduces a new dimension to classroom management by assessing student engagement and attendance through facial recognition and posture analysis.

## **Key Features:**

1. **Resource Repository:** Access to a vast repository of educational resources.
2. **Teaching Methodologies:** Guidance on effective teaching techniques and methodologies.
3. **Teacher Community:** A supportive online community for collaboration and sharing experiences.
4. **AI Course Outcomes and Answer Checking:** Automated assessment of course outcomes and answer checking using AI.
5. **Cheating and Malpractice Detection:** AI-powered tools to detect cheating and malpractice.
6. **Student Performance Tracking:** Monitoring and tracking individual student performance.
7. **Class Performance Analytics:** Data analytics to analyze class performance trends and patterns.
8. **AI Class Monitoring:** Innovative system to monitor student attentiveness and manage attendance using AI technology.

Through our platform, we aim to revolutionize the teaching experience by providing educators with a comprehensive toolkit for effective teaching, assessment, and classroom management, ultimately enhancing student learning outcomes.

## **Checkpoints:**

- [ ]  Documentation And Resources 
- [ ]  give resources (bh) 
- [ ]  methods to teach (bh) 
- [ ]  teacher community (bh) 
- [ ]  AI course outcomes and answer checking (bh) 
- [ ]  cheating and malpractice detection (bh) 
- [ ]  keep track of each student performance (bh) 
- [ ]  data analytics of class performance. (bh)
- [ ]  AI class monitoring (attentiveness) 

## **Get Started with OKULARY Today!**

Join OKULARY today and take your teaching to the next level. Our platform is designed to empower educators with the tools and resources they need to excel in their profession. Whether you're a seasoned teacher looking for new teaching strategies or a new teacher seeking guidance, OKULARY has something for everyone. Sign up now and start your journey towards becoming a more effective and successful educator.''')
