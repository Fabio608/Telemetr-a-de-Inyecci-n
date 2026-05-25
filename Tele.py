import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# 1. CONFIGURACIÓN DE LA PÁGINA
# Esto fuerza el diseño a lo ancho de la pantalla y le da el título a la pestaña
st.set_page_config(page_title="Vigía Diesel Pro", layout="wide", initial_sidebar_state="expanded")

# 2. GENERACIÓN DE DATOS SIMULADOS (Para que veas cómo se moverán los gráficos)
# En el software real, estos datos vendrán del Teltonika y del archivo DEM
def generar_datos_simulados():
    tiempo = pd.date_range(start="2026-05-25", periods=50, freq="1min")
    
    # Simulamos el perfil de elevación (una subida)
    elevacion = np.linspace(100, 400, 50) + np.random.normal(0, 5, 50)
    
    # Simulamos inyectores. El Inyector 2 va a fallar cuando la elevación suba
    inj_1 = np.random.normal(1, 0.2, 50)
    inj_2 = np.where(elevacion > 250, np.random.normal(12, 2, 50), np.random.normal(1, 0.2, 50)) # Falla en subida
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
    
    # Selector de camión (Tus marcas de preferencia)
    camion_seleccionado = st.selectbox(
        "Seleccionar Unidad en Ruta:",
        ["Scania R450 - Dominio ABC123", "Volvo FH540 - Dominio DEF456", "Mack Anthem - Dominio GHI789"]
    )
    
    st.markdown("---")
    st.subheader("Estado General")
    st.error("🔴 ALERTA: Compensación Alta")
    st.write("**Unidad:**", camion_seleccionado)
    st.write("**Ubicación:** Ruta 3, km 1830")
    st.write("**Velocidad:** 65 km/h")
    
    st.markdown("---")
    st.button("Generar Informe PDF")

# 4. ÁREA PRINCIPAL (MAPA Y GRÁFICOS)
col1, col2 = st.columns([2, 1]) # El mapa ocupará el doble de ancho que los gráficos

with col1:
    st.subheader("📍 Mapeo de Estrés Mecánico en Tiempo Real")
    
    # Mapa oscuro profesional centrado en Comodoro Rivadavia
    m = folium.Map(location=[-45.8641, -67.4965], zoom_start=11, tiles="CartoDB dark_matter")
    
    # Dibujamos una línea de ruta simulada
    ruta_coords = [
        [-45.8641, -67.4965], [-45.8500, -67.5100], [-45.8300, -67.5300], 
        [-45.8100, -67.5400], [-45.7900, -67.5500]
    ]
    folium.PolyLine(ruta_coords, color="green", weight=4, opacity=0.7).add_to(m)
    
    # Marcador rojo simulando el camión en el punto de falla
    folium.CircleMarker(
        location=[-45.7900, -67.5500],
        radius=8,
        color="red",
        fill=True,
        fill_color="red",
        popup="Inyector 2 - Alerta"
    ).add_to(m)
    
    # Mostrar el mapa en Streamlit
    st_folium(m, width=800, height=450)

with col2:
    st.subheader("⚙️ Diagnóstico de Inyección")
    st.write("Caudal de compensación (%)")
    
    # Mostramos los gráficos de los inyectores
    # Notarás cómo el inyector 2 se dispara en la gráfica
    st.line_chart(datos_telemetria[["Inyector 1 (%)", "Inyector 2 (%)", "Inyector 3 (%)", "Inyector 4 (%)"]], height=200)
    
    st.markdown("---")
    st.subheader("⛰️ Perfil de Elevación (DEM)")
    st.write("Altitud sobre el nivel del mar (m)")
    
    # Gráfico del relieve en el mismo eje de tiempo
    st.area_chart(datos_telemetria["Elevación (m)"], color="#FFA500", height=150)
