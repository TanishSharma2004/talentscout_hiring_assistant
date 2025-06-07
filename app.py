import streamlit as st
from chatbot import TalentScoutChatbot
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title("TalentScout Hiring Assistant")
st.write("Welcome! I'm here to assist with your application.")

if "chatbot" not in st.session_state:
    st.session_state.chatbot = TalentScoutChatbot()
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Type your response..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    try:
        response = st.session_state.chatbot.get_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    except Exception as e:
        st.error(f"Error: {str(e)}")
