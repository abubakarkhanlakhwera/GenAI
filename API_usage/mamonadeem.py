import google.generativeai as genai
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Fetch API Key securely from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Streamlit title and greeting message
st.title('Nadeem Khan Lakhwera (SRDB) Chatbot')
st.subheader("Nadeem Khan Lakhwera (SRDB - Sugarcane Research and Development Board) is here to help you with sugarcane farming in Bahawalpur, Punjab, Pakistan!")

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

# Streamlit input field to get user questions
user_input = st.text_input("Enter your farming-related question:")

# Display
