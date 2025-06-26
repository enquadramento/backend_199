import os
import pandas as pd
import plotly.express as px
from plotly.colors import sample_colorscale

base_dir = os.path.dirname(__file__)
excel_path = os.path.join(base_dir, '..', 'data', 'tables', 'grafico_emp_formais.xlsx')

df = pd.read_excel(excel_path)

greems = sample_colorscale('Greens', [1, 0.8, 0.6, 0.4, 0.2])

greems2 = ['#2e7d32', '#388e3c', '#43a047', '#66bb6a', '#a5d6a7']

verde_azulado = ['#2c3e50', '#3e615f', '#4a7760', '#5f9e6e', '#7fbf7f']

# montando a figura
fig = px.bar(
    df, #dataframe
    x='Profissão',
    y='Percento',
    # title='População por bacia hidrográfica', #titulo do mapa
    color='Profissão', #separa a cor por microbacia
    text='Percento', #rotulo nas barras
    color_discrete_sequence= verde_azulado,

)

#montando elementos visuais
fig.update_traces(
    texttemplate='%{text:,} %', #separador decimal
    textposition='outside', #mostrar o rotulo acima das barras
    marker_line_width = 0, #remove a borda do mapa
    hovertemplate='<b>%{x}</b><br>Percentual: %{y:.1f}%' + '<extra></extra>'
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
    ),
    yaxis=dict(
        title='Percento (%)',                     # Título do eixo Y
        showgrid=True,                         # Mostra linhas horizontais de grade
        gridcolor='lightgray'                  # Cor da grade
    ),
    showlegend=True,                           # Mostra a legenda (pode ser desativado se cada cor já estiver clara no eixo X)
    bargap=0.1,                                  # Espaço entre as barras (0 = coladas, 0.5 = bem separadas)

)




saida_html = os.path.join(base_dir, '..', 'pg_panorama', 'grafico_emp_formais.html')
fig.write_html(saida_html, full_html=True, include_plotlyjs='cdn')


