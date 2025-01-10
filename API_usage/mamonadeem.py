import google.generativeai as genai
import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import random

# Helper function for generating random pastel colors
def generate_random_color():
    colors = ["#FFB6C1", "#ADD8E6", "#90EE90", "#FFDAB9", "#E6E6FA", "#FFFACD", "#D3D3D3"]
    return random.choice(colors)

# Fetch API Key securely from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Streamlit app title and introduction
st.title('Nadeem Khan Lakhwera Farming Chatbot')
st.markdown("""
Welcome! I am **Nadeem Khan Lakhwera**, specializing in **farming advice** for Punjab, Pakistan. While my expertise is sugarcane farming, I can help with broader agricultural topics too!

**How to use:**
- Enter your farming question.
- Click **Submit** to get advice.
- Keep asking questions for more detailed assistance.
""")

# Define the prompt template for farming-related advice
prompt_template = """
You are an expert in farming from Bahawalpur, Punjab, Pakistan. You work for the Sugarcane Research and Development Board (SRDB) but can provide advice on other types of farming as well.
Keep your responses simple and formal for clarity. Your name is Nadeem Khan Lakhwera.

User's input: {user_input}
"""

prompt = PromptTemplate(input_variables=["user_input"], template=prompt_template)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to check if the input is related to farming
def is_farming_related(user_input):
    farming_keywords = ["farming", "agriculture", "crops", "irrigation", "fertilizer", "pests", "harvesting", "soil", "planting", "yield", "livestock", "climate"]
    return any(keyword in user_input.lower() for keyword in farming_keywords)

# Get model response function
def get_response(user_input):
    if not is_farming_related(user_input):
        return "I'm here to help with farming-related questions. Please ask about agriculture, crops, or related topics!"
    response_prompt = prompt.format(user_input=user_input)
    response = model.generate_content(response_prompt)
    return response.text

# Conversation History Initialization
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Chat UI Layout
st.markdown("""
<style>
.chat-bubble-user {
    background-color: #d1e7dd;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 5px;
    text-align: left;
    color: #0f5132;
    font-size: 16px;
}
.chat-bubble-bot {
    background-color: #e2e3e5;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 5px;
    text-align: left;
    color: #495057;
    font-size: 16px;
}
.input-container {
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: white;
    padding: 10px 0;
}
.chat-container {
    max-height: 70vh;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# User Input and Submit Form
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("Enter your farming-related question:", max_chars=2000)
    submit_button = st.form_submit_button("Submit")

# Handling User Input
if submit_button and user_input:
    response = get_response(user_input)
    st.session_state.conversation_history.append({"user": user_input, "response": response})

# Displaying Conversation History
if st.session_state.conversation_history:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for chat in st.session_state.conversation_history:
        st.markdown(f'<div class="chat-bubble-user"><strong>You:</strong> {chat["user"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-bubble-bot"><strong>Nadeem Khan Lakhwera:</strong> {chat["response"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Clear Conversation Button
if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.experimental_rerun()
