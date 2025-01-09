import os 
import google.generativeai as genai
import streamlit as st

GOOGLE_API_KEY = os.environ.get('google_api_key')
genai.configure(api_key=GOOGLE_API_KEY)
st.title('Nadeem khan lakhwera(SRDB) Chatbot')
# Model Initiate

model = genai.GenerativeModel('gemini-1.5-flash')

def getResponseFromModel(user_input):
    response = model.generate_content(user_input)
    return response.text
user_input = input("Enter your prompt: ")
output = getResponseFromModel(user_input)
print(output)