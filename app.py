import streamlit as st
from src.scripts.chat.document_loader import limpar_diretorio

if "init" not in st.session_state:
    st.session_state.init = "cache_cleared"
    st.cache_resource.clear()
    limpar_diretorio()


pages = {
    "Menu": [
        st.Page("./page/chat_page.py", title="Chat com assistente"),
        st.Page("./page/upload_page.py", title="Upload"),
        st.Page("./page/analysis_page.py", title="Análise"),
        st.Page("./page/score_page.py", title="Dashboard"),
    ],
    "Recursos": [
         st.Page("./page/about_page.py", title="Sobre"),
         st.Page("./page/criterios_page.py", title="Critérios de Análise"),
         st.Page("./page/gri_page.py", title="Padrão GRI"),
     ]
}

st.logo("./src/img/logo.png", size="large", icon_image="./src/img/icone.png")
pg = st.navigation(pages)
pg.run()