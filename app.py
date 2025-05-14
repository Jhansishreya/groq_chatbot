import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY') or os.getenv('groq_key')

if not groq_api_key:
    st.error("Please set your GROQ_API_KEY environment variable")
    st.stop()

st.sidebar.title('Personalization')

prompt = st.sidebar.title('System Prompt')
model = st.sidebar.selectbox('Model', ['llama3-8b-8192', 'llama3-70b-8192', 'Gemma-7b-It'])
client = Groq(api_key=groq_api_key)


st.title('💬chat with Groq ')

user_input=st.text_input('Enter your prompt')
if "history" not in st.session_state:
    st.session_state.history=[]

if st.button('Generate'):
    chat=client.chat.completions.create(
        model=model,
        messages=[
            
            {"role":"user","content":user_input}
        ]
    )
    response=chat.choices[0].message.content
    st.session_state.history.append({"user":user_input,"assistant":response})
    st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)

st.sidebar.title("History")
for i, entry in enumerate(st.session_state.history):
    if st.sidebar.button(f'Query {i+1}: {entry["query"]}'):
        st.markdown(f'<div class="response-box">{entry["response"]}</div>', unsafe_allow_html=True)
             