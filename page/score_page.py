import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.scripts.status_application import atualizar_status

status = atualizar_status()
if status.status["analise"]:
    st.write(status.status["analise"])
    # Dados de exemplo
    dados = {
        "Documento 1": {"Critério 1": 4, "Critério 2": 5, "Critério 3": 3},
        "Documento 2": {"Critério 1": 2, "Critério 2": 4, "Critério 3": 5},
        "Documento 3": {"Critério 1": 3, "Critério 2": 3, "Critério 3": 2},
    }

    # Transformar os dados em DataFrame
    df = pd.DataFrame(dados).T  # Transpor para que documentos fiquem como linhas

    # Calcular a média para cada critério
    media_criterios = df.mean(axis=0)

    # Exibir a média por critério
    st.subheader("Média das Notas por Critério")

    # Gráfico de barras estilizado com degradê verde
    fig = go.Figure()

    # Adicionar as barras
    fig.add_trace(go.Bar(
        x=media_criterios.index,
        y=media_criterios.values,
        text=media_criterios.values,
        textposition='auto',
        marker=dict(
            color=media_criterios.values,
            colorscale='Greens',  # Degradê em tons de verde
        ),
        name="Média por Critério"
    ))

    # Adicionar linha de referência (Nota 4)
    fig.add_hline(
        y=4,
        line_dash="dash",
        line_color="darkgreen",
        annotation_text="Bom (Nota 4)",
        annotation_position="top right",
    )

    # Configurações do layout
    fig.update_layout(
        title="Média das Notas por Critério",
        xaxis_title="Critério",
        yaxis_title="Média das Notas",
        template="simple_white",
        title_x=0.5,
        font=dict(size=14),
        margin=dict(l=40, r=40, t=50, b=40),
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)
else:
    st.info("Não há analises prontas")