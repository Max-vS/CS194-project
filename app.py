from config.settings import FOI_OPTIONS
from utils.audio import st_play_audio, st_play_audio_openai, st_transcribe_audio
from agents.agent_configs import AgentType
from agents.groupchat import create_group_chat
from agents.factory import create_agent
import os
import sys
import tempfile
from time import sleep
import streamlit as st
from audiorecorder import audiorecorder

# Configure Python path to allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local imports


def initialize_session_state():
    """Initialize all required session state variables if they don't exist"""
    if not hasattr(st.session_state, 'initialized'):
        st.session_state.agents = {
            agent_type: create_agent(agent_type)
            for agent_type in AgentType
        }
        st.session_state.manager = create_group_chat(st.session_state.agents)
        st.session_state.status = None
        st.session_state.foi = None
        st.session_state.chat_history = None
        st.session_state.audio_responses = []
        st.session_state.current_audio = None
        st.session_state.initialized = True


def run_streamlit_app():
    # Configure Streamlit page settings
    st.set_page_config(
        page_title="CasePilot - Case Interview Practice", layout="wide")

    st.title("CasePilot - Case Interview Practice")
    st.markdown("---")

    # Initialize session state
    initialize_session_state()

    # Display industry selection or interview interface
    if not st.session_state.status:
        st.markdown("## Step 1: Industry Selection")
        st.markdown(
            "Select your industry of interest and we'll initiate the interview.")

        foi_option = st.selectbox(
            "Which industry are you preparing your interview for?",
            FOI_OPTIONS,
            index=None,
            placeholder="Select an industry"
        )

        if st.button("Start Interview"):
            if foi_option:
                st.session_state.status = "init"
                st.session_state.foi = foi_option

            st.rerun()

    elif st.session_state.status == "init":
        st.markdown("## Step 2: Generate Case Study")

        # Add a loading spinner in the center of the screen
        with st.spinner('Generating your case study... Please wait.'):
            agents = st.session_state.agents
            chat_result = agents[AgentType.INIT].initiate_chat(
                st.session_state.manager,
                message=f"Generate a case study context for the {st.session_state.foi} industry.",
            )

            st.session_state.chat_history = chat_result.chat_history
            st.session_state.status = "chat"

            st.rerun()

    elif st.session_state.status == "chat":
        st.markdown("## Step 3: Interview in Progress")
        st.markdown("Listen to the questions and record your responses.")

        user_audio_num = 0

        # Display chat history
        for message in st.session_state.chat_history:

            if message["name"] == "chat_manager":

                with st.chat_message("user"):
                    st.write(message["content"])
                    st.audio(st.session_state.audio_responses[user_audio_num])
                    user_audio_num += 1

            else:

                with st.chat_message("assistant"):
                    st.write(message["content"])

                    # Add TTS only for messages starting with QUESTION or FOLLOWUP
                    if (
                        message["content"].startswith("QUESTION") or
                        message["content"].startswith("FOLLOW-UP")
                    ):
                        question_tts = st_play_audio(message["content"])
                        st.audio(question_tts, format="mp3", autoplay=1)

                    if message["name"] == "feedback_agent":
                        st.session_state.status = "feedback"

        if st.session_state.status != "feedback":
            with st.chat_message("user"):

                audio = audiorecorder("Click to record your response")

                # Process recorded audio and get AI response
                if len(audio) > 0 and audio != st.session_state.current_audio:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                        audio.export(temp_audio.name, format="wav")
                        st.session_state.audio_responses.append(
                            audio.export().read())

                    st.session_state.current_audio = audio

                    st.audio(st.session_state.audio_responses[-1])

                    st.markdown("#### Transcription")

                    with st.spinner('Transcribing...'):
                        transcription = st_transcribe_audio(
                            temp_audio.name)["text"]
                        st.write(transcription)

                        chat_result = st.session_state.manager.initiate_chat(
                            recipient=st.session_state.agents[AgentType.QA],
                            message=transcription,
                            clear_history=False
                        )
                        st.session_state.chat_history = chat_result.chat_history

                        st.rerun()


if __name__ == "__main__":
    run_streamlit_app()
