# Importa as bibliotecas necessárias
import streamlit as st
import geopandas as gpd
import folium
# Importa o componente st_folium que permite a interação
from streamlit_folium import st_folium
from folium.plugins import Draw

# Título da aplicação
st.title("Mapa com Camada Espacial do GeoPackage (Editável)")

# Nome do arquivo GeoPackage
gpkg_file = "uc.gpkg"

# Tenta carregar o arquivo usando GeoPandas
try:
    gdf = gpd.read_file(gpkg_file)

    # Verifica se o GeoDataFrame não está vazio
    if not gdf.empty:
        # Reprojeta os dados para EPSG:4326 se necessário, que é o padrão para folium
        if gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs(epsg=4326)

        # Calcula o centro e o zoom do mapa com base na camada
        bounds = gdf.total_bounds
        center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
        
        # Cria o mapa Folium centrado na camada
        m = folium.Map(location=center, zoom_start=10)

        # Adiciona o plugin de desenho para permitir a edição
        Draw(
            export=True,
            filename="edited_data.geojson",
            position="topleft",
            draw_options={
                "polyline": False,
                "rectangle": True,
                "polygon": True,
                "circle": False,
                "marker": True,
                "circlemarker": False,
            },
            edit_options={"edit": True, "remove": True},
        ).add_to(m)

        # Adiciona a camada espacial ao mapa.
        folium.GeoJson(
            gdf,
            name="Camada Espacial de uc.gpkg",
            style_function=lambda feature: {
                "fillColor": "blue",
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.5,
            }
        ).add_to(m)

        # Adiciona um controle de camadas
        folium.LayerControl().add_to(m)

        # Exibe o mapa interativo usando st_folium
        # A saída agora contém informações sobre as edições
        st.header("Edite a Camada Espacial")
        output = st_folium(m, width=700, height=500)
        
        # Mostra os dados editados
        st.subheader("Dados Editados (GeoJSON)")
        
        # Verifica se há novas feições ou edições
        if output and 'all_drawings' in output:
            st.write(output['all_drawings'])
        else:
            st.info("Nenhuma feição foi desenhada ou editada ainda.")

    else:
        st.warning("O arquivo uc.gpkg foi carregado, mas a camada espacial está vazia.")

except FileNotFoundError:
    st.error(f"O arquivo {gpkg_file} não foi encontrado. Por favor, coloque o arquivo no mesmo diretório que o script.")

except Exception as e:
    st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")
