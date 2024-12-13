import streamlit as st
from src.scripts.analysis.analiser import GreenAgent
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx

# Function to run in a separate thread
def long_running_task(initial_page, final_page):
    try:
        bot = GreenAgent()
        result = bot.analizer_page(int(initial_page), int(final_page))
        
        # Use a thread-safe way to update session state
        st.session_state['analise'] = result
        st.session_state['analise_status'] = "Completed"
    except Exception as e:
        st.session_state['analise_status'] = "Error"
        st.session_state['analise_error'] = str(e)

def start_analysis(initial_page, final_page):
    # Reset status and create a new thread
    st.session_state.analise_status = "Running"
    st.session_state.analise = []
    
    # Create and start the thread with Streamlit context
    thread = threading.Thread(target=long_running_task, args=(initial_page, final_page))
    
    # This is the key addition to fix the threading context issue
    add_script_run_ctx(thread)
    thread.start()


st.title('Análise do Documento')
st.write("Escolha as páginas do relatório para serem feitas as análises:")

# Initialize session state variables if they don't exist
if 'analise_status' not in st.session_state:
    st.session_state.analise_status = None

if 'analise' not in st.session_state:
    st.session_state.analise = []

# Input columns for page range
cols = st.columns([0.5, 0.5])
with cols[0]:
    initial_page = st.text_input('Página inicial')
with cols[1]:
    final_page = st.text_input('Página final')

# Submit button
if st.button("Iniciar Análise"):
    start_analysis(initial_page, final_page)

# Progress and results display
if st.session_state.analise_status == "Running":
    st.spinner("Análise em andamento...")
    st.write("Processando análise. Você pode navegar em outras páginas enquanto isso.")

# Check for completed analysis
if st.session_state.analise_status == "Completed":
    st.success("Análise concluída!")
    
    # Display results
    for doc in st.session_state.analise:
        with st.container(border=True):
            # Expandable section for document details
            st.write(f"**Documento ID**: {doc['ids']}")            
            # Metadata display
            colsx = st.columns([0.5, 0.5])
            with colsx[0]:
                st.markdown(f"**Documento**: {doc['metadatas']['source']}")
            with colsx[1]:
                st.markdown(f"**Página**: {doc['metadatas']['page']}")
            
            # Criteria analysis
            st.subheader("Critérios de Análise")
            for avaliacao in doc["analise"]["criterios"]:
                with st.expander(f"""**{avaliacao['nome_criterio']}**  
                                    **Nota**: {avaliacao['nota']}"""):
                    st.write(f"**Justificativa**: {avaliacao['justificativa']}")
                    st.write(f"**Recomendação**: {avaliacao['recomendacao']}")
            
            # Analysis history
            with st.expander("**Histórico de Análise**"):
                for obj in doc["history"]:
                    with st.container(border=True,height=300):
                        if isinstance(obj, HumanMessage):
                            st.markdown("#### Entrada da Análise")
                            st.write(obj.content)
                        elif isinstance(obj, AIMessage):
                            st.markdown("#### Resposta do Agente")
                            st.write(obj.content)
                            if obj.additional_kwargs:
                                st.write("**Pesquisas Adicionais**")
                                st.write(obj.additional_kwargs)
                        elif isinstance(obj, ToolMessage):
                            st.markdown("#### Resultado de Pesquisa")
                            st.write(obj.content)

# Error handling
if st.session_state.analise_status == "Error":
    st.error(f"Erro durante a análise: {st.session_state.get('analise_error', 'Erro desconhecido')}")

