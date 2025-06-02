import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY') or os.getenv('groq_key')

# Validate API key
if not groq_api_key:
    st.error("Please set your GROQ_API_KEY environment variable.")
    st.stop()

# Sidebar for settings
st.sidebar.title("🔧 Settings")
model = st.sidebar.selectbox('Choose Model', ['llama3-8b-8192', 'llama3-70b-8192', 'Gemma-7b-It'])
system_prompt = st.sidebar.text_area('System Prompt (optional)', '')

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# App title
st.title("💬 Chat with Groq")

# Input field for user prompt
user_input = st.text_input("Enter your prompt")

# Initialize chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Generate response on button click
if st.button("Generate"):
    messages = []
    if system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt.strip()})
    messages.append({"role": "user", "content": user_input})

    try:
        chat = client.chat.completions.create(
            model=model,
            messages=messages
        )
        response = chat.choices[0].message.content
        st.session_state.history.append({"user": user_input, "assistant": response})
        st.markdown(f'<div class="response-box"><strong>Assistant:</strong> {response}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")

# Display chat history
st.sidebar.title("📜 History")
for i, entry in enumerate(st.session_state.history):
    if st.sidebar.button(f"Query {i+1}: {entry['user'][:20]}..."):
        st.markdown(f"**You:** {entry['user']}")
        st.markdown(f"**Assistant:** {entry['assistant']}")
