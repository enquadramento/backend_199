import folium
from geopandas import read_file
from folium.features import GeoJsonTooltip


cores_classes = {
    "Agricultura": "#c9c996",        # amarelo
    "Área Úmida": "#00ffff",         # ciano
    "Áreas antropiadas": "#e73e0b", # laranja
    "Áreas ubanizadas": "#808080",  # cinza
    "Corpos hídricos": "#0000ff",    # azul
    "Pastagem": "#a5be80",           # verde-claro
    "Vegetação": "#006400",          # verde-escuro
}

def style_function(feature):
    classe = feature['properties']['CATEGORIA']  # Substitua 'classe' pelo nome correto do campo
    cor = cores_classes.get(classe, "#000000")  # cor padrão: preto
    return {
        'fillColor': cor,
        'color': cor,
        'weight': 1,
        'fillOpacity': 1,
    }


def subbacias(x):

    geojson = read_file("data/geojson/01_SUB_BACIAS_GERAIS.geojson")

    folium.GeoJson(
        geojson,
        overlay=False, 
        control=False, 
        show= True,      
        style_function= lambda feature: {
            'fillColor': "#3a595c", #cor de fundo
            'color': "#FFFFFF", #cor da borda
            #'dashArray': 5, #tracejamento da borda
            'weight': 2, #tamanho da borda
            'fillOpacity': 0, #transparencia da cor de fundo e cor de borda
           
        },  
        highlight_function = lambda feature: {
            'fillColor': "red", 
            'color': "red", 
            #'oppacity':0.3, também pode ser subastituído por fillOpacity
            'dashArray':0, 
            'fillOpacity': 0.3,
            
        },
        name='Sub bacias hidrográficas', 
        tooltip=GeoJsonTooltip(
            fields=['NOME'], #coluna do popup
            sticky=True, #se o nome acompanha o mouse, ou centraliza na feição
            labels=False), #evita o nome da coluna
        zoom_on_click=True, 
    ).add_to(x)

def uso_da_terra(x):
    geojson = read_file("data/geojson/03_USO_DA_TERRA04.geojson")

    folium.GeoJson(
        geojson,
        name='Uso da terra',
        overlay=True,
        control=False,
        show=True,
        style_function=style_function
    ).add_to(x)

def criar_mapa():
    
    mapa = folium.Map(
        location=[-20.81130,-54.57809], 
        zoom_start= 10,  
        control_scale=False,
        zoom_control=False,
        width='100%',  
        height='880px', 
        tiles = None, 
        scrollWheelZoom=False, 
        attributionControl=False,
        


    )
    uso_da_terra(mapa)
    subbacias(mapa)


    aviso = """
   AVISOENAS SERÁ UTILIADO SE O IFRAME FOR INCORPORADO NO CODIGO PRINCIPAL
    # script_click = folium.Element(
        <script>
            window.addEventListener('load', function () {
                var maps = Object.values(window).filter(v => v instanceof L.Map);
                if (maps.length === 0) return;

                var map = maps[0];

                map.eachLayer(function (layer) {
                    if (layer.feature && layer.feature.properties && layer.feature.properties.NOME) {
                        layer.on('click', function () {
                            var nome = layer.feature.properties.NOME;
                            var div = document.getElementById("bacia-info");
                            if (div) {
                                div.innerHTML = "A bacia selecionada é a do " + nome;
                            }
                        });
                    }
                });
            });
        </script> - falta um parentese aq
        """
   
    html_legenda = folium.Element("""
    <div id="mapa-legenda" style="
        position: fixed;
        bottom: 30px;
        left: 30px;
        background-color: white;
        padding: 10px;
        border: 1px solid #999;
        border-radius: 5px;
        font-family: Arial, sans-serif;
        font-size: 14px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        z-index: 9999;
    ">
        <b>Legenda - Uso da Terra</b><br>
        <div><span style="background:#c9c996; width: 20px; height: 20px; display: inline-block; margin-right: 8px;"></span>Agricultura</div>
        <div><span style="background:#00ffff; width: 20px; height: 20px; display: inline-block; margin-right: 8px;"></span>Área Úmida</div>
        <div><span style="background:#e73e0b; width: 20px; height: 20px; display: inline-block; margin-right: 8px;"></span>Áreas antropiadas</div>
        <div><span style="background:#808080; width: 20px; height: 20px; display: inline-block; margin-right: 8px;"></span>Áreas urbanizadas</div>
        <div><span style="background:#0000ff; width: 20px; height: 20px; display: inline-block; margin-right: 8px;"></span>Corpos hídricos</div>
        <div><span style="background:#a5be80; width: 20px; height: 20px; display: inline-block; margin-right: 8px;"></span>Pastagem</div>
        <div><span style="background:#006400; width: 20px; height: 20px; display: inline-block; margin-right: 8px;"></span>Vegetação</div>
    </div>
    """)
    botao_reset_view = folium.Element("""
    <style>
    #botaoReset {
        position: absolute;
        top: 10px;
        left: 10px;
        z-index: 9999;
        background-color: #ffffff;
        border: 1px solid #aaa;
        border-radius: 4px;
        padding: 6px 10px;
        cursor: pointer;
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
    
    aviso2 = """script_click_iframe = folium.Element(
    <script>
        window.addEventListener('load', function () {
            var maps = Object.values(window).filter(v => v instanceof L.Map);
            if (maps.length === 0) return;

            var map = maps[0];

            map.eachLayer(function (layer) {
                if (layer.feature && layer.feature.properties && layer.feature.properties.NOME && layer.feature.properties.DESC) {
                    layer.on('click', function () {
                        var nome = layer.feature.properties.NOME;
                        var desc = layer.feature.properties.DESC;
                        window.parent.postMessage(
                            { type: 'baciaSelecionada', nome: nome, desc: desc },
                            '*'
                        );
                    });
                }
            });
        });
    </script>
    )"""

    script_click_iframe = folium.Element("""
    <script>
        window.addEventListener('load', function () {
            var maps = Object.values(window).filter(v => v instanceof L.Map);
            if (maps.length === 0) return;

            var map = maps[0];
            var camadaSelecionada = null;

            map.eachLayer(function (layer) {
                if (layer.feature && layer.feature.properties && layer.feature.properties.NOME && layer.feature.properties.DESC) {
                    layer.on('click', function () {
                        var nome = layer.feature.properties.NOME;
                        var desc = layer.feature.properties.DESC;

                        // Envia mensagem para o iframe pai
                        window.parent.postMessage(
                            { type: 'baciaSelecionada', nome: nome, desc: desc },
                            '*'
                        );

                        // Remove camada anterior
                        if (camadaSelecionada) {
                            map.removeLayer(camadaSelecionada);
                            camadaSelecionada = null;
                        }

                        // Cria nova camada com apenas o polígono clicado
                        camadaSelecionada = L.geoJSON(layer.feature, {
                            style: {
                                fillColor: '#ff0000',
                                color: '#ff0000',
                                weight: 2,
                                fillOpacity: 0.5
                            }
                        }).addTo(map);

                        // Ajusta o mapa para centralizar no novo polígono
                        map.fitBounds(camadaSelecionada.getBounds());
                    });
                }
            });
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
        background: #3a595c !important;
    }
    </style>
    """)
    # mapa.get_root().html.add_child(script_click)

    mapa.get_root().html.add_child(html_legenda)
    mapa.get_root().html.add_child(script_click_iframe)
    mapa.get_root().html.add_child(fundo_transparente) #injeção de CSS transparente ao Leaflet do Folium 
    mapa.get_root().html.add_child(travar_arraste_mouse) #injeção de JS do Leaflet do Folium 
    mapa.get_root().html.add_child(botao_reset_view)  
    return mapa

# injeção de HTML para fundo colorido no folium
fundo_mapa = folium.Element("""
<style>
html, body {
    width: 100%;height: 100%;margin: 0;padding: 0;background-color: #3a595c !important}
</style>
""")
m = criar_mapa()
m.get_root().html.add_child(fundo_mapa)
m.save("pg_conheca/03_mapa_pg_conheca.html")



