import streamlit as st

def show_module_intro():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@300;600;800&display=swap');

        .intro-container {
            background: linear-gradient(135deg, rgba(10, 25, 41, 0.9) 0%, rgba(20, 80, 110, 0.4) 100%);
            padding: 3rem;
            border-radius: 20px;
            border: 1px solid rgba(0, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
            margin-bottom: 2rem;
            text-align: center;
            backdrop-filter: blur(10px);
            animation: fadeIn 1.2s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .intro-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 3.5rem;
            background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            letter-spacing: -1px;
        }

        .intro-subtitle {
            font-family: 'JetBrains Mono', monospace;
            color: #00d4ff;
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 4px;
            margin-bottom: 2rem;
        }

        .intro-description {
            font-family: 'Outfit', sans-serif;
            color: #e0e6ed;
            font-size: 1.25rem;
            max-width: 800px;
            margin: 0 auto 2.5rem auto;
            line-height: 1.6;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }

        .feature-item {
            padding: 1rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            border: 1px solid rgba(0, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .feature-item:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.1);
            border-color: #00f2fe;
        }

        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
            display: block;
        }

        .feature-text {
            color: #fff;
            font-weight: 600;
            font-family: 'Outfit', sans-serif;
        }
        </style>

        <div class="intro-container">
            <div class="intro-title">SHAPESHIFTER DETECTOR</div>
            <div class="intro-subtitle">Advanced Forensic Intelligence</div>
            <p class="intro-description">
                Revela la verdadera naturaleza de tus archivos. Una suite forense de alto impacto diseñada para detectar spoofing, anomalías binarias y vulnerabilidades críticas en milisegundos.
            </p>
            <div class="feature-grid">
                <div class="feature-item">
                    <span class="feature-icon">🔍</span>
                    <span class="feature-text">Magic Numbers Identification</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🛡️</span>
                    <span class="feature-text">SAST Security Auditing</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">⚡</span>
                    <span class="feature-text">O(1) Optimized Engine</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">📊</span>
                    <span class="feature-text">Deep Entropy Analysis</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
