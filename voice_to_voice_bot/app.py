import os
import gradio as gr
import torch
from groq import Groq
from gtts import gTTS
import whisper

# Initialize Whisper model
whisper_model = whisper.load_model("base")

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def voice_to_voice_chat(audio):
    # Transcribe audio using Whisper
    result = whisper_model.transcribe(audio)
    user_text = result['text']
    
    # Send transcribed text to Groq LLM
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_text
            }
        ],
        model="llama-3.3-70b-versatile",
        stream=False,
    )
    
    # Get LLM response
    llm_response = chat_completion.choices[0].message.content
    
    # Convert LLM response to speech
    tts = gTTS(text=llm_response, lang='en')
    audio_response_path = "response.mp3"
    tts.save(audio_response_path)
    
    return audio_response_path, llm_response

# Create Gradio interface
iface = gr.Interface(
    fn=voice_to_voice_chat,
    inputs=gr.Audio(sources=["microphone"], type="filepath"),
    outputs=[
        gr.Audio(type="filepath"),
        gr.Textbox(label="LLM Response")
    ],
    title="Voice-to-Voice Chatbot",
    description="Speak to the AI and get a spoken response!"
)

if __name__ == "__main__":
    iface.launch(debug=True)