import pandas as pd
from geopy.distance import geodesic
import folium

# Leer archivos
df_distritos = pd.read_csv("distritos.csv")
df_victoria = pd.read_csv("la_victoria.csv")
df_lurigancho = pd.read_csv("san_juan_de_lurigancho.csv")

# Unir los puntos de ambos distritos
df_puntos = pd.concat([df_victoria, df_lurigancho])

# Crear mapa centrado en promedio de todos los puntos
m = folium.Map(location=[df_puntos.latitud.mean(), df_puntos.longitud.mean()], zoom_start=12)

# Función para conectar puntos dentro de un mismo distrito
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

# Guardar mapa
m.save("Mapa de distritos con Acceso de red gratuito.html")
print("✅ Mapa de distritos con acesso de wifi gratuito")
