import os
import json
import tempfile
from src.core import identify_type, get_file_signature, analyze_vulnerabilities, calculate_hashes
from src.cli import check_mismatch
from src.logger import logger

def run_evaluation():
    """
    Evalúa el rendimiento del agente contra un set de pruebas controladas.
    """
    logger.info("🚀 [bold cyan]Iniciando Evaluación del Agente Forense[/bold cyan]...")
    
    test_cases = [
        # Caso 1: Spoofing de Ejecutable
        {
            "name": "Spoofing EXE a JPG",
            "content": b"\x4D\x5A\x90\x00\x03\x00\x00\x00", # Firma de EXE
            "extension": ".jpg",
            "expected_mismatch": True,
            "expected_type": "Executable (EXE/DLL)"
        },
        # Caso 2: Ransomware Pattern
        {
            "name": "Detección de Ransomware (vssadmin)",
            "content": b"vssadmin.exe delete shadows /all /quiet",
            "extension": ".bat",
            "expected_vuln": "Borrado de Copias de Seguridad (Shadow Copies)"
        },
        # Caso 3: Persistencia en Registro
        {
            "name": "Detección de Persistencia (Run Keys)",
            "content": b"RegSetValueEx(hKey, 'Malware', 0, REG_SZ, 'C:\\malware.exe')",
            "extension": ".py",
            "expected_vuln": "Persistencia en Registro (Run Keys)"
        },
        # Caso 4: Archivo Legítimo (PNG)
        {
            "name": "Falso Positivo - PNG Real",
            "content": b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A", # Firma PNG
            "extension": ".png",
            "expected_mismatch": False,
            "expected_type": "PNG Image"
        }
    ]

    results = {"passed": 0, "failed": 0, "details": []}

    for case in test_cases:
        with tempfile.NamedTemporaryFile(suffix=case["extension"], delete=False) as tf:
            tf.write(case["content"])
            temp_path = tf.name

        try:
            # Análisis
            sig = get_file_signature(temp_path)
            type_info = identify_type(sig)
            is_mismatch = check_mismatch(temp_path, type_info)
            vulns = analyze_vulnerabilities(temp_path)
            
            # Verificación
            case_passed = True
            
            # Verificar Spoofing
            if "expected_mismatch" in case:
                if is_mismatch != case["expected_mismatch"]:
                    case_passed = False
            
            # Verificar Vulnerabilidades
            if "expected_vuln" in case:
                detected_vuln_names = [v["rule"] for v in vulns]
                if case["expected_vuln"] not in detected_vuln_names:
                    case_passed = False

            if case_passed:
                results["passed"] += 1
                logger.info(f"✅ [green]PASS:[/green] {case['name']}")
            else:
                results["failed"] += 1
                logger.error(f"❌ [red]FAIL:[/red] {case['name']}")

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # Resumen Final
    total = results["passed"] + results["failed"]
    accuracy = (results["passed"] / total) * 100 if total > 0 else 0
    
    logger.info(f"\n[bold blue]Resultados de la Evaluación:[/bold blue]")
    logger.info(f"📊 Accuracy: [bold yellow]{accuracy:.2f}%[/bold yellow]")
    logger.info(f"✅ Aprobados: {results['passed']}")
    logger.info(f"❌ Fallidos: {results['failed']}")

if __name__ == "__main__":
    run_evaluation()
