import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Vigía Diesel Pro", layout="wide", initial_sidebar_state="expanded")

# 2. GENERACIÓN DE DATOS SIMULADOS 
# (En producción, estos datos vendrán del módulo de telemetría y tu análisis GIS)
def generar_datos_simulados():
    tiempo = pd.date_range(start="2026-05-25", periods=50, freq="1min")
    
    # Simulamos el perfil de elevación (una subida)
    elevacion = np.linspace(100, 400, 50) + np.random.normal(0, 5, 50)
    
    # Simulamos inyectores. El Inyector 2 falla cuando la elevación supera los 250m
    inj_1 = np.random.normal(1, 0.2, 50)
    inj_2 = np.where(elevacion > 250, np.random.normal(12, 2, 50), np.random.normal(1, 0.2, 50))
    inj_3 = np.random.normal(1, 0.3, 50)
    inj_4 = np.random.normal(1, 0.1, 50)
    
    df = pd.DataFrame({
        "Elevación (m)": elevacion,
        "Inyector 1 (%)": inj_1,
        "Inyector 2 (%)": inj_2,
