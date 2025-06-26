import os
import pandas as pd
import plotly.express as px

base_dir = os.path.dirname(__file__)
excel_path = os.path.join(base_dir, '..', 'data', 'tables', 'grafico_educ.xlsx')

df = pd.read_excel(excel_path)

paleta = ['#2c3e50', '#34495e', '#4a6b8c', '#5f80a3', '#7f9ebf'] * 5
verde_azulado = ['#2c3e50', '#3e615f', '#4a7760', '#5f9e6e', '#7fbf7f'] * 5

# montando a figura
fig = px.bar(
    df, #dataframe
    x='Tipo de escola',
    y='Quantidade',
    # title='Quantidade de escola por tipo', #titulo do mapa
    color='Tipo de escola', #separa a cor por microbacia
    text='Quantidade', #rotulo nas barras
    color_discrete_sequence= verde_azulado,
)

#montando elementos visuais
fig.update_traces(
    texttemplate='%{text:,}', #separador decimal
    textposition='auto', #mostrar o rotulo acima das barras
    marker_line_width = 0, #remove a borda do mapa
    hovertemplate='<b>Quantidade: </b>%{y:.0f}' + '<extra></extra>'

)

fig.update_layout(
    title_font_size= 222,
    title_font_family='Arial',
    title_x=0.5,
    margin=dict(t=40, b=10, l=40, r=40),
    plot_bgcolor='rgba(0,0,0,0)',  
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial', size=13, color='#2c3e50'),
    xaxis=dict(
        showgrid=False,                        # Oculta as linhas verticais da grade
        tickangle=0                           # Inclina os rótulos do eixo X para melhor leitura
    ),
    yaxis=dict(
        title='Quantidade',                     # Título do eixo Y
        showgrid=True,                         # Mostra linhas horizontais de grade
        gridcolor='lightgray'                  # Cor da grade
    ),
    showlegend=False,                           # Mostra a legenda (pode ser desativado se cada cor já estiver clara no eixo X)
    bargap=0.2                                  # Espaço entre as barras (0 = coladas, 0.5 = bem separadas)
)

saida_html = os.path.join(base_dir, '..', 'pg_panorama', 'grafico_educ.html')
fig.write_html(saida_html, full_html=True, include_plotlyjs='cdn')


