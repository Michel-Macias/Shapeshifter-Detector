import os
import requests
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()

VT_API_KEY = os.getenv("VT_API_KEY")

class CTI_Engine:
    def __init__(self):
        self.vt_url = "https://www.virustotal.com/api/v3/files/"
        self.headers = {
            "accept": "application/json",
            "x-apikey": VT_API_KEY
        }

    def check_hash_vt(self, file_hash):
        """
        Consulta el hash en VirusTotal.
        Usa manejo de excpeciones para funcionar offline o sin clave.
        """
        if not VT_API_KEY:
            # Operando en modo silencioso si no hay API KEY
            return None
            
        try:
            response = requests.get(f"{self.vt_url}{file_hash}", headers=self.headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                malicious = stats.get("malicious", 0)
                return {
                    "malicious_hits": malicious,
                    "total_scans": sum(stats.values()),
                    "permalink": f"https://www.virustotal.com/gui/file/{file_hash}"
                }
            elif response.status_code == 404:
                # Hash no encontrado en VT
                return {"malicious_hits": 0, "total_scans": 0, "status": "Not Found"}
            else:
                logger.warning(f"Error VT API ({response.status_code}): {response.text}")
                return None
        except Exception as e:
            logger.error(f"Fallo de resolución a VT: {e}")
            return None
