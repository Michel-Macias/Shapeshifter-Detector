import sqlite3
import streamlit as st
import json
import pandas as pd
import os
from src.ui_components import show_module_intro
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_extras.metric_cards import style_metric_cards

# Configuración de página con estética Premium
st.set_page_config(
    page_title="Shapeshifter Forensic Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de Estilos Globales
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
    .stApp { background: linear-gradient(135deg, #000000 0%, #0a1929 100%); color: #f0f4f8; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d1b2a 0%, #1b263b 100%); border-right: 2px solid #00d4ff; }
    [data-testid="stMetricValue"] { color: #00f2fe !important; text-shadow: 0 0 20px rgba(0, 242, 254, 0.5); }
    .css-1r6p783, .stTabs { background: rgba(255, 255, 255, 0.08) !important; padding: 25px !important; border-radius: 15px !important; border: 2px solid rgba(0, 212, 255, 0.3) !important; backdrop-filter: blur(10px); }
    </style>
""", unsafe_allow_html=True)

def load_data(uploaded_file):
    try: return json.load(uploaded_file)
    except: return None

def load_data_from_db():
    db_path = os.path.join('reports', 'memory.db')
    if not os.path.exists(db_path): return None
    try:
        with sqlite3.connect(db_path) as conn:
            return pd.read_sql_query("SELECT * FROM analyses ORDER BY timestamp DESC LIMIT 1000", conn)
    except: return None

def load_memory():
    db_path = os.path.join('reports', 'memory.db')
    if not os.path.exists(db_path): return None
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT sha256, filename, threat_score FROM analyses WHERE threat_score > 20 LIMIT 100")
            analyses = {row['sha256']: dict(row) for row in cursor.fetchall()}
            cursor = conn.execute("SELECT ioc_type, ioc_value, sha256 FROM global_iocs WHERE sha256 IN (SELECT sha256 FROM analyses WHERE threat_score > 20) LIMIT 500")
            iocs = {}
            for row in cursor.fetchall():
                t, v, h = row['ioc_type'], row['ioc_value'], row['sha256']
                if t not in iocs: iocs[t] = {}
                if v not in iocs[t]: iocs[t][v] = []
                iocs[t][v].append(h)
            return {"analyses": analyses, "global_iocs": iocs}
    except: return None

def normalize_dataframe(df):
    """Garantiza que el DataFrame tenga las columnas necesarias para el Dashboard."""
    if df is None or df.empty: return df
    
    # Mapeo de nombres comunes (JSON vs DB)
    rename_map = {
        'path': 'filename',
        'malicious_hits': 'cti_hits'
    }
    df = df.rename(columns=rename_map)
    
    # Asegurar columnas críticas con valores por defecto
    required_cols = {
        'threat_score': 0,
        'cti_hits': 0,
        'filename': 'Unknown',
        'sha256': 'N/A'
    }
    
    for col, default in required_cols.items():
        if col not in df.columns:
            df[col] = default
            
    return df

show_module_intro()

db_df = normalize_dataframe(load_data_from_db())
memory_data = load_memory()

with st.sidebar:
    st.header("📂 Origen de Datos")
    source = st.radio("Cargar desde:", ["Base de Datos (Global)", "Reporte JSON (Manual)"])
    df = None
    if source == "Reporte JSON (Manual)":
        up = st.file_uploader("Subir JSON", type=["json"])
        if up: 
            raw = load_data(up)
            if raw: 
                df = normalize_dataframe(pd.DataFrame(raw))
    else:
        df = db_df
    st.markdown("---")
    if db_df is not None: st.success("🟢 DB Conectada")
    else: st.warning("🟡 DB no encontrada")

if df is not None:
    # Métricas
    m1, m2, m3 = st.columns(3)
    m1.metric("Archivos", len(df))
    m2.metric("Alertas", len(df[df['threat_score'] > 60]))
    m3.metric("Promedio Riesgo", f"{df['threat_score'].mean():.1f}")
    style_metric_cards()

    tabs = st.tabs(["📊 Análisis", "⚔️ Riesgos", "🧠 Grafo", "📂 Crudo"])
    
    with tabs[0]:
        st.subheader("Distribución de Amenazas")
        if 'threat_score' in df.columns:
            st.bar_chart(df['threat_score'])
            
    with tabs[1]:
        st.subheader("Top Amenazas Detectadas")
        st.table(df[df['threat_score'] > 40][['filename', 'threat_score']].sort_values(by='threat_score', ascending=False).head(10))

    with tabs[2]:
        st.subheader("Grafo Relacional (Top Amenazas)")
        if memory_data:
            nodes, edges = [], []
            an = memory_data['analyses']
            for h, info in an.items():
                nodes.append(Node(id=h, label=info['filename'][:15], size=20, color="#ff4b4b"))
            
            iocs = memory_data['global_iocs']
            for t, vals in iocs.items():
                for v, hs in vals.items():
                    iid = f"i_{v}"
                    nodes.append(Node(id=iid, label=v[:15], size=10, color="#00f2fe", shape="diamond"))
                    for h in hs:
                        if h in an: edges.append(Edge(source=h, target=iid))
            
            if nodes:
                config = Config(width="100%", height=500, physics=False)
                agraph(nodes=nodes, edges=edges, config=config)
            else: st.info("Escaneos limpios. No hay grafo que mostrar.")

    with tabs[3]:
        st.dataframe(df, width="stretch")
else:
    st.info("⚡ Inicia un escaneo o carga un reporte para visualizar resultados.")
