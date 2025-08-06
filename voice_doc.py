
import os
import subprocess
import platform
from gtts import gTTS
from pydub import AudioSegment

def text_to_speech_with_gtts(input_text, mp3_filepath, wav_filepath=None):
    try:
        # Step 1: Convert text to MP3
        audio = gTTS(text=input_text, lang="en", slow=False)
        audio.save(mp3_filepath)
        print(f"Audio saved successfully as '{mp3_filepath}'")

        os_name = platform.system()

        # Step 2: Windows requires WAV format
        if os_name == "Windows":
            if wav_filepath is None:
                wav_filepath = mp3_filepath.replace(".mp3", ".wav")

            # Convert MP3 to WAV
            sound = AudioSegment.from_mp3(mp3_filepath)
            sound.export(wav_filepath, format="wav")

            # Play WAV using PowerShell
            subprocess.run([
                "powershell",
                "-c",
                f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'
            ])

        elif os_name == "Darwin":  # macOS
            subprocess.run(["afplay", mp3_filepath])

        elif os_name == "Linux":
            subprocess.run(["aplay", mp3_filepath])  # or mpg123 if needed

        else:
            raise OSError("Unsupported operating system")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_text = "Hey, this is AI docter assistant "
text_to_speech_with_gtts(
    input_text=input_text,
    mp3_filepath="gtts_testing_autoplay.mp3"
)
