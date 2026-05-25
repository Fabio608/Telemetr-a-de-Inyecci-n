import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time

# 1. CONFIGURACION
st.set_page_config(
    page_title="Vigia Diesel", 
    layout="wide"
)

if "paso" not in st.session_state:
    st.session_state.paso = 0
if "animacion_activa" not in st.session_state:
    st.session_state.animacion_activa = False

# 2. DATOS DE RUTA
datos_ruta = [
    {"km": 0, "lat": -45.8641, "lon": -67.4965, "alt": 10, "lugar": "Comodoro", "estado": "OK"},
    {"km": 5, "lat": -45.8915, "lon": -67.5320, "alt": 45, "lugar": "Ind. Sur", "estado": "OK"},
    {"km": 12, "lat": -45.9230, "lon": -67.5610, "alt": 75, "lugar": "Rada Tilly", "estado": "OK"},
    {"km": 20, "lat": -45.9110, "lon": -67.6430, "alt": 180, "lugar": "El Trebol", "estado": "OK"},
    {"km": 32, "lat": -45.8920, "lon": -67.7410, "alt": 260, "lugar": "Pampa Castillo", "estado": "OK"},
    {"km": 40, "lat": -45.8810, "lon": -67.8250, "alt": 380, "lugar": "Meseta Alta", "estado": "OK"},
    {"km": 48, "lat": -45.8715, "lon": -67.9210, "alt": 430, "lugar": "Subida Meseta", "estado": "ADV"},
    {"km": 55, "lat": -45.8610, "lon": -68.0150, "alt": 540, "lugar": "Cresta Meseta", "estado": "CRITICO"},
    {"km": 68, "lat": -45.8420, "lon": -68.1890, "alt": 510, "lugar": "Cruce Rutas", "estado": "ADV"},
    {"km": 82, "lat": -45.8210, "lon": -68.3950, "alt": 420, "lugar": "Curvon", "estado": "OK"},
    {"km": 95, "lat": -45.7720, "lon": -68.7120, "alt": 310, "lugar": "Valle Hermoso", "estado": "OK"},
    {"km": 110, "lat": -45.7110, "lon": -68.9110, "alt": 275, "lugar": "Valle Entrada", "estado": "OK"},
    {"km": 125, "lat": -45.5901, "lon": -69.0800, "alt": 260, "lugar": "Sarmiento", "estado": "OK"}
]

# 3. CONTROL
st.title("Vigia Diesel Pro - Demo Ruta 26")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("INICIAR"):
        st.session_state.animacion_activa = True
with c2:
    if st.button("PAUSAR"):
        st.session_state.animacion_activa = False
with c3:
    if st.button("REINICIAR"):
        st.session_state.paso = 0
        st.session_state.animacion_activa = False

if st.session_state.animacion_activa:
    if st.session_state.paso < len(datos_ruta) - 1:
        st.session_state.paso += 1
        time.sleep(2)
        st.rerun()
    else:
        st.session_state.animacion_activa = False

punto_actual = datos_ruta[st.session_state.paso]

# 4. VISTA
col_mapa, col_telemetria = st.columns([2, 1])

with col_mapa:
    st.subheader(f"GPS: {punto_actual['lugar']} (KM {punto_actual['km']})")
    
    m = folium.Map(location=[punto_actual["lat"], punto_actual["lon"]], zoom_start=11, tiles=None)
    
    folium.TileLayer(
        tiles='http://mt0.google.com/vt/lyrs=y&hl=es&x={x}&y={y}&z={z}',
        attr='Google Maps',
        name='Google Satellite',
        max_zoom=20
    ).add_to(m)
    
    coordenadas_hasta_ahora = [[p["lat"], p["lon"]] for p in datos_ruta[:st.session_state.paso + 1]]
    if len(coordenadas_hasta_ahora) > 1:
        folium.PolyLine(coordenadas_hasta_ahora, color="#00FFFF", weight=5, opacity=0.8).add_to(m)
    
    for p in datos_ruta[:st.session_state.paso + 1]:
        color_nodo = "green" if p["estado"] == "OK" else "orange" if p["estado"] == "ADV" else "red"
        folium.Marker(
            location=[p["lat"], p["lon"]],
            popup=f"KM {p['km']}",
            icon=folium.Icon(color=color_nodo, icon="screenshot")
        ).add_to(m)
        
    st_folium(m, width=850, height=450, key=f"mapa_real_{st.session_state.paso}")

with col_telemetria:
    st.subheader("Telemetria Inyeccion")
    
    if punto_actual["estado"] == "OK":
        st.success("Estado: OPTIMO")
    elif punto_actual["estado"] == "ADV":
        st.warning("Estado: ADVERTENCIA")
    else:
        st.error("Estado: CRITICO")
        
    st.markdown("---")
    st.write("**Movil:** Scania R450")
    st.write(f"**Altitud:** {punto_actual['alt']} m")
    
    st.markdown("### Caudal Inyectores")
    
    if punto_actual["estado"] == "ADV":
        val_inj2 = 5.2
    elif punto_actual["estado"] == "CRITICO":
        val_inj2 = 14.1
    else:
        val_inj2 = 0.7
        
    st.metric(label="Inyector 1", value="0.9 %")
    st.metric(label="Inyector 2", value=f"{val_inj2} %")
    st.metric(label="Inyector 3", value="1.1 %")
    st.metric(label="Inyector 4", value="0.8 %")

# 5. GRAFICO
st.markdown("---")
st.subheader("Perfil Altometrico (DEM)")

datos_grafico = pd.DataFrame(datos_ruta[:st.session_state.paso + 1])
if not datos_grafico.empty:
    st.area_chart(datos_grafico.set_index("km")["alt"], color="#FFA500", height=150)
