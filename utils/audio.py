from gtts import gTTS
import whisper
import tempfile
import os
from openai import OpenAI

# Initialize Whisper model (you may choose different models like "small", "medium", etc.)
whisper_model = whisper.load_model("base")


def st_play_audio(text):
    """Save tts audio and return to streamlit frontend"""
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        audio_path = fp.name
        tts.save(audio_path)
    return audio_path


def st_play_audio_openai(text):
    client = OpenAI()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        filepath = temp_file.name
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=f"{text}"
        )
        with open(filepath, 'wb') as f:
            for chunk in response.iter_bytes():
                f.write(chunk)
    return filepath


def st_transcribe_audio(filename):
    if not os.path.exists(filename):
        print(f"Error: {
              filename} not found. Please ensure the recording was saved correctly.")
        return ""
    try:
        whisper_stt = whisper_model.transcribe(filename, language='en')
        return whisper_stt
    except FileNotFoundError:
        print("Audio file not found. Please ensure recording is working.")
        return ""
