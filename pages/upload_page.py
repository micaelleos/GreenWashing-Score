import streamlit as st
import os
from src.scripts.chat.document_loader import *

st.title("Faça upload do documento")

uploaded_file = st.file_uploader("Escolha um arquivo PDF",type=['pdf'],accept_multiple_files=False)

if uploaded_file is not None:
    with st.spinner('Uploading file...'):
        save_uploadedfile(uploaded_file)
    try:
        with st.spinner('Preprocessing file...'):
            load_doc_pipeline()
        st.success("Docmuent loaded!")

    except ValueError as e:
        st.error("O documento está vazio (não possui caracteres). Por favor, faça um novo upload.")
    



