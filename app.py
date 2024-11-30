import streamlit as st

pages = {
    "Menu": [
        st.Page("./pages/chat_page.py", title="Chat com assistente"),
        st.Page("./pages/upload_page.py", title="Upload"),
        st.Page("./pages/score_page.py", title="Score"),
    ],
    "Recursos": [
         st.Page("./pages/about_page.py", title="About"),
     ]
}

st.logo("./src/img/logo.png", size="large") # icon_image="./src/img/jira_logo.png"
pg = st.navigation(pages)
pg.run()