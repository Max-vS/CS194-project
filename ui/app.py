import os
import sys
import tempfile
import streamlit as st
from audiorecorder import audiorecorder

# Configure Python path to allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local imports
from agents.factory import create_agent
from agents.chat import create_group_chat
from agents.agent_configs import AgentType
from utils.audio import st_play_audio_openai, st_transcribe_audio
from config.settings import FOI_OPTIONS

def run_streamlit_app():
    # Configure Streamlit page settings
    st.set_page_config(
        page_title="CasePilot - Case Interview Practice", layout="wide")

    st.title("CasePilot - Case Interview Practice")
    st.markdown("---")

    # Initialize session state with agents and chat manager
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.current_response = ""
        st.session_state.agents = {
            agent_type: create_agent(agent_type) 
            for agent_type in AgentType
        }
        st.session_state.manager = create_group_chat(st.session_state.agents)
        st.session_state.chat_started = False

    # Display industry selection or interview interface
    if not st.session_state.chat_started:
        st.markdown("## Step 1: Industry Selection")
        st.markdown("Select your industry of interest and we'll initiate the interview.")

        foi_option = st.selectbox(
            "Which industry are you preparing your interview for?",
            FOI_OPTIONS,
            index=None,
            placeholder="Select an industry"
        )

        if st.button("Start Interview"):
            st.session_state.chat_started = True
            agents = st.session_state.agents
            agents[AgentType.INIT].initiate_chat(
                st.session_state.manager,
                message=f"Generate a case study context for the {foi_option} industry.",
            )
            st.rerun()
    else:
        st.markdown("## Step 2: Interview in Progress")
        st.markdown("Listen to the questions and record your responses.")

    # Render chat history with audio playback
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message.get("audio_path"):
                st.audio(message["audio_path"])

    # Handle audio recording and response processing
    if st.session_state.chat_started:
        audio = audiorecorder("Click to record your response")

        if len(audio) > 0:
            # Process recorded audio and get AI response
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                audio.export(temp_audio.name, format="wav")

            st.audio(audio.export().read())
            transcription = st_transcribe_audio(temp_audio.name)
            
            if transcription:
                user_message = transcription['text']
                
                # Update chat with user response and AI reply
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_message
                })

                response = st.session_state.manager.send(
                    user_message,
                    st.session_state.agents[AgentType.USER]
                )

                audio_path = st_play_audio_openai(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "audio_path": audio_path
                })

                st.rerun()

if __name__ == "__main__":
    run_streamlit_app()
