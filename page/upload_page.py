import streamlit as st
import os
from src.scripts.chat.document_loader import *

if "documents" not in st.session_state:
    st.session_state.documents = []

st.title("Faça upload do documento")

uploaded_file = st.file_uploader("Escolha um arquivo PDF",type=['pdf'],accept_multiple_files=False)

if uploaded_file is not None:
    with st.spinner('Uploading file...'):
        save_uploadedfile(uploaded_file)
    try:
        with st.spinner('Preprocessing file...'):
            #load_doc_pipeline()
            load_doc_family_pipeline()
        st.success("Docmuent loaded!")
        st.session_state.documents.append(uploaded_file.name)

    except ValueError as e:
        st.error("O documento está vazio (não possui caracteres). Por favor, faça um novo upload.")

if st.session_state.documents:
    for doc in st.session_state.documents:
        st.info(f"Documento {doc} na base de dados")



