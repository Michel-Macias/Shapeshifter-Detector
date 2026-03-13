import json
import os
from src.logger import logger

# Ruta por defecto para la base de conocimientos
MEMORY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'memory.json')

class AgentKnowledgeBase:
    """
    Gestiona la persistencia y correlación de hallazgos del agente forense.
    Permite deduplicar análisis y encontrar patrones entre archivos.
    """
    def __init__(self, memory_path=MEMORY_PATH):
        self.memory_path = memory_path
        self.data = self._load_memory()

    def _load_memory(self):
        """Carga la base de conocimientos desde el archivo JSON."""
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                logger.error(f"Error cargando memoria desde [bold red]{self.memory_path}[/bold red]. Reiniciando...")
                return {"analyses": {}, "global_iocs": {}}
        return {"analyses": {}, "global_iocs": {}}

    def save_memory(self):
        """Guarda el estado actual en el disco."""
        try:
            os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
            with open(self.memory_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            logger.error(f"No se pudo persistir la memoria: {e}")

    def get_analysis(self, sha256):
        """Recupera un análisis previo si existe."""
        return self.data["analyses"].get(sha256)

    def learn_analysis(self, sha256, filepath, results):
        """
        Registra un nuevo análisis y actualiza la lista global de IoCs (Indicadores de Compromiso).
        """
        # Guardar análisis individual
        self.data["analyses"][sha256] = {
            "filename": os.path.basename(filepath),
            "timestamp": results.get("timestamp"),
            "threat_score": results.get("threat_score", 0),
            "findings": results.get("findings", [])
        }

        # Correlación de IoCs (IPs, URLs, etc.)
        # Si el análisis tiene strings sospechosas, las guardamos globalmente vinculadas a este hash
        if "iocs" in results:
            for ioc_type, items in results["iocs"].items():
                if ioc_type not in self.data["global_iocs"]:
                    self.data["global_iocs"][ioc_type] = {}
                
                for item in items:
                    if item not in self.data["global_iocs"][ioc_type]:
                        self.data["global_iocs"][ioc_type][item] = []
                    
                    if sha256 not in self.data["global_iocs"][ioc_type][item]:
                        self.data["global_iocs"][ioc_type][item].append(sha256)

        self.save_memory()

    def find_correlations(self, iocs):
        """
        Busca si alguno de los IoCs encontrados ya ha sido visto en otros archivos.
        """
        correlations = {}
        for ioc_type, items in iocs.items():
            for item in items:
                known_hashes = self.data["global_iocs"].get(ioc_type, {}).get(item, [])
                if known_hashes:
                    correlations[item] = known_hashes
        return correlations

# Instancia global para facilitar el uso
memory = AgentKnowledgeBase()
