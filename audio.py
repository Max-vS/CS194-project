from gtts import gTTS
from playsound import playsound
import whisper
import tempfile
import os
import sounddevice as sd
import wavio

# Initialize Whisper model (you may choose different models like "small", "medium", etc.)
whisper_model = whisper.load_model("base")

def play_audio(text):
    """Convert text to speech and play it."""
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        audio_path = fp.name
        tts.save(audio_path)
    playsound(audio_path)
    os.remove(audio_path)

def record_audio(duration=5, filename="user_response.wav"):
    """Record audio from user and save it to a file."""
    fs = 44100  # Sample rate
    print("Recording audio... (speak your response)")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    wavio.write(filename, audio_data, fs, sampwidth=2)
    print(f"Audio saved at: {filename}")
    return filename

def transcribe_audio(filename="user_response.wav"):
    """Transcribe audio response from user using Whisper."""
    if not os.path.exists(filename):
        print(f"Error: {filename} not found. Please ensure the recording was saved correctly.")
        return ""
    try:
        transcription = whisper_model.transcribe(filename, language = 'en')
        return transcription['text']
    except FileNotFoundError:
        print("Audio file not found. Please ensure recording is working.")
        return ""
