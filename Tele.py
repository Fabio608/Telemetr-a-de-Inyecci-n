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

if "paso" not in st.session_state:
    st.session_state.paso = 0
if "animacion_activa" not in st.session_state:
    st.session_state.animacion_activa = False

# 2. BASE DE DATOS CON LÍNEAS ULTRA CORTAS (Para evitar cortes de editor)
datos_ruta = [
    {"km": 0, "lat": -45.8641, "lon": -67.4965, "alt": 10, "lugar": "Comodoro", "estado": "OK"},
    {"km": 5, "lat": -45.8915, "lon": -67.5320, "alt": 45, "lugar": "Ind. Sur", "estado": "OK"},
    {"km": 12, "lat": -45.9230, "lon": -67.5610, "alt": 75, "lugar": "Rada Tilly", "estado": "OK"},
    {"km": 20, "lat": -45.9110, "lon": -67.6430, "alt": 180, "lugar": "El Trébol", "estado": "OK"},
    {"km": 32, "lat": -45.8920, "lon": -67.7410, "alt": 260, "lugar": "Pampa Castillo", "estado": "OK"},
    {"km": 40, "lat": -45.8810, "lon": -67.8250, "alt": 380, "lugar": "Meseta Alta", "estado": "OK"},
    {"km": 48, "lat": -45.8715, "lon": -67.9210, "alt": 430, "lugar": "Subida Meseta", "estado": "ADV"},
    {"km": 55, "lat": -45.8610, "lon": -68.0150, "alt": 540, "lugar": "Cresta Meseta", "estado": "CRITICO"},
    {"km": 68, "lat": -45.8420, "lon": -68.1890, "alt": 510, "lugar": "Cruce Rutas", "estado": "ADV"},
    {"km": 82, "lat": -45.8210, "lon": -68.3950, "alt": 420, "lugar": "Curvón", "estado": "OK"},
    {"km": 95, "lat": -45.7720, "lon": -68.7120, "alt": 310, "lugar": "Valle Hermoso", "estado": "OK"},
    {"km": 110, "lat": -45.7110, "lon": -68.9110, "alt": 275, "lugar": "Valle Entrada", "estado": "OK"},
    {"km": 125, "lat": -45.5901, "lon": -69.0800, "alt": 260, "lugar": "Sarmiento", "estado": "OK"}
]

# 3. INTERFAZ DE CONTROL
st.title("🚚 Demo Telemetría Avanzada: Ruta 26 Real")
st.write("Muestreo geográfico adaptado a la calzada.")

col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    if st.button("▶️ Iniciar Viaje"):
        st.session_state.animacion_activa = True
with col_btn2:
    if st.button("⏸
