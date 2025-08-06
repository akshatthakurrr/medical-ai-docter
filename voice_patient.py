
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import traceback
import os
from groq import Groq


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Audio Recording ---
def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Records audio from the microphone and saves it as an MP3 file.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Ready! Start speaking now...")

            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("🎧 Recording complete.")

            
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            print(f"✅ Audio saved to: {file_path}")

    except Exception as e:
        print("❌ An error occurred during recording:")
        print(e)
        traceback.print_exc()

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    if not GROQ_API_KEY:
        raise EnvironmentError("❌ GROQ_API_KEY environment variable is not set.")

    try:
        client = Groq(api_key=GROQ_API_KEY)
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        return transcription.text

    except Exception as e:
        print("❌ An error occurred during transcription:")
        print(e)
        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("📢 Starting voice capture and transcription...")

    audio_path = "voice_test_patient.mp3"
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    stt_model = "whisper-large-v3"

    record_audio(audio_path, timeout=50, phrase_time_limit=20)

    print("🔁 Sending audio for transcription...")
    result = transcribe_with_groq(stt_model, audio_path, GROQ_API_KEY)

    if result:
        print("📝 Transcription Result:")
        print(result)

    print("✅ Script complete.")
