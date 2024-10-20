# ui/app.py

import streamlit as st

# from entrypoint_agent import EntrypointAgent
#from .question_agent import QuestionAgent
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.entrypoint_agent import EntrypointAgent

def run_streamlit_app():
    st.title("AI Interview Coach")

    # Initialize the EntrypointAgent
    entrypoint_agent = EntrypointAgent()

    # Welcome message
    st.write("Welcome to the AI Interview Coach! Let's start by generating a case study.")

    # Button to start the interview
    if st.button("Start Interview"):
        context, questions = entrypoint_agent.start_interview()
        st.write(f"Case Context: {context}")

        # Loop through questions and get user input
        answers = []
        follow_up_question = ""
        for i, question in enumerate(questions):
            user_response = st.text_input(f"Question {i+1}: {question}", "")
            if user_response:
                follow_up = entrypoint_agent.handle_response(user_response)
                if follow_up:
                    follow_up_question = follow_up
                answers.append(user_response)

        # Handle the follow-up question
        if follow_up_question:
            follow_up_response = st.text_input(f"Follow-up: {follow_up_question}", "")
            if follow_up_response:
                answers.append(follow_up_response)

        # If all questions have been answered, provide feedback
        if len(answers) == len(questions):
            feedback = entrypoint_agent.give_feedback()
            st.write("Feedback:")
            for fb in feedback:
                st.write(fb)

if __name__ == "__main__":
    run_streamlit_app()
