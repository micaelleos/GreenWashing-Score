import streamlit as st

pages = {
    "Menu": [
        st.Page("./page/chat_page.py", title="Chat com assistente"),
        st.Page("./page/upload_page.py", title="Upload"),
        st.Page("./page/score_page.py", title="Análise"),
        st.Page("./page/criterios_page.py", title="Critérios de Análise"),
    ],
    "Recursos": [
         st.Page("./page/about_page.py", title="Sobre"),
     ]
}

st.logo("./src/img/logo.png", size="large", icon_image="./src/img/icone.png")
pg = st.navigation(pages)
pg.run()