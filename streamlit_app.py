import pandas as pd
from geopy.distance import geodesic
import folium
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(page_title="Mapa WiFi Gratuito", layout="centered")
st.title("📡 Mapa de Acceso Gratuito a Internet por Distrito")

# Menú desplegable para seleccionar el distrito
opcion = st.selectbox("Selecciona qué distrito mostrar:", ["Ambos", "La Victoria", "San Juan de Lurigancho"])

# Leer archivos CSV
df_victoria = pd.read_csv("la_victoria.csv")
df_lurigancho = pd.read_csv("san_juan_de_lurigancho.csv")

# Eliminar filas con coordenadas vacías
df_victoria.dropna(subset=["latitud", "longitud"], inplace=True)
df_lurigancho.dropna(subset=["latitud", "longitud"], inplace=True)

# Seleccionar qué puntos mostrar según el menú
if opcion == "La Victoria":
    df_puntos = df_victoria
elif opcion == "San Juan de Lurigancho":
    df_puntos = df_lurigancho
else:
    df_puntos = pd.concat([df_victoria, df_lurigancho])

# Crear el mapa centrado en el promedio de lat/lon
m = folium.Map(location=[df_puntos.latitud.mean(), df_puntos.longitud.mean()], zoom_start=12)

# Función para conectar puntos cercanos
def conectar_puntos(df, color):
    lugares = df[["nombre_lugar", "latitud", "longitud"]].values
    for i, (n1, lat1, lon1) in enumerate(lugares):
        distancias = []
        for j, (n2, lat2, lon2) in enumerate(lugares):
            if i != j:
                dist = geodesic((lat1, lon1), (lat2, lon2)).meters
                distancias.append((dist, lat2, lon2))
        distancias.sort()
        for _, lat2, lon2 in distancias[:3]:
            folium.PolyLine([(lat1, lon1), (lat2, lon2)], color=color).add_to(m)

# Mostrar puntos y líneas según la selección
if opcion in ["Ambos", "La Victoria"]:
    df_victoria.apply(lambda row: folium.Marker(
        [row.latitud, row.longitud], 
        popup=f"La Victoria - {row.nombre_lugar}"
    ).add_to(m), axis=1)
    conectar_puntos(df_victoria, color="blue")

if opcion in ["Ambos", "San Juan de Lurigancho"]:
    df_lurigancho.apply(lambda row: folium.Marker(
        [row.latitud, row.longitud], 
        popup=f"SJL - {row.nombre_lugar}"
    ).add_to(m), axis=1)
    conectar_puntos(df_lurigancho, color="green")

# Mostrar mapa interactivo
st.markdown("### 🌐 Mapa interactivo")
st_folium(m, width=800, height=600)

