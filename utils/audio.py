from gtts import gTTS
import whisper
import tempfile
import os
from openai import OpenAI
import base64
import hashlib
from pathlib import Path

# Initialize Whisper model (you may choose different models like "small", "medium", etc.)
whisper_model = whisper.load_model("base")


def get_cache_path():
    """Create and return cache directory path"""
    cache_dir = Path(".tts_cache")
    cache_dir.mkdir(exist_ok=True)
    return cache_dir


def get_cache_key(text):
    """Generate a unique cache key for the text"""
    return hashlib.md5(text.encode()).hexdigest()


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


def st_play_audio_openai_64(text):
    cache_dir = get_cache_path()
    cache_key = get_cache_key(text)
    cache_file = cache_dir / f"{cache_key}.b64"

    # Check if cached version exists
    if cache_file.exists():
        return cache_file.read_text()

    # If not cached, generate new audio
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

    with open(filepath, "rb") as f:
        data = f.read()
    b64_audio = base64.b64encode(data).decode()
    html_str = f"""
        <audio autoplay controls>
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
    """

    # Cache the result
    cache_file.write_text(html_str)

    # Clean up temp file
    os.unlink(filepath)

    return html_str


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
