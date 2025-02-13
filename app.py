import streamlit as st
import os
import shelve
import google.generativeai as genai

# Configure the Gemini API client
api_key = "gemini_key"  # Replace with your API key
genai.configure(api_key=api_key)

# Create the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 200,  # Limiting to 200 tokens for responses
}

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Start a chat session
chat_session = model.start_chat(history=[])

# Streamlit app setup
st.title("ASK TOM")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# Function to load chat history
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Function to save chat history
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages   

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar for deleting chat history
with st.sidebar:
    if st.button("Delete chat history"):
        st.session_state.messages = []
        save_chat_history([])

# Display chat history
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Input from user
if prompt := st.chat_input("How can I help?"):
    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    # Send message to the chat session
    response = chat_session.send_message(prompt)

    # Check if the response is valid
    if response and response.text:
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()
            full_response = response.text  # Get the text response
            message_placeholder.markdown(full_response)

            # Append the assistant's message to session state and save history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            save_chat_history(st.session_state.messages)
    else:
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            st.markdown("Sorry, I couldn't generate a response.")
