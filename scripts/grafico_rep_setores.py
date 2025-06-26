import os
import pandas as pd
import plotly.express as px

base_dir = os.path.dirname(__file__)
excel_path = os.path.join(base_dir, '..', 'data', 'tables', 'grafico_rep_setores.xlsx')


df = pd.read_excel(excel_path)

df = df.sort_values(by='PERCENTUAL', ascending=False)

top5 = df.iloc[0:5].copy()

demais = df.iloc[5:]

total_demais = demais['PERCENTUAL'].sum()

top5.loc[6] = ['Demais setores', total_demais]
print(top5)

cores = ['#2c3e50', '#34495e', '#4a6b8c', '#5f80a3', '#7f9ebf', '#103b5c']

fig = px.bar(
    top5, 
    x='PERCENTUAL',
    y=[''] * len(top5),
    color='SETOR',
    orientation='h',
    text='SETOR',
    color_discrete_sequence= cores
    
)

fig.update_traces(
    textposition='inside',
    insidetextanchor='start',
    textfont_color='white',
    cliponaxis=False,
    hovertemplate='<b>%{text}</b><br>Percentual: %{x:.1f}%' + '<extra></extra>'
)

fig.update_layout(
    barmode='stack',
    showlegend=False,
    xaxis=dict(
        showticklabels=False,
        title=None,
        showgrid=False
    ),
    yaxis=dict(
        showticklabels=False,
        title=None
    ),
    height=200,
    margin=dict(l=10, r=10, t=10, b=10),
    plot_bgcolor='white',
    paper_bgcolor='white'
)


saida_html = os.path.join(base_dir, '..', 'pg_panorama', 'grafico_rep_setores.html')
fig.write_html(saida_html, full_html=True, include_plotlyjs='cdn')


