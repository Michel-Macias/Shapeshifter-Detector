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

# Inyección de Estilos Globales (Glassmorphism & Cyber Theme - OPTIMIZADO PARA LEGIBILIDAD)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
    
    /* Estética General Dark Crypto/Hacker - MEJORADO */
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a1929 100%);
        color: #f0f4f8;
        font-family: 'Inter', sans-serif;
    }
    
    /* Personalización de Sidebar - MÁS CONTRASTE */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1b2a 0%, #1b263b 100%);
        border-right: 2px solid #00d4ff;
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e6ed !important;
        font-size: 16px !important;
    }
    
    /* Estilo de Tarjetas de Métricas - GIGANTES Y LEGIBLES */
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif;
        font-weight: 900 !important;
        font-size: 3rem !important;
        color: #00f2fe !important;
        text-shadow: 0 0 20px rgba(0, 242, 254, 0.5);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.1rem !important;
        color: #8899a6 !important;
        font-weight: 600 !important;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
    }
    
    /* Contenedores con Efecto Cristal - MÁS VISIBLE */
    .css-1r6p783, .stTabs {
        background: rgba(255, 255, 255, 0.08) !important;
        padding: 25px !important;
        border-radius: 15px !important;
        border: 2px solid rgba(0, 212, 255, 0.3) !important;
        backdrop-filter: blur(10px);
    }

    /* Títulos Secciones - MÁS GRANDES */
    h1 {
        font-family: 'Inter', sans-serif;
        font-size: 3rem !important;
        font-weight: 900 !important;
        color: #00f2fe !important;
        text-shadow: 0 0 30px rgba(0, 242, 254, 0.6);
        letter-spacing: -1px;
    }
    
    h2 {
        font-family: 'Inter', sans-serif;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #00d4ff !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #4facfe !important;
    }
    
    /* Tablas - MUCHO MÁS LEGIBLES */
    [data-testid="stDataFrame"] {
        font-size: 1.1rem !important;
    }
    
    [data-testid="stDataFrame"] td {
        padding: 12px !important;
        color: #f0f4f8 !important;
        background: rgba(15, 30, 50, 0.6) !important;
        border-bottom: 1px solid rgba(0, 212, 255, 0.2) !important;
    }
    
    [data-testid="stDataFrame"] th {
        padding: 15px !important;
        background: rgba(0, 212, 255, 0.2) !important;
        color: #00f2fe !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Texto general - AUMENTADO */
    p, div, span, label {
        font-size: 1.1rem !important;
        line-height: 1.7 !important;
        color: #e0e6ed !important;
    }
    
    /* Status Alerts - MÁS VISIBLE */
    .status-alert {
        padding: 1.5rem !important;
        border-radius: 12px !important;
        margin-bottom: 1.5rem !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .status-critical {
        background: rgba(255, 75, 75, 0.25) !important;
        border: 3px solid #ff4b4b !important;
        color: #ff6b6b !important;
        box-shadow: 0 0 25px rgba(255, 75, 75, 0.4);
    }
    .status-ok {
        background: rgba(0, 255, 221, 0.15) !important;
        border: 3px solid #00ffdd !important;
        color: #00ffdd !important;
        box-shadow: 0 0 25px rgba(0, 255, 221, 0.3);
    }
    
    /* Tabs - MÁS CONTRASTE */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #8899a6 !important;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px 8px 0 0;
        padding: 12px 24px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, rgba(0, 242, 254, 0.2) 0%, rgba(0, 212, 255, 0.1) 100%) !important;
        color: #00f2fe !important;
        border-bottom: 3px solid #00f2fe !important;
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
