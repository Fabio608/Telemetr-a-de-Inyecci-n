import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time

# 1. CONFIGURACIÓN DEL DASHBOARD
st.set_page_config(page_title="Vigía Diesel - DEMO EN VIVO", layout="wide")

# Inicializar el estado de la animación si no existe
if "paso" not in st.session_state:
    st.session_state.paso = 0
if "animacion_activa" not in st.session_state:
    st.session_state.animacion_activa = False

# 2. BASE DE DATOS DE LA RUTA (Comodoro Rivadavia a Sarmiento - Ruta 26)
# Simulamos coordenadas reales, elevaciones de la meseta y fallas aleatorias
datos_ruta = [
    {"km": 0, "lat": -45.8641, "lon": -67.4965, "alt": 10, "lugar": "Salida: Comodoro Rivadavia", "estado": "🟢 OK"},
    {"km": 15, "lat": -45.8850, "lon": -67.5800, "alt": 120, "lugar": "Subida de El Trébol", "estado": "🟢 OK"},
    {"km": 30, "lat": -45.8900, "lon": -67.7500, "alt": 250, "lugar": "Zona de Canteras / Pampa del Castillo", "estado": "🟢 OK"},
    {"km": 45, "lat": -45.8700, "lon": -67.9500, "alt": 410, "lugar": "Meseta Central (Subida fuerte)", "estado": "🟡 ADVERTENCIA - Inj 2 exigido"},
    {"km": 60, "lat": -45.8500, "lon": -68.1500, "alt": 550, "lugar": "Alto Río Senguer / Cruce Rutas", "estado": "🔴 ALERTA CRÍTICA - Falla Inj 2"},
    {"km": 75, "lat": -45.8300, "lon": -68.4000, "alt": 480, "lugar": "Bajada hacia Valle Hermoso", "estado": "🟡 ADVERTENCIA - Presión inestable"},
    {"km": 90, "lat": -45.7900, "lon": -68.6500, "alt": 320, "lugar": "Aproximación a Sarmiento", "estado": "🟢 OK"},
    {"km": 105, "lat": -45.5901, "lon": -69.0800, "alt": 260, "lugar": "Llegada: Sarmiento (Chubut)", "estado": "🟢 OK"}
]

# 3. INTERFAZ DE CONTROL (Encabezado)
st.title("🚚 Demo de Telemetría en Tiempo Real: Tramo Comodoro - Sarmiento")
st.write("Simulación de envío de datos de inyección cada 2 segundos vinculados a la topografía de la Ruta 26.")

# Botones para controlar la simulación
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    if st.button("▶️ Iniciar / Avanzar Camión"):
        st.session_state.animacion_activa = True
with col_btn2:
    if st.button("⏸️ Pausar Simulación"):
        st.session_state.animacion_activa = False
with col_btn3:
    if st.button("🔄 Reiniciar Viaje"):
        st.session_state.paso = 0
        st.session_state.animacion_activa = False

# Lógica de avance automático (Cada actualización avanza un paso)
if st.session_state.animacion_activa:
    if st.session_state.paso < len(datos_ruta) - 1:
        st.session_state.paso += 1
        time.sleep(2) # Retraso de 2 segundos simulando la señal GPS
        st.rerun()
    else:
        st.session_state.animacion_activa = False

# Obtener datos del punto actual del camión
punto_actual = datos_ruta[st.session_state.paso]

# 4. DISTRIBUCIÓN DEL DASHBOARD
col_mapa, col_telemetria = st.columns([2, 1])

with col_mapa:
    st.subheader(f"📍 Posición GPS Actual: {punto_actual['lugar']} (KM {punto_actual['km']})")
    
    # Crear mapa base con Google Satellite
    m = folium.Map(location=[punto_actual["lat"], punto_actual["lon"]], zoom_start=10, tiles=None)
    folium.TileLayer(
        tiles='http://mt0.google.com/vt/lyrs=y&hl=es&x={x}&y={y}&z={z}',
        attr='Google Maps',
        name='Google Satellite',
        max_zoom=20
    ).add_to(m)
    
    # Dibujar todo el historial del recorrido hecho hasta el momento
    coordenadas_hasta_ahora = [[p["lat"], p["lon"]] for p in datos_ruta[:st.session_state.paso + 1]]
    if len(coordenadas_hasta_ahora) > 1:
        folium.PolyLine(coordenadas_hasta_ahora, color="cyan", weight=5, opacity=0.8).add_to(m)
    
    # Colocar los marcadores cada 15km con el color de salud correspondiente
    for i, p in enumerate(datos_ruta[:st.session_state.paso + 1]):
        if "🟢" in p["estado"]:
            color_nodo = "green"
        elif "🟡" in p["estado"]:
            color_nodo = "orange"
        else:
            color_nodo = "red"
            
        folium.Marker(
            location=[p["lat"], p["lon"]],
            popup=f"KM {p['km']}: {p['estado']}",
            icon=folium.Icon(color=color_nodo, icon="info-sign")
        ).add_to(m)
        
    # Renderizar mapa
    st_folium(m, width=850, height=450, key=f"mapa_{st.session_state.paso}")

with col_telemetria:
    st.subheader("📊 Ficha de Inyección Digital")
    
    # Cuadro de alertas dinámico
    if "🟢" in punto_actual["estado"]:
        st.success(f"Estado de Flota: {punto_actual['estado']}")
    elif "🟡" in punto_actual["estado"]:
        st.warning(f"Estado de Flota: {punto_actual['estado']}")
    else:
        st.error(f"Estado de Flota: {punto_actual['estado']}")
        
    st.markdown("---")
    st.write("**Un
