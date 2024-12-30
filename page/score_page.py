import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.scripts.status_application import atualizar_status

status = atualizar_status()

def extrair_notas_por_id(data):
    """
    Extrai as notas de critérios de uma estrutura de dados usando os IDs como chaves principais
    e os nomes dos critérios como chaves para as notas.
    
    Args:
        data (dict): Estrutura de dados contendo os resultados de análise.
    
    Returns:
        dict: Dicionário com IDs dos documentos e notas associadas aos nomes dos critérios.
    """
    dados = {
        item["id"]: {
            criterio["nome_criterio"]: criterio["nota"]
            for criterio in item["data"]["analise"]["criterios"]
        }
        for item in data["resultado_analise"]
    }
    return dados





def plot_analysis_chart(media_criterios):
    fig = go.Figure()
    
    # Barra principal com gradiente
    fig.add_trace(go.Bar(
        x=media_criterios.index,
        y=media_criterios.values,
        text=[f'{val:.2f}' for val in media_criterios.values],
        textposition='outside',
        marker=dict(
            color=media_criterios.values,
            colorscale=[[0, '#e2f5e9'], [1, '#059669']],
            showscale=False
        ),
        hovertemplate='<b>%{x}</b><br>Média: %{y:.2f}<extra></extra>'
    ))

    # Linha de referência
    fig.add_hline(y=4, 
                  line=dict(color='#065f46', dash='dash', width=2),
                  annotation=dict(text="Bom (Nota 4)", 
                                font=dict(color='#065f46')))

    fig.update_layout(
        title=dict(
            text='Média das Notas por Critério',
            font=dict(size=24, color='#1f2937'),
            x=0.5
        ),
        plot_bgcolor='white',
        showlegend=False,
        xaxis=dict(
            title='Critério',
            tickangle=-45,
            gridcolor='#f3f4f6'
        ),
        yaxis=dict(
            title='Média das Notas',
            range=[0, max(media_criterios.values) + 0.5],
            gridcolor='#f3f4f6'
        ),
        hoverlabel=dict(bgcolor='white'),
        margin=dict(t=100, b=100)
    )

    st.plotly_chart(fig, use_container_width=True)

if status.status["analise"]:
    analise = status.status["analise"]
    dados = extrair_notas_por_id(analise)
    df = pd.DataFrame(dados).T
    media_criterios = df.mean(axis=0)
    
    st.markdown("### Score Dashboard")
    plot_analysis_chart(media_criterios)
else:
    st.info("Não há análises prontas")

