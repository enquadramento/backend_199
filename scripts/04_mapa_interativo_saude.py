import os
import folium
from geopandas import read_file
from folium.features import GeoJsonTooltip
from folium.plugins import Fullscreen


def basemap_limpo(X):
    folium.TileLayer('https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png', 
                 attr='@QueirozRM', 
                 name = 'Mapa em branco',
                 show=True,
                 ).add_to(X)

def basemap_topografico(X):
    folium.TileLayer(
        'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', 
        attr='@OpenTopo', 
        name = 'Topográfico',
        show=True,
        ).add_to(X)

def basemap_satelite(X):
    folium.TileLayer(
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
        attr='@ESRI', 
        name = 'Satélite',
        show=True, #esse argumento é IMPORTANTE, porque serve para dizer se um GEJSON vem ligado ou não
        ).add_to(X)

def limites(x):
    
    geojson = read_file("data/geojson/06_BACIA.geojson")

    folium.GeoJson(
        geojson,
        overlay=False, 
        control=False, 
        show= True,
        style_function= lambda feature: {
            'fillColor': "#3a595c", #cor de fundo
            'color': "#3a595c", #cor da borda
            #'dashArray': 5, #tracejamento da borda
            'weight': 2, #tamanho da borda
            'fillOpacity': 0, #transparencia da cor de fundo e cor de borda
           
        },
    ).add_to(x)

def saude(x):
    geojson = read_file("data/geojson/10_SAUDE_MBH.geojson")

    # Cores e ícones por tipo de escola
    estilo_saude = {
        'Estadual': {'color': 'blue',    'icon': 'hospital'},
        'Federal':  {'color': 'green',   'icon': 'clinic-medical'},
        'Municipal':{'color': 'orange',  'icon': 'user-nurse'},
    }
        

    for _, row in geojson.iterrows():
        tipo = row.get("Tipo", "Outro")
        nome = row.get("Nome", "Sem nome")
        coords = [row.geometry.y, row.geometry.x]  # ponto

        estilo = estilo_saude.get(tipo, {'color': 'gray', 'icon': 'question'})

        folium.Marker(
            location=coords,
            tooltip=f"{nome} ({tipo})",
            icon=folium.Icon(color=estilo['color'], icon=estilo['icon'], prefix='fa')
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
        location=[-20.50806,-54.61853],    #[-20.81130,-54.57809]
        zoom_start= 12,  
        control_scale=False,
        zoom_control=True,
        width='100%',  
        height='880px', 
        tiles = None, 
        scrollWheelZoom=False, 
        attributionControl=False,
    )


    saude(mapa)
    limites(mapa)
    tela_full(mapa)
    basemap_limpo(mapa)

    fundo_transparente = folium.Element("""
    <style>
    div.leaflet-container {
        background: #e7e7e7 !important;
    }
    </style>
    """)

    legenda = folium.Element("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div style="position: fixed; 
                    bottom: 30px; left: 30px; z-index: 9999; 
                    background-color: white; padding: 10px; border: 2px solid grey; border-radius: 5px;
                    font-size: 14px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
            <b>Tipos de Unidade de Saúde</b><br>
            
            <i class="fa fa-hospital" style="color:#3399FF"></i> Estadual<br>
            <i class="fa fa-clinic-medical" style="color:green"></i> Federal<br>
            <i class="fa fa-user-nurse" style="color:orange"></i> Municipal<br>
        </div>
    """)
    

    mapa.get_root().html.add_child(fundo_transparente) #injeção de CSS transparente ao Leaflet do Folium 
    mapa.get_root().html.add_child(legenda)
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

fonte_awesome = folium.Element("""
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.4/css/all.css">
""")


m = criar_mapa()
m.get_root().html.add_child(remover_barra)
m.get_root().html.add_child(fundo_mapa)
m.get_root().header.add_child(fonte_awesome)

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

caminho_saida = os.path.join(os.path.dirname(__file__), '..', 'pg_panorama', '04_mapa_interativo_saude.html')
caminho_saida = os.path.abspath(caminho_saida)

m.save(caminho_saida)