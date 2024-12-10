# ui/app.py

import asyncio
import streamlit as st
import sys
import os
import time
import keyboard

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.case_context_agent import CaseContextAgent
from agents.question_agent import QuestionAgent
from agents.feedback_agent import FeedbackAgent
from utils.audio import st_play_audio, st_play_audio_openai, record_audio, st_transcribe_audio
from audiorecorder import audiorecorder


def initialize_agents():
    """Initialize all agents and store them in session state."""
    if "case_context_agent" not in st.session_state:
        st.session_state.case_context_agent = CaseContextAgent()
    if "question_agent" not in st.session_state:
        st.session_state.question_agent = QuestionAgent()
    if "feedback_agent" not in st.session_state:
        st.session_state.feedback_agent = FeedbackAgent()
    if "st.session_state.current_question_idx" not in st.session_state:
        st.session_state.current_question_idx = 0
        

def count_down(ts):
    """Non-blocking countdown timer."""
    placeholder = st.empty()  # Create a placeholder for the timer display
    while ts:
        mins, secs = divmod(ts, 60)
        time_now = f"{mins:02d}:{secs:02d}"
        placeholder.header(f"⏳ Time Remaining: {time_now}")
        time.sleep(0.5)
        ts -= 1
        try:
            if keyboard.is_pressed('space'):
                placeholder.write("⏹ Countdown Stopped!")
                break
        except ImportError:
            st.warning("Timer failed")
        time.sleep(0.5)
    if ts == 0:
        placeholder.write("🎉 Time's up!")


def run_streamlit_app():
    st.title("CasePilot, the AI Interview Coach for your case interviews")
    
    # Initialize agents
    initialize_agents()

    # Welcome message
    st.write("Step 1: Select your industry of interest and we'll initiate the interview.")
    
    ### User gets a choice (1. select from field of interest, 2. type a custom field of interest)   
    # initialize visibility settings and foi_option into mem
    foi_option = "Sales"
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
    # button states
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    if "finished_reading" not in st.session_state:
        st.session_state.finished_reading = False
    
    # Checkbox toggles between predefined list and custom input
    custom_inst = st.checkbox("Check to enter a custom industry of interest")
    if custom_inst:
        # If user selects "Other Field of Interest", show a text input for custom field
        foi_option = st.text_input("Type in your field of interest:", placeholder="e.g., Rocketry and Space Exploration (and press Enter)")
    else:
        # Otherwise, show the selectbox with predefined options
        foi_option = st.selectbox(
            "Which industry are you preparing your interview for?",
            (
                "Agriculture", "Arts and Design", "Computer industry", "Construction", 
                "Education", "Energy", "Entertainment", "Food Manufacturing", 
                "Healthcare", "Hospitality industry", "Human Services", 
                "Information technology", "Insurance occupations", "Journalist", 
                "Law", "Marketing and advertising", "Metal fabrication", 
                "Mining", "Real Estate", "Sales", "Telecommunication", 
                "Transportation", "Utilities", "Wholesale trade"
            ),
            index=None,
            placeholder="Sales",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
    st.write("You selected:", foi_option)
    
    # save foi_option to session memory
    st.session_state.foi_option = foi_option

    # start the interview
    if not st.session_state.interview_started:
        if st.button("Start Interview"):
            st.session_state.interview_started = True
            
            st.session_state.context, st.session_state.questions_list, st.session_state.number_of_questions = st.session_state.case_context_agent.generate_case(st.session_state.foi_option)
            st.session_state.questions_audio_dir_list = [0] * st.session_state.number_of_questions      # mem of questions audio file directories
            st.session_state.transcription = [0] * st.session_state.number_of_questions                 # mem of transcriptions of responses
            st.session_state.log = []                                                                   # mem of entire conversation history
            
            # generating TTS (buffering)
            for idx in range(st.session_state.number_of_questions):
                st.session_state.questions_audio_dir_list[idx] = st_play_audio(st.session_state.questions_list[idx]) # use this for testing
                # st.session_state.questions_audio_dir_list[idx] = st_play_audio_openai(st.session_state.questions_list[idx]) # use this for production
                
    # display case context
    if st.session_state.interview_started:
        if "context" in st.session_state:
            st.write("Step 2: Read the following case context and spend the remaining time analyzing the company.")
            st.write(st.session_state.context)

        # structuring time: allow user to plan and analyze the problem
        # timer runs down during this time (no mic required)
        while not ("timer_done" in st.session_state):
            count_down(15 * 60)  # 15-minute timer
            st.session_state.timer_done = True
            
        # Sequentially ask questions (1 through n)
        if st.session_state.current_question_idx < st.session_state.number_of_questions:
            st.session_state.current_q = st.session_state.questions_list[st.session_state.current_question_idx]
            
            # Display question in Expander form
            with st.expander(f"Question {st.session_state.current_question_idx+1}"):
                st.write(f'''{st.session_state.current_q}''')
                
            # TTS current question                       (live TTS generation--slow)
            # question_tts = st_play_audio(st.session_state.questions_list[st.session_state.current_question_idx]) # live tts generation
            # st.audio(f"{question_tts}", format="mp3", autoplay=1)
            #                                            (play TTS from buffer--fast)
            st.audio(f"{st.session_state.questions_audio_dir_list[st.session_state.current_question_idx]}", format="mp3", autoplay=1)
                    
            # Record user response
            audio = audiorecorder(key=f"audio_recorder_{st.session_state.current_question_idx}")
            if len(audio) > 0:
                audio_filepath = f"data/user_response/response_to_question_{st.session_state.current_question_idx+1}.wav"
                st.audio(audio.export().read())  
                audio.export(f"{audio_filepath}", format="wav")
                st.write(f"Your response duration for Question {st.session_state.current_question_idx}: {audio.duration_seconds} seconds")
                
                # STT using Whisper API
                st.session_state.user_response = st_transcribe_audio(audio_filepath)
                st.session_state.transcription[st.session_state.current_question_idx] = st.session_state.user_response
                
                # log conversation
                st.session_state.log.append("Question: ")
                st.session_state.log.append(st.session_state.current_q)
                st.session_state.log.append("User: ")
                st.session_state.log.append(st.session_state.user_response)
                
                st.session_state.followup_idx = 0
                # while follow up questions need to be answered
                while True:
                    # Question Agent determines whether a follow-up is required
                    qa_response = st.session_state.question_agent.evaluate_response(st.session_state.context, st.session_state.current_q, st.session_state.user_response)

                    if qa_response["terminate"]:    
                        st.success("Response accepted. Click to move on to the next question.")
                        st.session_state.current_question_idx += 1 
                    
                    st.session_state.followup_idx += 1
                    st.warning("A follow-up question will be asked for your previous response.")
                    # st.write(f"Follow-up Question: {qa_response['followup_question']}")
                    
                    # TTS current followup question
                    question_tts = st_play_audio(qa_response['followup_question'])
                    st.audio(f"{question_tts}", format="mp3", autoplay=1)
                    
                    # record user response to followup question
                    audio_followup = audiorecorder(key=f"followup_audio_recorder_{st.session_state.current_question_idx}_{st.session_state.followup_idx}")
                    if len(audio_followup) > 0:
                        audio_followup_filepath = f"data/user_response/response_to_question_{st.session_state.current_question_idx+1}_followup_{st.session_state.followup_idx+1}.wav"
                        st.audio(audio_followup.export().read())  
                        audio.export(f"{audio_followup_filepath}", format="wav")
                        st.write(f"Your response duration for Question {st.session_state.current_question_idx}, Followup {st.session_state.followup_idx}: {audio_followup.duration_seconds} seconds")
                        
                        # STT using Whisper API
                        st.session_state.user_followup = st_transcribe_audio(audio_followup_filepath)
                        
                        st.session_state.log.append("Follow up question: ")
                        st.session_state.log.append(qa_response['followup_question'])
                        st.session_state.log.append("User: ")
                        st.session_state.log.append(st.session_state.user_response)
                    break
                st.success("Please move on to the next question.")
                
                if st.session_state.current_question_idx < st.session_state.number_of_questions-1:
                    if st.button("Next Question"):
                        st.session_state.current_question_idx += 1
                if st.session_state.current_question_idx == st.session_state.number_of_questions: 
                    if st.button("Finish Interview"):
                        # Call Feedback agent to analyze interview
                        feedback_text = st.session_state.feedback_agent.provide_feedback(st.session_state.log)
                        # Display feedback in Expander form
                        with st.expander(f"Final feedback"):
                            st.write(f'''{feedback_text}''')


if __name__ == "__main__":
    run_streamlit_app()
