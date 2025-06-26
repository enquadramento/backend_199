import os
import folium
from geopandas import read_file
from folium.features import GeoJsonTooltip
from folium.plugins import Fullscreen



def setores_cens(x):

    geojson = read_file("data/geojson/04_SETORES_CENSI.geojson")

    folium.GeoJson(
        geojson,
        overlay=False, 
        control=False, 
        show= True,      
        style_function= lambda feature: {
            'fillColor': "#3a595c", 
            'color': "#161616", #cor da borda
            'weight': 0.5, #tamanho da borda
            'fillOpacity': 0, #transparencia da cor de fundo e cor de borda
          
        },  

        highlight_function = lambda feature: {
            'fillColor': "red", 
            'color': "red", 
            #'oppacity':0.3, também pode ser subastituído por fillOpacity
            'dashArray':0, 
            'fillOpacity': 0.2,
            
        },

        name='Setores censitários', 
        tooltip=GeoJsonTooltip(
            fields=['POPULAÇÃO'], #coluna do popup
            sticky=True, #se o nome acompanha o mouse, ou centraliza na feição
            labels=True), #evita o nome da coluna
        zoom_on_click=False, 
    ).add_to(x)

def coropletico_pop(x):
    geojson = read_file("data/geojson/04_SETORES_CENSI.geojson")

    folium.Choropleth(
            geo_data=geojson,
            data=geojson,
            columns=["CD_SETOR", "POPULAÇÃO"],
            key_on="feature.properties.CD_SETOR",
            fill_color="BrBG_r", #amarelo, laranja e vermelho, usar o _r inverte a seleção de cores https://colorbrewer2.org/#type=diverging&scheme=BrBG&n=3
            fill_opacity=0.7,
            line_opacity=0.1,
            nan_fill_color="gray",
            legend_name="População por setor censitário",
            name="Densidade populacional"
        ).add_to(x)

def tela_full(x):
    Fullscreen(
        position='topright',
        title='Ver em tela cheia',
        title_cancel='Sair da tela cheia',
        force_separate_button=True
    ).add_to(x)

def criar_mapa():
    
    mapa = folium.Map(
        location=[-20.50136,-54.62032],  #[-20.81130,-54.57809]
        zoom_start= 12,  
        control_scale=False,
        zoom_control=True,
        width='100%',  
        height='880px', 
        tiles = None, 
        scrollWheelZoom=True, 
        attributionControl=False,
    )
    
    coropletico_pop(mapa)
    setores_cens(mapa)
    tela_full(mapa)

    fundo_transparente = folium.Element("""
    <style>
    div.leaflet-container {
        background: transparent !important;
    }
    </style>
    """)

    mapa.get_root().html.add_child(fundo_transparente) #injeção de CSS transparente ao Leaflet do Folium 
 
    return mapa

# injeção de HTML para fundo colorido no folium
fundo_mapa = folium.Element("""
<style>
html, body {
    width: 100%;height: 100%;margin: 0;padding: 0;background-color: transparent !important}
</style>
""")


remover_barra = folium.Element("""
<style>
    body {
        overflow: hidden !important;
    }
</style>
""")

m = criar_mapa()
m.get_root().html.add_child(remover_barra)
m.get_root().html.add_child(fundo_mapa)

#injeção para evitar o background black na tela cheia
ajuste_fullscreen = folium.Element("""
<script>
document.addEventListener("fullscreenchange", function() {
    let container = document.querySelector(".leaflet-container");
    if (document.fullscreenElement && container) {
        container.style.setProperty("background-color", "white", "important");
    } else if (container) {
        container.style.setProperty("background-color", "transparent", "important");
    }
});
document.addEventListener("webkitfullscreenchange", function() {
    let container = document.querySelector(".leaflet-container");
    if (document.webkitFullscreenElement && container) {
        container.style.setProperty("background-color", "white", "important");
    } else if (container) {
        container.style.setProperty("background-color", "transparent", "important");
    }
});
</script>
""")


m.get_root().html.add_child(ajuste_fullscreen)

caminho_saida = os.path.join(os.path.dirname(__file__), '..', 'pg_panorama', '02_mapa_pg_interativo_populacional.html')
caminho_saida = os.path.abspath(caminho_saida)

m.save(caminho_saida)