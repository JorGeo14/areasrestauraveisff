# Importa as bibliotecas necessárias
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# Título da aplicação
st.title("Mapa com Camada Espacial do GeoPackage")

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

        # Adiciona a camada espacial ao mapa.
        # Use um estilo básico para visualização.
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

        # Adiciona um controle de camadas para ligar/desligar a camada
        folium.LayerControl().add_to(m)

        # Exibe o mapa na aplicação Streamlit
        st.header("Camada Espacial de uc.gpkg")
        folium_static(m)
    else:
        st.warning("O arquivo uc.gpkg foi carregado, mas a camada espacial está vazia.")

except FileNotFoundError:
    st.error(f"O arquivo {gpkg_file} não foi encontrado. Por favor, coloque o arquivo no mesmo diretório que o script.")

except Exception as e:
    st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")

