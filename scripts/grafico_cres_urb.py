import os
import pandas as pd
import plotly.express as px
from plotly.colors import sample_colorscale

base_dir = os.path.dirname(__file__)
excel_path = os.path.join(base_dir, '..', 'data', 'tables', 'grafico_cres_urb.xlsx')

df = pd.read_excel(excel_path)

greems = sample_colorscale('Greens', [1, 0.8, 0.6, 0.4, 0.2])
azuis = sample_colorscale('Blues', [1, 0.8, 0.6, 0.4, 0.2])
paleta = ['#2c3e50', '#34495e', '#4a6b8c', '#5f80a3', '#7f9ebf'] * 3

#formatei o dataframe para poder obter valores com casas decimais
df['População_formatada'] = df['População'].apply(lambda x: f'{x:,.0f}'.replace(',', '.'))

# montando a figura
fig = px.bar(
    df, #dataframe
    x='Microbacia',
    y='População',
    # title='População por bacia hidrográfica', #titulo do mapa
    color='Microbacia', #separa a cor por microbacia
    # text='População', #rotulo nas barras
    text='População_formatada',  # <-- Usa a versão formatada com pontos
    color_discrete_sequence= paleta,
)

#montando elementos visuais
fig.update_traces(
    texttemplate='%{text:.}', #separador decimal
    textposition='outside', #mostrar o rotulo acima das barras
    marker_line_width = 0, #remove a borda do mapa
    hovertemplate='<b>Microbacia:</b> %{x}<br><b>População:</b> %{y:,.0f}<extra></extra>'
    # hovertemplate='<b>Microbacia:</b> %{x}<br><b>População:</b> %{y:,}<extra></extra>'
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
    bargap=0.1,                                  # Espaço entre as barras (0 = coladas, 0.5 = bem separadas)

    #  legenda orizontal
    # legend=dict(
    #     orientation="h",
    #     y=-0.2,
    #     x=0.5,
    #     xanchor='center'
    # ),

     legend=dict(
        orientation="v",         # vertical (padrão)
        x=1.02,                     # posiciona à direita do gráfico
        y=1,
        xanchor="left",
        yanchor="top",
        font=dict(size=13),
        bgcolor='rgba(0,0,0,0)', # fundo transparente
        bordercolor='rgba(0,0,0,0)', # sem borda
        itemclick='toggle',         # desativa clique na legenda
        itemdoubleclick='toggle',
    ), 

    )

saida_html = os.path.join(base_dir, '..', 'pg_panorama', 'grafico_cres_urb.html')
fig.write_html(saida_html, full_html=True, include_plotlyjs='cdn')