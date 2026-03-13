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

def load_memory():
    """Carga la base de conocimientos desde el disco."""
    path = os.path.join('reports', 'memory.json')
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return None

# Interface Principal
show_module_intro()

# ... (Sidebar code stays the same) ...

if uploaded_file:
    data = load_data(uploaded_file)
    memory_data = load_memory()
    
    if data:
        df = pd.DataFrame(data)
        
        # ... (Metrics calculation code stays the same) ...
        
        st.markdown("---")

        tab1, tab2, tab3, tab4 = st.tabs(["📊 Estadísticas", "⚔️ Seguridad", "🧠 Inteligencia", "📂 Vista de Datos"])
        
        # ... (Tab 1 and Tab 2 code stay the same) ...

        with tab3:
            st.subheader("🧠 Base de Conocimiento del Agente")
            if memory_data:
                col_m1, col_m2 = st.columns([1, 2])
                
                with col_m1:
                    st.markdown("#### 📝 Archivos Conocidos")
                    analyses = memory_data.get("analyses", {})
                    st.write(f"El agente ha analizado **{len(analyses)}** archivos únicos.")
                    
                    # Mostrar tabla de archivos conocidos con Score
                    memo_df = pd.DataFrame([
                        {"Hash": h[:16]+"...", "Archivo": v["filename"], "Riesgo": v.get("threat_score", 0)} 
                        for h, v in analyses.items()
                    ])
                    st.dataframe(memo_df, use_container_width=True)

                with col_m2:
                    st.markdown("#### 🔗 Red de Correlaciones (IoCs)")
                    global_iocs = memory_data.get("global_iocs", {})
                    
                    ioc_rows = []
                    for ioc_type, items in global_iocs.items():
                        for item, hashes in items.items():
                            if len(hashes) > 1: # Solo mostrar si hay correlación
                                ioc_rows.append({
                                    "Tipo": ioc_type.upper(),
                                    "IoC": item,
                                    "Repeticiones": len(hashes),
                                    "Hashes Vinculados": ", ".join([h[:8] for h in hashes])
                                })
                    
                    if ioc_rows:
                        st.table(pd.DataFrame(ioc_rows))
                    else:
                        st.info("No hay correlaciones cruzadas detectadas todavía. Analiza más archivos para poblar la memoria.")

            else:
                st.warning("No se encontró el archivo de memoria del agente en `reports/memory.json`.")

        with tab4:
            st.subheader("Detalle Forense Completo")
            st.dataframe(df, use_container_width=True)

else:
    st.markdown("""
        <div style='text-align: center; padding: 50px; background: rgba(255,255,255,0.02); border-radius: 15px; border: 1px dashed rgba(255,255,255,0.1);'>
            <h2 style='color: #00f2fe;'>Esperando Reporte de Inteligencia...</h2>
            <p style='color: #8899a6;'>Sube un archivo <code>reporte_forense.json</code> en el panel lateral para iniciar la visualización avanzada.</p>
        </div>
    """, unsafe_allow_html=True)
