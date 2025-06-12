import os
import folium
from geopandas import read_file
from folium.features import GeoJsonPopup
from folium.features import GeoJsonTooltip


min_lat = -20,374
min_long = -54,928
max_lat = -21,246
max_long = -54,225

def hidrografia(x):
    geojson = read_file("data/geojson/02_HIDROGRAFIA.geojson")
    folium.GeoJson(
        geojson,
        overlay=True, #se pode ser sobreposta
        control=False, # se irá aparecer na escala
        show= True, # se a camada virá ligada
        name='Hidrografia',
        style_function= lambda feature: {
            'color': "blue",
            'weight': 0.5,
            'fillOpacity': 1,
            
        }
        # popup=GeoJsonPopup(
        #     fields=['NOME_CORRE'],
        #     labels=False,
        #     ),

    ).add_to(x)


def subbacias(x):

    geojson = read_file("data/geojson/01_SUB_BACIAS_GERAIS.geojson")
    folium.GeoJson(
        geojson,
        overlay=False, #se pode ser sobreposta
        control=False, # se irá aparecer na escala
        show= True, # se a camada virá ligada

        #a função style function configura o fundo do mapa
        style_function= lambda feature: {
            'fillColor': "#3a595c", #cor de fundo
            'color': "#AFAFAF", #cor da borda
            #'dashArray': 5, #tracejamento da borda
            'weight': '1', #tamanho da borda
            'fillOpacity': 1, #transparencia da cor de fundo e cor de borda
        },

        #a função highlight function é para dar estilo ao destacamento da feição após passar o mouse
        highlight_function = lambda feature: {
            'fillColor': "red", 
            'color': "red", 
            #'oppacity':0.3, também pode ser subastituído por fillOpacity
            'dashArray': 5, 
            'fillOpacity': 0.3,
            'stroke': False,
        },
        name='Sub bacias hidrográficas',
     
        # junto a highlight function, irá aparecer o nome da feição ao passar o mouse
        tooltip=GeoJsonTooltip(
            fields=['NOME'], #coluna do popup
            sticky=True, #se o nome acompanha o mouse, ou centraliza na feição
            labels=False) #evita o nome da coluna
    ).add_to(x)


def criar_mapa():
    
    mapa = folium.Map(
        location=[-20.81130,-54.57809], #retangulo envolvente inicial
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_long,
        max_lon=max_long,
        zoom_start=11,  #zoom inicial
        control_scale=False, #desativar layers na escala
        zoom_control=False, #poder alterar o zoom de visualização
        width='100%',  #larguma 
        height='1350px', #altura
        tiles = None, #basemap
        scrollWheelZoom=False, #evitar scroll do mouse
        attributionControl=False,
    )

    hidrografia(mapa)
    subbacias(mapa)

    # mapa_id = mapa.get_name()

    travar_arraste_mouse = folium.Element("""
    <script>
        window.addEventListener('load', function () {
            var maps = Object.values(window).filter(v => v instanceof L.Map);
            if (maps.length > 0) {
                var map = maps[0];  // assume o primeiro mapa Leaflet da página
                map.dragging.disable();
                map.scrollWheelZoom.disable();
                map.doubleClickZoom.disable();
                map.touchZoom.disable();
            }
        });
    </script>
    """)

    fundo_transparente = folium.Element("""
    <style>
    div.leaflet-container {
        background: transparent !important;
    }
    </style>
    """)

    mapa.get_root().html.add_child(fundo_transparente) #injeção de CSS transparente ao Leaflet do Folium 
    mapa.get_root().html.add_child(travar_arraste_mouse) #injeção de JS do Leaflet do Folium 
    
    return mapa


m = criar_mapa()


caminho_saida = os.path.join(os.path.dirname(__file__), '..', 'mapa.html')
caminho_saida = os.path.abspath(caminho_saida)

m.save(caminho_saida)




