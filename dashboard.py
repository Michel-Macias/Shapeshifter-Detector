import streamlit as st
import json
import pandas as pd
import os
from src.ui_components import show_module_intro

# Configuración de página con estética Premium
st.set_page_config(
    page_title="Identify-Files | Forensic Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de Estilos Globales (Glassmorphism & Cyber Theme)
st.markdown("""
    <style>
    /* Estética General Dark Crypto/Hacker */
    .stApp {
        background-color: #060c13;
        color: #e0e6ed;
    }
    
    /* Personalización de Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a1118;
        border-right: 1px solid rgba(0, 255, 255, 0.1);
    }
    
    /* Estilo de Tarjetas de Métricas */
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        color: #00f2fe;
    }
    
    /* Contenedores con Efecto Cristal */
    .css-1r6p783, .stTabs {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Títulos Secciones */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        letter-spacing: -0.5px;
    }
    
    .status-alert {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .status-critical {
        background: rgba(255, 75, 75, 0.1);
        border: 1px solid #ff4b4b;
        color: #ff4b4b;
    }
    .status-ok {
        background: rgba(0, 255, 221, 0.1);
        border: 1px solid #00ffdd;
        color: #00ffdd;
    }
    </style>
""", unsafe_allow_html=True)

# Lógica de carga de datos
def load_data(uploaded_file):
    try:
        return json.load(uploaded_file)
    except Exception as e:
        st.error(f"Error parseando JSON: {e}")
        return None

# Interface Principal
show_module_intro()

st.sidebar.markdown("### 📥 Ingesta de Datos")
uploaded_file = st.sidebar.file_uploader("Cargar reporte_forense.json", type=["json"])

if uploaded_file:
    data = load_data(uploaded_file)
    if data:
        df = pd.DataFrame(data)
        
        # Procesar vulnerabilidades (aplanar para conteo)
        all_vulns = []
        for v_list in df.get('vulnerabilities', []):
            if isinstance(v_list, list):
                all_vulns.extend(v_list)
        
        total_files = len(df)
        mismatches = df[df['extension_mismatch'] == True].shape[0]
        critical_vulns = len([v for v in all_vulns if v.get('severity') == 'Crítica'])
        
        # Dashboard de Métricas con diseño Premium
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("🕵️ Archivos", total_files)
        with m_col2:
            st.metric("🎭 Spoofing", mismatches, delta="- Alerta -" if mismatches > 0 else "Limpio")
        with m_col3:
            st.metric("🚫 Amenazas SAST", len(all_vulns))
        with m_col4:
            st.metric("💥 Riesgo Crítico", critical_vulns)

        st.markdown("---")

        tab1, tab2, tab3 = st.tabs(["📊 Análisis Estadístico", "⚔️ Seguridad & SAST", "📂 Vista de Datos"])
        
        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Tipología de Archivos")
                st.bar_chart(df['detected_type'].value_counts(), use_container_width=True)
            with c2:
                st.subheader("Mapa de Entropía (Confidencialidad)")
                st.area_chart(df['entropy'], use_container_width=True)
        
        with tab2:
            st.subheader("🛡️ Auditoría de Seguridad Automatizada")
            
            # Sub-sección de Spoofing
            if mismatches > 0:
                st.markdown('<div class="status-alert status-critical">DETECTADOS INTENTOS DE SPOOFING DE EXTENSIÓN</div>', unsafe_allow_html=True)
                st.dataframe(df[df['extension_mismatch'] == True][['path', 'detected_type', 'signature']], use_container_width=True)
            else:
                st.markdown('<div class="status-alert status-ok">ESTRUCTURA DE EXTENSIONES VERIFICADA Y SEGURA</div>', unsafe_allow_html=True)

            # Nueva Sección de Vulnerabilidades SAST
            st.markdown("### 🚩 Hallazgos de Vulnerabilidades en Código")
            vuln_data = []
            for _, row in df.iterrows():
                if 'vulnerabilities' in row and row['vulnerabilities']:
                    for v in row['vulnerabilities']:
                        vuln_data.append({
                            "Archivo": os.path.basename(row['path']),
                            "Regla": v['rule'],
                            "Severidad": v['severity'],
                            "Línea": v['line'],
                            "Snippet": v['content']
                        })
            
            if vuln_data:
                vuln_df = pd.DataFrame(vuln_data)
                # Colorear severidad
                def color_severity(val):
                    color = '#ff4b4b' if val == 'Crítica' else '#ffa500' if val == 'Alta' else '#00f2fe'
                    return f'color: {color}; font-weight: bold'
                
                st.table(vuln_df.style.applymap(color_severity, subset=['Severidad']))
            else:
                st.info("No se han detectado patrones de vulnerabilidades en los scripts analizados.")

        with tab3:
            st.subheader("Detalle Forense Completo")
            st.dataframe(df, use_container_width=True)

else:
    st.markdown("""
        <div style='text-align: center; padding: 50px; background: rgba(255,255,255,0.02); border-radius: 15px; border: 1px dashed rgba(255,255,255,0.1);'>
            <h2 style='color: #00f2fe;'>Esperando Reporte de Inteligencia...</h2>
            <p style='color: #8899a6;'>Sube un archivo <code>reporte_forense.json</code> en el panel lateral para iniciar la visualización avanzada.</p>
        </div>
    """, unsafe_allow_html=True)
