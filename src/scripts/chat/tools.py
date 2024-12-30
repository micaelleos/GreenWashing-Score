from src.scripts.chat.document_loader import tools
from langchain_core.tools import tool
import uuid
import streamlit as st
from pydantic import BaseModel, Field
from streamlit.runtime.scriptrunner import add_script_run_ctx
from src.scripts.status_application import status, atualizar_status

@tool
def status_da_aplicacao():
    """
    Recupera o status atual da aplicação. A aplicação pode ter um documento carregado ou não, pode ter uma análise pronta ou não. Consulte a existência de documentos na base de dados, além de análises prontas, por essa ferramenta. Utilize essa ferramenta também para verificar o resultado da análise.
    """
    #try:
    status = atualizar_status()
    print(status.status)
    return status.status
    #except:
    #    return "Erro ao recuperar o status da aplicação"
    
tools_esg_agent = [tools[0],status_da_aplicacao]