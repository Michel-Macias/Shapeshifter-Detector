import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(page_title="Identify-Files Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ Identify-Files: Dashboard de Seguridad")
st.markdown("Visualiza y analiza los reportes generados por la herramienta de identificación de archivos.")

# Sidebar para subir archivo
st.sidebar.header("Cargar Reporte")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo 'reporte.json'", type=["json"])

if uploaded_file is not None:
    try:
        data = json.load(uploaded_file)
        df = pd.DataFrame(data)
        
        # Métricas Generales
        total_files = len(df)
        mismatches = df[df['extension_mismatch'] == True].shape[0]
        high_entropy = df[df['entropy'] > 7.5].shape[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Archivos Analizados", total_files)
        col2.metric("Alertas de Spoofing", mismatches, delta_color="inverse")
        col3.metric("Alta Entropía (>7.5)", high_entropy, delta_color="inverse")
        
        st.divider()
        
        # Gráficos
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Distribución por Tipo de Archivo")
            type_counts = df['detected_type'].value_counts()
            st.bar_chart(type_counts)
            
        with col_chart2:
            st.subheader("Distribución de Entropía")
            st.line_chart(df['entropy'])

        st.divider()

        # Tabla de Alertas (Prioridad)
        st.subheader("🚨 Alertas de Seguridad (Spoofing Detected)")
        if mismatches > 0:
            st.error(f"Se encontraron {mismatches} archivos con discrepancia de extensión.")
            st.dataframe(df[df['extension_mismatch'] == True][['path', 'detected_type', 'signature']], use_container_width=True)
        else:
            st.success("No se detectaron intentos de spoofing.")

        # Tabla Completa
        with st.expander("Ver Reporte Completo"):
            st.dataframe(df)
            
    except Exception as e:
        st.error(f"Error al procesar el archivo JSON: {e}")
else:
    st.info("Por favor, sube un archivo JSON generado por la herramienta (ej. `reporte.json`) para ver el análisis.")
    
    st.markdown("""
    ### Cómo generar un reporte:
    Ejecuta el siguiente comando en tu terminal:
    ```bash
    python3 main.py /ruta/a/escanear --output reporte.json
    ```
    """)
