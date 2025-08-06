import base64
from groq import Groq
import os

client = Groq(api_key="your api key")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_image_with_query(query, encoded_image, model="meta-llama/llama-4-maverick-17b-128e-instruct"):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                },
            ],
        }
    ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )
    return chat_completion.choices[0].message.content

