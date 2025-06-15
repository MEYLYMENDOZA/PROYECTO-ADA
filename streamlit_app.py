import pandas as pd
from geopy.distance import geodesic
import folium
import streamlit as st
from streamlit_folium import st_folium

# Configuración visual de la página
st.set_page_config(page_title="Mapa WiFi Gratuito", layout="centered", page_icon="📡")

# Títulos con colores personalizados
st.markdown("<h1 style='text-align: center; color: #0073e6;'>Mapa de Acceso Gratuito a Internet por Distrito</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #0066cc;'>Visualiza los puntos de acceso WiFi en tu distrito</h3>", unsafe_allow_html=True)

# Menú desplegable para seleccionar el distrito
opcion = st.selectbox("Selecciona qué distrito mostrar:", ["Ambos", "La Victoria", "San Juan de Lurigancho"])

# Cargar los archivos
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

# Crear el mapa centrado en el promedio de latitud y longitud
m = folium.Map(location=[df_puntos.latitud.mean(), df_puntos.longitud.mean()], zoom_start=12, control_scale=True)

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

# Estilo de los marcadores
def marcador_estilo(distrito, nombre):
    return f"{distrito} - {nombre}"

# Agregar marcadores y líneas según la opción seleccionada
if opcion in ["Ambos", "La Victoria"]:
    df_victoria.apply(lambda row: folium.Marker([row.latitud, row.longitud], 
                                               popup=marcador_estilo("La Victoria", row.nombre_lugar), 
                                               icon=folium.Icon(color="blue")).add_to(m), axis=1)
    conectar_puntos(df_victoria, color="blue")

if opcion in ["Ambos", "San Juan de Lurigancho"]:
    df_lurigancho.apply(lambda row: folium.Marker([row.latitud, row.longitud], 
                                                  popup=marcador_estilo("San Juan de Lurigancho", row.nombre_lugar), 
                                                  icon=folium.Icon(color="green")).add_to(m), axis=1)
    conectar_puntos(df_lurigancho, color="green")

# Mostrar el mapa interactivo
st.markdown("### 🌍 Mapa interactivo")
st_folium(m, width=800, height=600)

# Botón de descarga de CSV
@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df_puntos)
st.download_button(
    label="Descargar datos como CSV",
    data=csv,
    file_name='datos_wifi.csv',
    mime='text/csv',
    use_container_width=True
)

# Agregar créditos o nota final
st.markdown("<p style='text-align: center; color: #666666;'>Datos proporcionados por la comunidad para el acceso libre a Internet.</p>", unsafe_allow_html=True)

