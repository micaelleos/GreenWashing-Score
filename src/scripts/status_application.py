import streamlit as st

@st.cache_resource()
def status():
    status = {"analise":None,
            "documento":None}
    return status