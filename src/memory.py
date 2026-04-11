import os
import sqlite3
import json
import threading
from src.logger import logger

# Rutas por defecto
REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
DB_PATH = os.path.join(REPORTS_DIR, 'memory.db')
JSON_PATH = os.path.join(REPORTS_DIR, 'memory.json')

class AgentKnowledgeBase:
    """
    Gestiona la persistencia bajo un motor SQLite (ACID Compliance)
    para tolerar alta concurrencia. Soporta exportación a JSON en caliente.
    """
    def __init__(self, db_path=DB_PATH, json_path=JSON_PATH):
        self.db_path = db_path
        self.json_path = json_path
        self.lock = threading.Lock()
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS analyses (
                        sha256 TEXT PRIMARY KEY,
                        filename TEXT,
                        threat_score REAL,
                        timestamp TEXT
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS global_iocs (
                        ioc_type TEXT,
                        ioc_value TEXT,
                        sha256 TEXT,
                        UNIQUE(ioc_type, ioc_value, sha256)
                    )
                ''')
                conn.commit()

    def get_analysis(self, sha256):
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT filename, threat_score FROM analyses WHERE sha256 = ?", (sha256,))
                row = cursor.fetchone()
                if row:
                    return {"filename": row[0], "threat_score": row[1]}
        return None

    def learn_analysis(self, sha256, filepath, results):
        filename = os.path.basename(filepath)
        score = results.get("threat_score", 0)
        timestamp = results.get("timestamp", "")
        
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO analyses (sha256, filename, threat_score, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (sha256, filename, score, timestamp))
                
                if "iocs" in results:
                    for ioc_type, items in results["iocs"].items():
                        for item in items:
                            cursor.execute('''
                                INSERT OR IGNORE INTO global_iocs (ioc_type, ioc_value, sha256)
                                VALUES (?, ?, ?)
                            ''', (ioc_type, item, sha256))
                conn.commit()
                
            # Exportar el volcado para compatibilidad con el Dashboard
            self._export_to_json_unlocked()

    def find_correlations(self, iocs):
        correlations = {}
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for ioc_type, items in iocs.items():
                    for item in items:
                        cursor.execute("SELECT sha256 FROM global_iocs WHERE ioc_type = ? AND ioc_value = ?", (ioc_type, item))
                        hashes = [row[0] for row in cursor.fetchall()]
                        if hashes:
                            correlations[item] = hashes
        return correlations

    def _export_to_json_unlocked(self):
        """Volcado rápido al disco en schema JSON clásico para Streamlit."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT sha256, filename, threat_score, timestamp FROM analyses")
                analyses_dict = {}
                for row in cursor.fetchall():
                    analyses_dict[row[0]] = {"filename": row[1], "threat_score": row[2], "timestamp": row[3]}
                
                cursor.execute("SELECT ioc_type, ioc_value, sha256 FROM global_iocs")
                iocs_dict = {}
                for row in cursor.fetchall():
                    i_type, i_val, h = row
                    if i_type not in iocs_dict:
                        iocs_dict[i_type] = {}
                    if i_val not in iocs_dict[i_type]:
                        iocs_dict[i_type][i_val] = []
                    iocs_dict[i_type][i_val].append(h)
                    
            state = {"analyses": analyses_dict, "global_iocs": iocs_dict}
            
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)
        except Exception as e:
            logger.error(f"Falla crítica en reconstrucción de JSON Dashboard: {e}")

# Instancia global (Thread Safe)
memory = AgentKnowledgeBase()
