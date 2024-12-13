import streamlit as st
import os
import threading
from src.scripts.chat.document_loader import *
from streamlit.runtime.scriptrunner import add_script_run_ctx

# Function to run document loading in a background thread
def background_doc_loading():
    try:
        load_doc_family_pipeline()
        st.session_state['document_load_status'] = "Completed"
    except Exception as e:
        st.session_state['document_load_status'] = "Error"
        st.session_state['document_load_error'] = str(e)

def start_document_loading():
    # Reset status
    st.session_state['document_load_status'] = "Running"
    
    # Create and start the thread with Streamlit context
    thread = threading.Thread(target=background_doc_loading)
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
        # Start background loading process
        start_document_loading()
        
        # Add the document name to session state
        st.session_state.documents.append(uploaded_file.name)
        
    except ValueError as e:
        st.error("O documento está vazio (não possui caracteres). Por favor, faça um novo upload.")

# Check for completed document loading
if st.session_state.document_load_status == "Completed":
    st.success("Documento processado com sucesso!")

# Check for loading errors
if st.session_state.document_load_status == "Error":
    st.error(f"Erro no processamento: {st.session_state.get('document_load_error', 'Erro desconhecido')}")

# Display loaded documents
if st.session_state.documents:
    st.subheader("Documentos na base de dados:")
    for doc in st.session_state.documents:
        st.info(f"Documento {doc} na base de dados")