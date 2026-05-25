import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time

# 1. CONFIGURACIÓN DEL DASHBOARD
st.set_page_config(
    page_title="Vigía Diesel - DEMO REAL", 
    layout="wide"
)

# Inicializar el estado de la animación si no existe
if "paso" not in st.session_state:
    st.session_state.paso = 0
if "animacion_activa" not in st.session_state:
    st.session_state.animacion_activa = False

# 2. BASE DE DATOS GEOGRÁFICA TRAZADA SOBRE LA RUTA 26 REAL
# Incrementamos los puntos simulando un muestreo de alta densidad en curvas y pendientes
datos_ruta = [
    {"km": 0, "lat": -45.8641, "lon": -67.4965, "alt": 10, "lugar": "Salida: Comodoro (Taller)", "estado": "🟢 OK"},
    {"km": 5, "lat": -45.8915, "lon": -67.5320, "alt": 45, "lugar": "Zona Industrial Sur", "estado": "🟢 OK"},
    {"km": 12, "lat": -45.9230, "lon": -67.5610, "alt": 75, "lugar": "Cruce Rada Tilly (Giro Oeste)", "estado": "🟢 OK"},
    {"km": 20, "lat": -45.9110, "lon": -67.6430, "alt": 180, "lugar": "Subida El Trébol (Curvas)", "estado": "🟢 OK"},
    {"km": 32, "lat": -45.8920, "lon": -67.7410, "alt": 260, "lugar": "Ingreso a Pampa del Castillo", "estado": "🟢 OK"},
    {"km": 40, "lat": -45.8810, "lon": -67.8250, "alt": 380, "lugar": "Tramo Recto Meseta Alta", "estado": "🟢 OK"},
    {"km": 48, "lat": -45.8715, "lon": -67.9210, "alt": 430, "lugar": "Subida fuerte de la Meseta", "estado": "🟡 ADV - Inj 2 exigido"},
    {"km": 55, "lat": -45.8610, "lon": -68.0150, "alt": 540, "lugar": "Cresta de la Meseta (Exigencia)", "estado": "🔴 CRÍTICO - Falla Inj 2"},
    {"km": 68, "lat": -45.8420, "lon": -68.1890, "alt": 510, "lugar": "Cruce de Rutas (Bajada suave)", "estado": "🟡 ADV - Presión"},
    {"km": 82, "lat": -45.8210, "lon": -68.3950, "alt": 420, "lugar": "Zona Cañadón Seco / Curvón", "estado": "
