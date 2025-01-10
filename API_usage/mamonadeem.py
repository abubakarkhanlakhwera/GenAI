import google.generativeai as genai
import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

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

# Initialize the Gemini Model
model = genai.GenerativeModel('gemini-1.5-flash')

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

# Streamlit input field and button
user_input = st.text_input("Enter your farming-related question:")

# Submit button
if st.button("Submit"):
    if user_input:
        # Get response from the model
        output = get_response_from_gemini(user_input)
        
        # Store user input and model response in conversation history
        st.session_state.conversation_history.append({"user": user_input, "response": output})
        st.text_input("Enter your farming-related question:", key="user_input")  # Reset the input field
    
    else:
        st.warning("Please enter a question before submitting.")

# Display conversation history
if st.session_state.conversation_history:
    for message in st.session_state.conversation_history:
        st.markdown(f"**You:** {message['user']}")
        st.markdown(f"**Nadeem Khan Lakhwera:** {message['response']}")
        
# Reset button to clear conversation history
if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.experimental_rerun()  # Rerun to clear the history from the UI
