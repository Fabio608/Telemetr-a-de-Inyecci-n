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
        "Inyector 3 (%)": inj_3,
        "Inyector 4 (%)": inj_4
    }, index=tiempo)
    return df

datos_telemetria = generar_datos_simulados()

# 3. PANEL LATERAL (BARRA DE CONTROL BOMBISTA)
with st.sidebar:
    st.title("Vigía Diesel Pro")
    st.markdown("---")
    st.subheader("Flota Activa")
    
    camion_seleccionado = st.selectbox(
        "Seleccionar Unidad en Ruta:",
        ["Scania R450 - Dominio ABC123", "Volvo FH540 - Dominio DEF456", "Mack Anthem - Dominio GHI789"]
    )
    
    st.markdown("---")
    st.subheader("Estado General")
    st.error("🔴 ALERTA: Compensación Alta en Subida")
    st.write("**Unidad:**", camion_seleccionado)
    st.write("**Ubicación:** Ruta 3
