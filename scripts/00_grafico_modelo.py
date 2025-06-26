import os
import pandas as pd
import plotly.express as px

df = pd.read_excel('../data/tables/grafico_pop_geral.xlsx')

paleta = ['#2c3e50', '#34495e', '#4a6b8c', '#5f80a3', '#7f9ebf'] * 5

# montando a figura
fig = px.bar(
    df, #dataframe
    x='Municipio',
    y='População',
    # title='População por bacia hidrográfica', #titulo do mapa
    color='Municipio', #separa a cor por microbacia
    text='População', #rotulo nas barras
    color_discrete_sequence= paleta,
)

#montando elementos visuais
fig.update_traces(
    texttemplate='%{text:,}', #separador decimal
    textposition='outside', #mostrar o rotulo acima das barras
    marker_line_width = 0, #remove a borda do mapa
)

fig.update_layout(
    title_font_size= 222,
    title_font_family='Arial',
    title_x=0.5,
    margin=dict(t=60, b=80, l=40, r=40),
    plot_bgcolor='rgba(0,0,0,0)',  
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial', size=13, color='#2c3e50'),
    xaxis=dict(
        showgrid=False,                        # Oculta as linhas verticais da grade
        tickangle=45                           # Inclina os rótulos do eixo X para melhor leitura
    ),
    yaxis=dict(
        title='População',                     # Título do eixo Y
        showgrid=True,                         # Mostra linhas horizontais de grade
        gridcolor='lightgray'                  # Cor da grade
    ),
    showlegend=True,                           # Mostra a legenda (pode ser desativado se cada cor já estiver clara no eixo X)
    bargap=0.1                                  # Espaço entre as barras (0 = coladas, 0.5 = bem separadas)
)

fig.write_html('../pg_panorama/grafico_pop_geral.html', full_html=True, include_plotlyjs='cdn')