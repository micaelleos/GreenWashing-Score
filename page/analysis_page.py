import streamlit as st
from src.scripts.analysis.analiser import GreenAgent
from src.scripts.status_application import atualizar_status
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx
import time

@st.dialog("Trecho do Relatório")
def mostrar(item,id,pg):
    st.write(f"**ID do trecho: {id}**")
    st.write(f"**Página: {pg}**")
    st.write(item)

# Function to run in a separate thread
def long_running_task(initial_page, final_page):
    #try:
    bot = GreenAgent()
    result = bot.analizer_page(int(initial_page), int(final_page))
    print(bot.cost)
    # Use a thread-safe way to update session state
    st.session_state['analise'] = result
    st.session_state['analise_status'] = "Completed"
    # except Exception as e:
    #      st.session_state['analise_status'] = "Error"
    #      st.session_state['analise_error'] = str(e)

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

status = atualizar_status()
# Submit button
if st.button("Iniciar Análise"):
    if status.status["documento"]:
        start_analysis(initial_page, final_page)
    else:
        st.info("Não há documentos carregados na base.")

# Progress and results display
while st.session_state.analise_status == "Running":
    with st.spinner("Análise em adamento. Por favor, aguarde..."):
        time.sleep(7)  # Aguarda um segundo antes de recarregar

# Check for completed analysis
if st.session_state.analise_status == "Completed":
    st.success("Análise concluída!")
    result_list =[]
    for doc in st.session_state.analise:
        result = {}
        result['analise'] = doc['analise']
        result['documents'] = doc['documents']
        result['metadata'] = doc['metadata']
        result_list.append({"id":doc["id"], "data": result})
    atualizar_status(analise=result_list)
    
    # Display results
    i=0
    for doc in st.session_state.analise:
        with st.container(border=True):
            i=i+1
            if st.button(f"Ver trecho {i}"):
                mostrar(doc['documents'],doc['id'],doc["metadata"]["page"])        
            # Metadata display
            colsx = st.columns([0.8, 0.2])
            with colsx[0]:
                st.markdown(f"**Documento**: {doc['metadata']['source']}")
            with colsx[1]:
                st.markdown(f"**Página**: {doc['metadata']['page']}")
            
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

