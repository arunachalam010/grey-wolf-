import streamlit as st
import requests

st.set_page_config(page_title="DeepSeek R1 Chatbot", layout="wide")

st.title("🧠 DeepSeek R1 Chatbot")

# Check model status
status_response = requests.get("http://127.0.0.1:8000/status")
status = status_response.json().get("status", "offline")

# Display status
st.markdown(f"**Model Status: {'🟢 Online' if status == 'online' else '🔴 Offline'}**")

# Toggle button
if st.button("🔄 Toggle Model Online/Offline"):
    toggle_response = requests.post("http://127.0.0.1:8000/toggle")
    status = toggle_response.json().get("status", "offline")
    st.experimental_rerun()  # Refresh UI

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Type a message...")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send chat history to FastAPI
    chat_history = [msg["content"] for msg in st.session_state.messages]
    response = requests.post("http://127.0.0.1:8000/generate", json={"chat_history": chat_history})
    bot_reply = response.json().get("response", "Error generating response.")

    # Display bot message
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # Save bot response in chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

