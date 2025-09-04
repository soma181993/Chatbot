import streamlit as st
import requests
import uuid

st.title("HR Assistant 🤖")

# Create a unique user_id for each session
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]
    st.session_state.user_name = "Soma"  # Or prompt user for name

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input box
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Call Flask API
    resp = requests.post("http://127.0.0.1:5000/get_response", json={"input_text": prompt})

    try:
        data = resp.json()
        reply = data.get("response", "⚠️ No response from server")
    except requests.exceptions.JSONDecodeError:
        st.error(f"Invalid JSON from server: {resp.text}")
        reply = "⚠️ Error: Server returned invalid response."

    # Store assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
