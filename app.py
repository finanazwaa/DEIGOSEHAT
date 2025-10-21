import streamlit as st
import requests

st.title("🗺️ Route Assistant Chatbot - Yogyakarta")

# Input field for user query
user_input = st.text_input("Ketik tujuanmu (contoh: Saya mau ke UGM dari Malioboro):")

# Function to send user input to the FastAPI backend
def chatbot_response(user_input):
    url = "http://127.0.0.1:8000/chatbot"  # FastAPI backend URL
    response = requests.post(url, json={"user_input": user_input})
    if response.status_code == 200:
        return response.json().get("response", "Error: No response from backend.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Display the chatbot response
if user_input:
    response = chatbot_response(user_input)
    st.write(response)