import streamlit as st
from src.scripts.analysis.criteria import criterios


st.markdown("### Critérios de Analise")
st.write("Abaixo seguem os critérios de análise do documento. Para cada um desses critérios, o agente pontua uma nota entre 0 a 5:")
st.write(criterios)