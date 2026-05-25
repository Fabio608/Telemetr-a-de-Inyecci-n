import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time

# 1. CONFIGURACION DEL DASHBOARD
st.set_page_config(
    page_title="Vigia Diesel - Ruta 26", 
    layout="wide"
)

if "paso" not in st.session_state:
    st.session_state.paso = 0
if "animacion_activa" not in st.session_state:
    st.session_state.animacion_activa = False

# 2. GENERACION GEOSPATIAL DE ALTA DENSIDAD (SIMULA EL TRAZADO REAL)
# Definimos los puntos de quiebre reales de la Ruta 26 de Comodoro a Sarmiento
puntos_clave = [
    {"km": 0, "lat": -45.8641, "lon": -67.4965, "alt": 10, "estado": "OK"},       # Comodoro
    {"km": 12, "lat": -45.9230, "lon": -67.5610, "alt": 75, "estado": "OK"},      # Cruce Rada Tilly
    {"km": 25, "lat": -45.9050, "lon": -67.6800, "alt": 210, "estado": "OK"},     # Subida El Trebol
    {"km": 40, "lat": -45.8810, "lon": -67.8250, "alt": 380, "estado": "OK"},     # Pampa del Castillo
    {"km": 55, "lat": -45.8610, "lon": -68.0150, "alt": 540, "estado": "CRITICO"}, # Cresta de la Meseta
    {"km": 75, "lat": -45.8300, "lon": -68.3000, "alt": 450, "estado": "ADV"},     # Bajada Valle Hermoso
    {"km": 100, "lat": -45.7500, "lon": -68.7500, "alt": 300, "estado": "OK"},    # Entrada al Valle
    {"km": 125, "lat": -45.5901, "lon": -69.0800, "alt": 260, "estado": "OK"}     # Sarmiento
]

# Interpolación matemática para generar 80 puntos intermedios y "pegar" la linea a la ruta
@st.cache_data
def generar_traza_continua(puntos):
    lista_puntos = []
    for i in range(len(puntos) - 1):
        p1 = puntos[i]
        p2 = puntos[i+1]
        # Generamos 10 sub-puntos entre cada tramo
        sub_pasos = 10
        for j in range(sub_pasos):
            fraccion = j / sub_pasos
            km_inter = p1["km"] + (p2["km"] - p1["km"]) * fraccion
            lat_inter = p1["lat"] + (p2["lat"] - p1["lat"]) * fraccion
            lon_inter = p1["lon"] + (p2["lon"] - p1["lon"]) * fraccion
            alt_inter = p1["alt"] + (p2["alt"] - p1["alt"]) * fraccion
            
            # Agregamos una leve curvatura geografica para que no sea una linea recta rigida
            if i == 2 or i == 4: # Zonas con mas curvas en la ruta real
                lon_inter += np.sin(fraccion * np.pi) * 0.008
            
            lista_puntos.append({
                "km": round(km_inter, 1),
                "lat": lat_inter,
                "lon": lon_inter,
                "alt": int(alt_inter),
                "lugar": f"Ruta 26 - KM {int(km_inter)}",
                "estado": p1["estado"] if fraccion < 0.5 else p2["estado"]
            })
    lista_puntos.append(puntos[-1]) # Agregar el punto final de Sarmiento
    return list_puntos

datos_ruta = generar_traza_continua(puntos_clave)

# 3. INTERFAZ DE CONTROL (BOTONES)
st.title("Vigia Diesel Pro - Telemetria en Ruta 26 Real")
st.write("Muestreo de alta densidad para seguimiento de curvas y analisis de inyeccion.")

col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    if st.button("INICIAR VIAJE"):
        st.session_state.animacion_activa = True
with col_btn2:
    if st.button("PAUSAR"):
        st.session_state.animacion_activa = False
with col_btn3:
    if st.button("REINICIAR"):
        st.session_state.paso = 0
        st.session_state.animacion_activa = False

# Logica de refresco automatico
if st.session_state.animacion_activa:
    if st.session_state.paso < len(datos_ruta) - 1:
        st.session_state.paso += 1
        time.sleep(1) # Un paso por segundo para dinamismo
        st.rerun()
    else:
        st.session_state.animacion_activa = False

punto_actual = datos_ruta[st.session_state.paso]

# 4. DISTRIBUCION DE LA PANTALLA
col_mapa, col_telemetria = st.columns([2, 1])

with col_mapa:
    st.subheader(f"GPS: {punto_actual['lugar']}")
    
    # Mapa centrado dinamicamente en el camion
    m = folium.Map(location=[punto_actual["lat"], punto_actual["lon"]], zoom_start=11, tiles=None)
    
    # Capa Satelital Hibrida de Google Maps
    folium.TileLayer(
        tiles='http://mt0.google.com/vt/lyrs=y&hl=es&x={x}&y={y}&z={z}',
        attr='Google Maps',
        name='Google Satellite',
        max_zoom=20
    ).add_to(m)
    
    # Dibujar la estela del camion de alta densidad (sigue las curvas)
    coordenadas_hasta_ahora = [[p["lat"], p["lon"]] for p in datos_ruta[:st.session_state.paso + 1]]
    if len(coordenadas_hasta_ahora) > 1:
        folium.PolyLine(coordenadas_hasta_ahora, color="#00FFFF", weight=6, opacity=0.9).add_to(m)
    
    # Dibujar los marcadores especificos cada 5 pasos para no saturar la pantalla
    for idx, p in enumerate(datos_ruta[:st.session_state.paso + 1]):
        if idx % 5 == 0 or idx == st.session_state.paso:
            color_nodo = "green" if p["estado"] == "OK" else "orange" if p["estado"] == "ADV" else "red"
            folium.Marker(
                location=[p["lat"], p["lon"]],
                popup=f"KM {p['km']}",
                icon=folium.Icon(color=color_nodo, icon="screenshot")
            ).add_to(m)
        
    st_folium(m, width=850, height=450, key=f"mapa_real_{st.session_state.paso}")

with col_telemetria:
    st.subheader("Ficha Diagnostica")
    
    if punto_actual["estado"] == "OK":
        st.success("Estado de Flota: OPTIMO")
    elif punto_actual["estado"] == "ADV":
        st.warning("Estado de Flota: ADVERTENCIA")
    else:
        st.error("Estado de Flota: CRITICO")
        
    st.markdown("---")
    st.write("**Unidad:** Scania R450")
    st.write(f"**Altitud:** {punto_actual['alt']} metros s.n.m.")
    st.write(f"**Posicion:** {punto_actual['lat']:.4f}, {punto_actual['lon']:.4f}")
    
    st.markdown("### Caudal de Compensacion")
    
    # Logica de fallas vinculadas a la posicion geografica en la meseta
    if punto_actual["estado"] == "ADV":
        val_inj2 = 5.4
    elif punto_actual["estado"] == "CRITICO":
        val_inj2 = 13.8
    else:
        val_inj2 = 0.6
        
    st.metric(label="Inyector 1", value="0.9 %")
    st.metric(label="Inyector 2", value=f"{val_inj2} %")
    st.metric(label="Inyector 3", value="1.1 %")
    st.metric(label="Inyector 4", value="0.7 %")

# 5. PERFIL DE RELIEVE
st.markdown("---")
st.subheader("⛰️ Perfil Altometrico e Historial de Carga del Motor")

datos_grafico = pd.DataFrame(datos_ruta[:st.session_state.paso + 1])
if not datos_grafico.empty:
    st.area_chart(datos_grafico.set_index("km")["alt"], color="#FFA500", height=150)
