import google.generativeai as genai
import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import random

def generate_random_color():
    colors = ["#FFB6C1", "#ADD8E6", "#90EE90", "#FFDAB9", "#E6E6FA", "#FFFACD", "#D3D3D3"]
    return random.choice(colors)

# Fetch API Key securely from environment variables (if using Streamlit secrets, replace this with st.secrets)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Streamlit title and greeting message
st.title('Nadeem Khan Lakhwera (SRDB) Chatbot')
st.subheader("Welcome! Nadeem Khan Lakhwera (SRDB - Sugarcane Research and Development Board) is here to help you with sugarcane farming in Bahawalpur, Punjab, Pakistan!")

# Instructions for users
st.markdown("""
**How to use the chatbot:**
1. Enter your farming-related question.
2. Press **Submit** to get advice and tips related to sugarcane farming.
3. Feel free to ask as many questions as you like!
""")

# Define the prompt template to focus the model on farming-related queries and formal answers
template = """
You are an expert in sugarcane farming from Bahawalpur, Punjab, Pakistan. You work for the Sugarcane Research and Development Board (SRDB). 
You are giving advice to farmers who may not have much formal education. Always keep your answers simple, clear, and formal. 
Your name is Nadeem Khan Lakhwera. Provide helpful, direct, and easy-to-understand advice related to sugarcane farming. 

User's input: {user_input}
"""

# Set up LangChain's conversation prompt and memory system
prompt = PromptTemplate(input_variables=["user_input"], template=template)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize the Gemini Model
model = genai.GenerativeModel('gemini-1.5-flash')

# Custom function to interact with Gemini through LangChain
def get_response_from_gemini(user_input):
    # Prepare prompt with user input
    full_prompt = prompt.format(user_input=user_input)

    # Generate the response using the Gemini model
    response = model.generate_content(full_prompt)
    
    # Return the generated response text
    return response.text

# Initialize session state for conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# UI for Chatbot
st.markdown("""
<style>
.chat-bubble {
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 10px;
    color: black;
    font-size: 16px;
} 
.code-box {
    background-color: #1e1e1e;
    color: #dcdcdc;
    padding: 15px;
    border-radius: 5px;
    font-family: 'Courier New', monospace;
    position: relative;
    margin-bottom: 15px;
    overflow: auto;
    max-height: 300px;
}
.copy-button {
    position: absolute;
    top: 5px;
    right: 5px;
    background-color: #3c3c3c;
    color: #ffffff;
    padding: 5px 10px;
    border: none;
    border-radius: 3px;
    font-size: 12px;
    cursor: pointer;
}
.copy-button:hover {
    background-color: #555555;
}
.copy-button:active {
    background-color: #777777;
}
input[type="text"] {
    border: 1px solid #ccc;
    padding: 10px;
    width: 100%;
    border-radius: 4px;
    box-sizing: border-box;
}

/* Ensure the input box stays fixed at the bottom */
input:focus {
    outline: none;
}

body {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    height: 100vh;
    margin: 0;
}
</style>
<script>
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        const copyButton = event.target;
        copyButton.textContent = 'Copied!';
        setTimeout(() => {
            copyButton.textContent = 'Copy';
        }, 1500);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}
</script>
""", unsafe_allow_html=True)

# Streamlit input field and button
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("Enter your farming-related question:", key="user_input", max_chars=2000)
    submit_button = st.form_submit_button("Submit")

if submit_button:
    if user_input:
        # Get response from the model
        output = get_response_from_gemini(user_input)

        # Store user input and model response in conversation history
        st.session_state.conversation_history.append({"user": user_input, "response": output})
    else:
        st.warning("Please enter a question before submitting.")

# Display conversation history
if st.session_state.conversation_history:
    for message in st.session_state.conversation_history:
        user_color = generate_random_color()
        bot_color = generate_random_color()

        st.markdown(f'<div class="chat-bubble" style="background-color: {user_color};"><strong>You:</strong> 😀 {message["user"]}</div>', unsafe_allow_html=True)
        if "```" in message["response"]:  # Code Output
            clean_code = message["response"].replace("```", "").strip()
            st.markdown(f'<div class="code-box"><button class="copy-button" onclick="copyToClipboard(`{clean_code.replace("\\", "\\\\").replace("`", "\\`")}`)">Copy</button>{clean_code}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble" style="background-color: {bot_color};"><strong>Nadeem Khan Lakhwera:</strong> 🤖 {message["response"]}</div>', unsafe_allow_html=True)

# Reset button to clear conversation history
if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.experimental_rerun()
