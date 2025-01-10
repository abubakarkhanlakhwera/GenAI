import os 
import google.generativeai as genai
import streamlit as st
import random

def generate_random_color():
    colors = ["#FFB6C1", "#ADD8E6", "#90EE90", "#FFDAB9", "#E6E6FA", "#FFFACD", "#D3D3D3"]
    return random.choice(colors)

# Configure Generative AI API
GOOGLE_API_KEY = os.environ.get('google_api_key')
genai.configure(api_key=GOOGLE_API_KEY)

st.title('⭐ Simple Chatbot⭐')
st.write("Powered by Google's Generative AI")

if "history" not in st.session_state:
    st.session_state['history'] = []

# Initialize Model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_chatbot_response(user_input):
    response = model.generate_content(user_input)
    return response.text

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

# Form for Input
with st.form(key='my_form', clear_on_submit=True):
    user_input = st.text_input('', max_chars=2000, key='input_box')
    submit_button = st.form_submit_button('Send')

if submit_button:
    response = get_chatbot_response(user_input)
    st.session_state['history'].append((user_input, response))

# Display conversation history
for user_message, bot_message in st.session_state['history']:
    user_color = generate_random_color()
    bot_color = generate_random_color()

    st.markdown(f'<div class="chat-bubble" style="background-color: {user_color};"><strong>You:</strong> 😀 {user_message}</div>', unsafe_allow_html=True)
    if "```" in bot_message:  # Code Output
        clean_code = bot_message.replace("```", "").strip()
        st.markdown(f'<div class="code-box"><button class="copy-button" onclick="copyToClipboard(`{clean_code.replace("\\", "\\\\").replace("`", "\\`")}`)">Copy</button>{clean_code}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble" style="background-color: {bot_color};"><strong>Bot:</strong> 🤖 {bot_message}</div>', unsafe_allow_html=True)

# Keep input box at the end of the conversation
st.markdown("<script>var inputBox = document.querySelector('[data-baseweb=\"input\"]'); if (inputBox) inputBox.scrollIntoView({ behavior: 'smooth', block: 'end' });</script>", unsafe_allow_html=True)
