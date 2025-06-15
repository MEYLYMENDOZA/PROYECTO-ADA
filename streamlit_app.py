import pandas as pd
from geopy.distance import geodesic
import folium
import streamlit as st
from streamlit_folium import st_folium  # ✅ Necesario para mostrar el mapa en Streamlit

st.set_page_config(page_title="Mapa WiFi Gratuito", layout="centered")
st.title("📡 Mapa de Acceso Gratuito a Internet por Distrito")

# Leer archivos CSV
df_victoria = pd.read_csv("la_victoria.csv")
df_lurigancho = pd.read_csv("san_juan_de_lurigancho.csv")

# Limpiar datos vacíos
df_victoria.dropna(subset=["latitud", "longitud"], inplace=True)
df_lurigancho.dropna(subset=["latitud", "longitud"], inplace=True)

# Unir todos los puntos
df_puntos = pd.concat([df_victoria, df_lurigancho])

# Crear mapa centrado en promedio de latitud/longitud
m = folium.Map(location=[df_puntos.latitud.mean(), df_puntos.longitud.mean()], zoom_start=12)

# Función para conectar puntos cercanos
def conectar_puntos(df):
    lugares = df[["nombre_lugar", "latitud", "longitud"]].values
    for i, (n1, lat1, lon1) in enumerate(lugares):
        distancias = []
        for j, (n2, lat2, lon2) in enumerate(lugares):
            if i != j:
                dist = geodesic((lat1, lon1), (lat2, lon2)).meters
                distancias.append((dist, lat2, lon2))
        distancias.sort()
        for _, lat2, lon2 in distancias[:3]:
            folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="blue").add_to(m)

# Agregar marcadores y líneas para La Victoria
df_victoria.apply(lambda row: folium.Marker([row.latitud, row.longitud], popup=row.nombre_lugar).add_to(m), axis=1)
conectar_puntos(df_victoria)

# Agregar marcadores y líneas para San Juan de Lurigancho
df_lurigancho.apply(lambda row: folium.Marker([row.latitud, row.longitud], popup=row.nombre_lugar).add_to(m), axis=1)
conectar_puntos(df_lurigancho)

# Mostrar el mapa dentro de Streamlit
st.markdown("### 🌐 Mapa interactivo")
st_folium(m, width=800, height=600)
