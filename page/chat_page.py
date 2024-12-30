
import streamlit as st
import time
from src.scripts.chat.chat_rag import Bot

st.html(
    '''
        <style>
            div[aria-label="dialog"]>button[aria-label="Close"] {
                display: none;
            }
            .st-emotion-cache-ocqkz7{
                position: sticky;
                top: 3.75rem; 
                // width: 50%; 
                z-index:999991; 
                background-color: white;}
        </style>
    '''
)


# Streamed response emulator
def response_generator(response):
    time.sleep(0.03)
    for word in response.split(" "):
        yield word+ " "
        time.sleep(0.05)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "issues" not in st.session_state:
    st.session_state.issues = []

bot = Bot()

with st.container():
    col1, col2 = st.columns([0.8,0.2])
    with col1:
        #st.title("Assistente ESG")
        st.markdown("## Assistente ESG")
    with col2:
        if st.button(":gear:",use_container_width=True):
            pass


@st.fragment
def atualizar_chat(chat_container,prompt=None):
    with chat_container:
        if not prompt:
            pass
            #initial_message = st.chat_message("assistant")
            #initial_message.write("Olá, como posso ajudá-lo hoje?")
        messages = st.session_state.messages

        for i in range(0,len(messages)):
            message = messages[i]       
                                
            if message['role'] == "assistant":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            else:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])    

        if prompt:
            with st.chat_message("assistant"):
                with st.spinner(''):
                    response=bot.chat(prompt)
                st.write_stream(response_generator(response))

            st.session_state.messages.append({"role": "assistant", "content": response})

chat_container = st.container(height=400,border=False)
atualizar_chat(chat_container)

if prompt:= st.chat_input("Faça uma pergunta", key="user_input"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    atualizar_chat(chat_container,prompt)

