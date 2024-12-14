import streamlit as st
import os
import threading
from src.scripts.chat.document_loader import *
from streamlit.runtime.scriptrunner import add_script_run_ctx
import time

# Function to run document loading in a background thread
def background_doc_loading(filename=None):
    try:
        load_doc_family_pipeline()
        st.session_state['document_load_status'] = "Completed"
        # Add the document name to session state
        st.session_state.documents=filename
    except Exception as e:
        st.session_state['document_load_status'] = "Error"
        st.session_state['document_load_error'] = str(e)

def start_document_loading(files_name:list):
    # Reset status
    st.session_state['document_load_status'] = "Running"
    # Create and start the thread with Streamlit context
    thread = threading.Thread(target=background_doc_loading, args=(files_name))
    add_script_run_ctx(thread)
    thread.start()

# Initialize session state variables
if "documents" not in st.session_state:
    st.session_state.documents = []

if 'document_load_status' not in st.session_state:
    st.session_state.document_load_status = None

st.title("Faça upload do documento")

uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=['pdf'], accept_multiple_files=False)

if uploaded_file is not None:
    with st.spinner('Uploading file...'):
        save_uploadedfile(uploaded_file)
    
    try:
        start_document_loading([uploaded_file.name])
            
    except ValueError as e:
        st.error("O documento está vazio (não possui caracteres). Por favor, faça um novo upload.")

# Spinner enquanto a thread está rodando
while st.session_state.document_load_status == "Running":
    with st.spinner("Processando documento. Por favor, aguarde..."):
        time.sleep(7)  # Aguarda um segundo antes de recarregar
    #st.rerun()
    
# Check for completed document loading
if st.session_state.document_load_status == "Completed":
    st.success("Documento processado com sucesso!")

# Check for loading errors
if st.session_state.document_load_status == "Error":
    st.error(f"Erro no processamento: {st.session_state.get('document_load_error', 'Erro desconhecido')}")

# Display loaded documents
if st.session_state.documents:
    st.subheader("Lista de documentos na base de dados:")
    st.info(f"Documento {st.session_state.documents} na base de dados")



