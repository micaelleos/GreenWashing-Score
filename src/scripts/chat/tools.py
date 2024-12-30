from src.scripts.chat.document_loader import tools
from langchain_core.tools import tool
import uuid
import streamlit as st
from pydantic import BaseModel, Field
from streamlit.runtime.scriptrunner import add_script_run_ctx

def pegar_status():
    status = {"analise":None,
              "documento":None}
    print(st.session_state)
    try:
        if "analise" in st.session_state: 
            print(st.session_state.status_analise)
            if st.session_state.status_analise == "Completed":
                status["analise"] = {"status_analise":"Completed","resultado_analise": st.session_state['analise']}

        if 'document_load_status' in st.session_state:
            print(st.session_state.document_load_status)
            if st.session_state.document_load_status == "Completed": 
                status["documento"] = {"document_upload":"Completed", "nomes_documentos":st.session_state.documents}   

        print(status)
        
        return status

    except:
        return "Erro ao recuperar o status da aplicação"

@tool
def status_da_aplicacao():
    """
    Recupera o status atual da aplicação. A aplicação pode ter um documento carregado ou não, pode ter uma análise pronta ou não. Consulte a existência de documentos na base de dados, além de análises prontas, por essa ferramenta. Utilize essa ferramenta também para verificar o resultado da análise.
    """
    result = add_script_run_ctx(pegar_status())
    print("teste resultado", result)
    return result
    
tools_esg_agent = [tools[0],status_da_aplicacao]