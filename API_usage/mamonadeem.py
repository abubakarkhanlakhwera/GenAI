import google.generativeai as genai
import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import random

# Generate random pastel colors for user interface elements
def generate_random_color():
    colors = ["#FFB6C1", "#ADD8E6", "#90EE90", "#FFDAB9", "#E6E6FA", "#FFFACD", "#D3D3D3"]
    return random.choice(colors)

# Fetch API Key securely from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Streamlit title and instructions
st.title('Nadeem Khan Lakhwera (SRDB) Chatbot')
st.subheader("Welcome! Get expert advice on sugarcane farming from Bahawalpur, Punjab, Pakistan.")

st.markdown("""
**How to use the chatbot:**
1. Enter your farming-related question.
2. Press **Submit** to get advice.
3. Ask as many questions as you like!
""")

# Define prompt template for focused farming advice
template = """
You are an expert in sugarcane farming from Bahawalpur, Punjab, Pakistan. You work for the Sugarcane Research and Development Board (SRDB). 
Provide clear, formal, and easy-to-understand advice about sugarcane farming. 

User's input: {user_input}
"""

# Set up LangChain's conversation memory
prompt = PromptTemplate(input_variables=["user_input"], template=template)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize the Gemini Model
model = genai.GenerativeModel('gemini-1.5-flash')

# Check if user input is farming-related
def is_farming_related(user_input):
    keywords = ["sugarcane", "farming", "agriculture", "crops", "irrigation", "fertilizer", "pests", "harvesting", "soil", "planting", "yield"]
    return any(keyword in user_input.lower() for keyword in keywords)

# Get response from Gemini
def get_response(user_input):
    if not is_farming_related(user_input):
        return "I'm sorry, I can only answer farming-related questions. Please ask about sugarcane farming."
    
    full_prompt = prompt.format(user_input=user_input)
    response = model.generate_content(full_prompt)
    return response.text

# Session state for conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# UI for Chatbot input and display
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("Enter your farming-related question:", key="user_input", max_chars=2000)
    submit_button = st.form_submit_button("Submit")

if submit_button:
    if user_input:
        output = get_response(user_input)
        st.session_state.conversation_history.append({"user": user_input, "response": output})
    else:
        st.warning("Please enter a question before submitting.")

# Display conversation history
for message in st.session_state.conversation_history:
    user_color = generate_random_color()
    bot_color = generate_random_color()

    st.markdown(f'<div class="chat-bubble" style="background-color: {user_color};"><strong>You:</strong> {message["user"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-bubble" style="background-color: {bot_color};"><strong>Nadeem Khan Lakhwera:</strong> {message["response"]}</div>', unsafe_allow_html=True)

# Clear conversation history
if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.experimental_rerun()

# UI enhancements
st.markdown("""
<style>
.chat-bubble {
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 10px;
    font-size: 16px;
} 
input[type="text"] {
    border: 1px solid #ccc;
    padding: 10px;
    width: 100%;
    border-radius: 4px;
    box-sizing: border-box;
}
</style>
""", unsafe_allow_html=True)