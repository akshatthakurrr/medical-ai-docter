import os
import os
os.environ["GROQ_API_KEY"] = "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"

import gradio as gr
from brain import encode_image, analyze_image_with_query
from voice_patient import transcribe_with_groq
from voice_doc import text_to_speech_with_gtts

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
What's in this image?. Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    # Step 1: Convert speech to text
    speech_text = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    # Step 2: Analyze image + speech query
    if image_filepath:
        encoded_img = encode_image(image_filepath)
        full_query = system_prompt + " " + speech_text
        doctor_response = analyze_image_with_query(
            query=full_query,
            encoded_image=encoded_img,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for analysis."

    # Step 3: Convert doctor response text to speech
    mp3_output = "doctor_response.mp3"
    text_to_speech_with_gtts(
        input_text=doctor_response,
        mp3_filepath=mp3_output
    )

    return speech_text, doctor_response, mp3_output


iface = gr.Interface(
    fn=process_inputs,
    inputs=[
    gr.Audio(type="filepath", label="Record your question"),

        gr.Image(type="filepath", label="Upload medical image")
    ],
    outputs=[
        gr.Textbox(label="Transcribed Speech"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Response (Audio)")
    ],
    title="AI Doctor with Vision and Voice",
    description="Speak your question and upload an image, the AI doctor will analyze and reply."
)

if __name__ == "__main__":
    iface.launch(debug=True)
