import streamlit as st

class status_aplicacao:
    def __init__(self,):
        self.status = {"analise":None,
                        "documento":None}
    def atualizar(self, analise=None,documento=None):
        if analise:
            self.status["analise"] = {"status_analise":"Completed","resultado_analise": analise}
        if documento:
            self.status["documento"] = {"document_upload":"Completed", "nomes_documentos":documento}  
        return self.status 

@st.cache_resource()
def status()->dict:
    status = status_aplicacao()
    return status

def atualizar_status(analise=None,documento=None):
    """Atualiza dicionário de status em cache"""
    stats = status()
    if analise:
        stats.atualizar(analise=analise)
    if documento:
        stats.atualizar(documento=documento)
    return stats