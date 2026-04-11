import streamlit as st
import json
import pandas as pd
import os
from src.ui_components import show_module_intro
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_extras.metric_cards import style_metric_cards

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

with st.sidebar:
    st.header("📂 Carga de Inteligencia")
    uploaded_file = st.file_uploader("Subir reporte JSON del Agente", type=["json"])
    st.markdown("---")
    st.info("💡 Consejo: Analiza archivos con `main.py` y carga el reporte generado aquí.")

if uploaded_file:
    data = load_data(uploaded_file)
    memory_data = load_memory()
    
    if data:
        df = pd.DataFrame(data)
        
        # ... (Metrics calculation code stays the same) ...
        
        st.markdown("---")

        tab1, tab2, tab3, tab4 = st.tabs(["📊 Estadísticas", "⚔️ Seguridad", "🧠 Inteligencia", "📂 Vista de Datos"])
        
        # ... (Tab 1 and Tab 2 code stay the same) ...

        # Estilizar las métricas visuales con Extras
        style_metric_cards(background_color="rgba(255,255,255,0.05)", border_left_color="#00f2fe", border_color="rgba(0, 212, 255, 0.3)", box_shadow=False)

        with tab3:
            st.subheader("🧠 Grafo de Conocimiento (Correlaciones & IoCs)")
            if memory_data:
                nodes = []
                edges = []
                
                analyses = memory_data.get("analyses", {})
                global_iocs = memory_data.get("global_iocs", {})
                
                # Crear Nodos para Archivos
                for file_hash, file_info in analyses.items():
                    score = file_info.get("threat_score", 0)
                    color = "#00ffdd" if score < 40 else "#ff4b4b"
                    nodes.append(Node(id=file_hash, 
                                      label=file_info["filename"][:20], 
                                      size=25, 
                                      color=color,
                                      title=f"Score: {score}"))
                                      
                # Crear Nodos y Aristas para IoCs
                ioc_colors = {"ips": "#ffb800", "domains": "#b800ff", "urls": "#ff00b8"}
                
                for ioc_type, items in global_iocs.items():
                    color = ioc_colors.get(ioc_type, "#00d4ff")
                    for item, hashes in items.items():
                        ioc_id = f"ioc_{item}"
                        # Anadir el nodo IoC
                        nodes.append(Node(id=ioc_id, label=str(item)[:25], size=15, color=color, shape="hexagon"))
                        # Relacionar el IoC con el archivo
                        for h in hashes:
                            if h in analyses:
                                edges.append(Edge(source=h, target=ioc_id, color="rgba(0, 212, 255, 0.5)", width=2))

                # Configurar el motor de render de PyVis / Agraph
                config = Config(width="100%",
                                height=600,
                                directed=False,
                                physics=True,
                                hierarchical=False,
                                nodeHighlightBehavior=True,
                                highlightColor="#F7A7A6",
                                collapsible=True)

                if nodes:
                    st.markdown("""<p style="color: #8899a6; font-size:16px;">
                    🟢 Archivo Limpio | 🔴 Amenaza | 🟡 IP | 🟣 Dominio/URL <br>
                    Arrastra los nodos para explorar la topología de la amenaza.
                    </p>""", unsafe_allow_html=True)
                    
                    agraph(nodes=nodes, edges=edges, config=config)
                else:
                    st.info("No hay suficientes datos para generar el grafo 3D.")
            else:
                st.warning("No se encontró el archivo de memoria global para mapear grafos.")

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
