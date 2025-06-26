import os
import folium
from geopandas import read_file
from folium.features import GeoJsonTooltip


# cores_classes = {
#     "Agricultura": "#c9c996",        # amarelo
#     "Área Úmida": "#00ffff",         # ciano
#     "Áreas antropiadas": "#e73e0b", # laranja
#     "Áreas ubanizadas": "#808080",  # cinza
#     "Corpos hídricos": "#0000ff",    # azul
#     "Pastagem": "#a5be80",           # verde-claro
#     "Vegetação": "#006400",          # verde-escuro
# }

# def style_function(feature):
#     classe = feature['properties']['CATEGORIA']  # Substitua 'classe' pelo nome correto do campo
#     cor = cores_classes.get(classe, "#000000")  # cor padrão: preto
#     return {
#         'fillColor': cor,
#         'color': cor,
#         'weight': 1,
#         'fillOpacity': 1,
#     }


def subbacias(x):

    geojson = read_file("data/geojson/01_SUB_BACIAS_GERAIS.geojson")

    folium.GeoJson(
        geojson,
        overlay=False, 
        control=False, 
        show= True,      
        style_function= lambda feature: {
            'fillColor': "#3a595c", #cor de fundo
            'color': "#9B9999", #cor da borda
            #'dashArray': 5, #tracejamento da borda
            'weight': 2, #tamanho da borda
            'fillOpacity': 0, #transparencia da cor de fundo e cor de borda
           
        },  
        # highlight_function = lambda feature: {
        #     'fillColor': "red", 
        #     'color': "red", 
        #     #'oppacity':0.3, também pode ser subastituído por fillOpacity
        #     'dashArray':0, 
        #     'fillOpacity': 0.5,
            
        # },
        name='Sub bacias hidrográficas', 
        tooltip=GeoJsonTooltip(
            fields=['NOME'], #coluna do popup
            sticky=True, #se o nome acompanha o mouse, ou centraliza na feição
            labels=False), #evita o nome da coluna
        # zoom_on_click=True, 
    ).add_to(x)

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
            'weight': 1,
            'fillOpacity': 0.,
            
        }
        # popup=GeoJsonPopup(
        #     fields=['NOME_CORRE'],
        #     labels=False,
        #     ),

    ).add_to(x)

def criar_mapa():
    
    mapa = folium.Map(
        location=[-20.62232,-54.62204], #[-20.81130,-54.57809]
        zoom_start= 11,  
        control_scale=False,
        zoom_control=False,
        width='100%',  
        height='880px', 
        tiles = None, 
        scrollWheelZoom=False, 
        attributionControl=False,
        


    )
    hidrografia(mapa)
    subbacias(mapa)


    lista_suspensa_bacias = folium.Element("""
    <div id="bacia-dropdown" style="
            position: fixed;
            top: 10px;
            left: 10px;
            background-color: white;
            padding: 10px;
            border: 1px solid ;
            border-radius: 5px;
            font-family: Arial, sans-serif;
            font-style: italic;
            color: rgb(77, 72, 72);
            font-size: 14px;
            box-shadow: 1px 1px 2px rgba(0,0,0,0.2);
            z-index: 9999;
            opacity: 0.9;">
            
        <label for="select-bacia"><b>Selecione uma Sub-bacia:</b></label><br>
        <select id="select-bacia">
            <option value="">-- Escolha --</option>
        </select>
    </div>

    <script>
    window.addEventListener('load', function () {
        var maps = Object.values(window).filter(v => v instanceof L.Map);
        if (maps.length === 0) return;

        var map = maps[0];
        var layersBacias = [];

        var nomesBacias = [];

        map.eachLayer(function (layer) {
            if (layer.feature && layer.feature.properties && layer.feature.properties.NOME) {
                layersBacias.push(layer);
                nomesBacias.push(layer.feature.properties.NOME);
            }
        });

        nomesBacias.sort(function(a, b) {
            return a.localeCompare(b);
        });

        nomesBacias.forEach(function(nome) {
            var opt = document.createElement('option');
            opt.value = nome;
            opt.textContent = nome;
            document.getElementById('select-bacia').appendChild(opt);
        });


        document.getElementById('select-bacia').addEventListener('change', function () {
            var nomeSelecionado = this.value;
            var layerEncontrado = layersBacias.find(l => l.feature.properties.NOME === nomeSelecionado);
            if (!layerEncontrado) return;

            var props = layerEncontrado.feature.properties;
            var b = layerEncontrado.getBounds();
            var bounds = [b.getSouth(), b.getWest(), b.getNorth(), b.getEast()].join(",");

            window.parent.postMessage({
                type: 'baciaSelecionada',
                nome: props.NOME,
                desc: props.DESC,
                rio: props.RIO,
                area: props.AREA_M2,
                inf_urb: props["inf-urb"],
                inf_past: props["inf-past"],
                inf_agro: props["inf-agro"],
                inf_veg: props["inf-veg"],
                inf_umd: props["inf-umd"],
                inf_antr: props["inf-antr"],
                inf_cp: props["inf-cp"],
                bounds: bounds
            }, '*');

            if (window.camadaSelecionada) {
                map.removeLayer(window.camadaSelecionada);
            }

            window.camadaSelecionada = L.geoJSON(layerEncontrado.feature, {
                style: {
                    fillColor: 'yellow', 
                    weight: 2,
                    fillOpacity: 0.3,
                }
            }).addTo(map);

            map.fitBounds(window.camadaSelecionada.getBounds());
        });
    });
    </script>
    """)



    
    botao_reset_view = folium.Element("""
    <style>
    #botaoReset {
        position: absolute;
        top: 80px;
        left: 10px;
        z-index: 9999;
        background-color: #ffffff;
        border: 1px solid #aaa;
        border-radius: 4px;
        padding: 6px 10px;

        font-size: 14px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    </style>

    <div id="botaoReset">↺ Redefinir visão</div>

    <script>
    window.addEventListener('load', function () {
        var maps = Object.values(window).filter(v => v instanceof L.Map);
        if (maps.length === 0) return;

        var map = maps[0];

        // Salva a visão inicial
        var viewInicial = {
            center: map.getCenter(),
            zoom: map.getZoom()
        };

        var botao = document.getElementById('botaoReset');
        if (botao) {
            botao.addEventListener('click', function () {
                map.setView(viewInicial.center, viewInicial.zoom);
            });
        }
    });
    </script>
    """)
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
        background: #ffffff !important;
    }
    </style>
    """)
    cursor_remove = folium.Element("""
    <script>
        var css = '.leaflet-interactive { cursor: default !important; }';
        var style = document.createElement('style');
        style.type = 'text/css';
        if (style.styleSheet) {
        style.styleSheet.cssText = css;
        } else {
        style.appendChild(document.createTextNode(css));
        }
        document.head.appendChild(style);
    </script>
    """)

    mapa.get_root().html.add_child(cursor_remove)
    mapa.get_root().html.add_child(lista_suspensa_bacias)
    mapa.get_root().html.add_child(fundo_transparente) #injeção de CSS transparente ao Leaflet do Folium 
    mapa.get_root().html.add_child(travar_arraste_mouse) #injeção de JS do Leaflet do Folium 
    mapa.get_root().html.add_child(botao_reset_view)  
    return mapa

# injeção de HTML para fundo colorido no folium
fundo_mapa = folium.Element("""
<style>
html, body {
    width: 100%;height: 100%;margin: 0;padding: 0;background-color: #ffffff !important}
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

caminho_saida = os.path.join(os.path.dirname(__file__), '..', 'pg_conheca', '03_mapa_pg_conheca.html')
caminho_saida = os.path.abspath(caminho_saida)

m.save(caminho_saida)