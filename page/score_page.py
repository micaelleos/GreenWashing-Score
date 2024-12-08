import streamlit as st
from src.scripts.analysis.analiser import GreenAgent
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
    
cols = st.columns([0.5,0.5])
with cols[0]:
    initial_page = st.text_input('Página inicial')
with cols[1]:
    final_page = st.text_input('Página final')


@st.dialog("Mostrar Trecho do Relatório")
def mostrar(item):
    st.write(item)


if "analise" not in st.session_state:
    st.session_state.analise = []

    if st.button("Submit"):
        bot = GreenAgent()
        with st.spinner(text="Fazendo a análise..."):
            result = bot.analizer_page(int(initial_page),int(final_page))
        st.session_state.analise = result

        for doc in st.session_state.analise:
            with st.expander(f"**ID**: {doc['ids']}"):
                st.write(doc)
        

else:
    if st.button("Submit"):
        bot = GreenAgent()
        result = bot.analizer_page(int(initial_page),int(final_page))
        st.session_state.analise = result

    if st.session_state.analise:    
        for doc in st.session_state.analise:
            with st.container(border=True):
                if st.button(f"Ver trecho {doc['ids']}"):
                    mostrar(doc['documents'])
                colsx = st.columns([0.5,0.5])
                with colsx[0]:
                    st.markdown(f"**Documento**:{doc['metadatas']['source']}")
                with colsx[1]:
                    st.markdown(f"**Página**: {doc['metadatas']['page']}")
                for avaliacao in doc["analise"]["criterios"]:
                    with st.expander(f"""**{avaliacao['nome_criterio']}**  
                                     **Nota**: {avaliacao['nota']}"""):
                        st.write(f"**Justificativa**: {avaliacao['justificativa']}")
                        st.write(f"**Recomendação**: {avaliacao['recomendacao']}")
                with st.expander("**Histórico**"):
                    for obj in doc["history"]:
                        with st.container(border=True, height=300):
                            if isinstance(obj,HumanMessage):
                                st.markdown("#### Entrada da análise")
                                st.write(obj.content)
                            elif isinstance(obj,AIMessage):
                                st.markdown("#### Agente")
                                st.write(obj.content)
                                if obj.additional_kwargs:
                                    st.write("**Pesquisas**")
                                    st.write(obj.additional_kwargs)
                            elif isinstance(obj,ToolMessage):
                                st.markdown("#### Resultado de Pesquisa")
                                st.write(obj.content)
                            


