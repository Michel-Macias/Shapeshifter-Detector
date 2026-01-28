import streamlit as st

def show_module_intro():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;600;800;900&display=swap');

        .intro-container {
            background: linear-gradient(135deg, rgba(10, 25, 41, 0.95) 0%, rgba(20, 80, 110, 0.5) 100%);
            padding: 4rem 3rem;
            border-radius: 20px;
            border: 2px solid rgba(0, 255, 255, 0.4);
            box-shadow: 0 8px 40px 0 rgba(0, 0, 0, 0.9);
            margin-bottom: 3rem;
            text-align: center;
            backdrop-filter: blur(15px);
            animation: fadeIn 1.2s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .intro-title {
            font-family: 'Inter', sans-serif;
            font-weight: 900;
            font-size: 4.5rem;
            background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.5rem;
            letter-spacing: -2px;
            text-shadow: 0 0 40px rgba(0, 242, 254, 0.6);
        }

        .intro-subtitle {
            font-family: 'JetBrains Mono', monospace;
            color: #00d4ff;
            font-size: 1.4rem;
            text-transform: uppercase;
            letter-spacing: 6px;
            margin-bottom: 2.5rem;
            font-weight: 700;
        }

        .intro-description {
            font-family: 'Inter', sans-serif;
            color: #f0f4f8;
            font-size: 1.5rem;
            font-weight: 500;
            max-width: 900px;
            margin: 0 auto 3rem auto;
            line-height: 1.8;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 2rem;
            margin-top: 2.5rem;
        }

        .feature-item {
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            border: 2px solid rgba(0, 255, 255, 0.2);
            transition: all 0.3s ease;
        }

        .feature-item:hover {
            transform: translateY(-8px);
            background: rgba(255, 255, 255, 0.15);
            border-color: #00f2fe;
            box-shadow: 0 10px 30px rgba(0, 242, 254, 0.3);
        }

        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }

        .feature-text {
            color: #fff;
            font-weight: 700;
            font-size: 1.2rem;
            font-family: 'Inter', sans-serif;
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
