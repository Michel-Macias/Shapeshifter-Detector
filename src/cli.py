import argparse
import os
import json
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import track
from src.core import (
    get_file_signature, identify_type, calculate_hashes, 
    calculate_entropy, extract_strings, identify_iocs, analyze_vulnerabilities,
    analyze_pe_headers
)
from src.memory import memory
from src.logger import logger
from src.cti_integration import CTI_Engine
from src.report_generator import generate_pdf_report

console = Console()
print_lock = threading.Lock()
cti_engine = CTI_Engine()

def check_mismatch(filepath, detected_type_info):
    """
    Verifica si la extensión del archivo coincide con las extensiones esperadas para el tipo detectado.
    Devuelve True si hay una discrepancia (posible spoofing), False si todo está bien.
    """
    if not detected_type_info:
        return False
        
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    
    expected_extensions = detected_type_info.get('extensions', [])
    
    # Si la extensión actual NO está en la lista de esperadas, es una discrepancia
    if ext not in expected_extensions:
        return True
    return False

def scan_file(filepath, report_list=None):
    """
    Escanea un archivo individual y muestra los resultados usando Rich.
    Integra la Memoria del Agente para deduplicación y correlación de IoCs.
    """
    # 1. Calcular hashes primero para consultar la Memoria
    hashes = calculate_hashes(filepath)
    if not hashes:
        return
    
    sha256 = hashes['sha256']
    
    # 2. Consultar Memoria (Deduplicación)
    previous_analysis = memory.get_analysis(sha256)
    if previous_analysis:
        console.print(Panel(
            f"🧠 [bold cyan]Agente:[/bold cyan] Ya analicé este archivo anteriormente.\n"
            f"📅 [dim]Fecha:[/dim] {previous_analysis.get('timestamp')}\n"
            f"📊 [dim]Resultado:[/dim] {previous_analysis.get('filename')}",
            title="[bold blue]Conocimiento Previo[/bold blue]", border_style="cyan"
        ))

    # 3. Análisis Forense Completo
    signature = get_file_signature(filepath)
    type_info = identify_type(signature)
    entropy = calculate_entropy(filepath)
    strings = extract_strings(filepath)
    iocs = identify_iocs(strings)
    vulnerabilities = analyze_vulnerabilities(filepath)
    vulnerabilities.extend(analyze_pe_headers(filepath)) # Añadimos detección PE
    
    # Integración CTI (VirusTotal)
    cti_data = cti_engine.check_hash_vt(sha256)
    
    # Buscar correlaciones en la memoria global
    correlations = memory.find_correlations(iocs)
    
    file_type = type_info['type'] if type_info else "Desconocido"
    is_mismatch = check_mismatch(filepath, type_info)
    
    # Calcular un "Threat Score" simple para la memoria (MODO PARANOIA MAXIMA)
    threat_score = 0
    if is_mismatch: threat_score += 85
    if not type_info: threat_score += 65 # Alto riesgo si es desconocido
    if entropy > 7.5: threat_score += 25
    if vulnerabilities: threat_score += 35
    if correlations: threat_score += 15 * len(correlations)
    
    if cti_data and cti_data.get("malicious_hits", 0) > 0:
        threat_score += 100  # Máximo castigo por detección confirmada en VT

    # Crear tabla de resultados
    table = Table(title=f"Análisis: {os.path.basename(filepath)}", show_header=False, box=None)
    table.add_row("Ruta", filepath)
    table.add_row("Firma Hex", signature)
    
    type_style = "bold green" if type_info else "bold yellow"
    table.add_row("Tipo Detectado", Text(file_type, style=type_style))
    
    if hashes:
        table.add_row("MD5", hashes['md5'])
        table.add_row("SHA256", hashes['sha256'])
    
    entropy_style = "bold red" if entropy > 7.5 else "green"
    table.add_row("Entropía", Text(f"{entropy:.2f}", style=entropy_style))
    
    # Mostrar IoCs detectados
    if iocs:
        ioc_summary = []
        for ioc_type, items in iocs.items():
            ioc_summary.append(f"{ioc_type.upper()}: {len(items)}")
        table.add_row("IoCs Detectados", ", ".join(ioc_summary))

    # Mostrar tabla estructurada evitando superposición de Hilos
    with print_lock:
        console.print(Panel(table, title="[bold blue]Resultados del Escaneo[/bold blue]", border_style="blue"))

        # Alertas y Correlaciones
        if correlations:
            c_text = Text("🧠 Correlaciones Detectadas:\n", style="bold cyan")
            for item, hashes_list in correlations.items():
                c_text.append(f"  • {item} ", style="white")
                c_text.append(f"(visto en {len(hashes_list)} archivos previos)\n", style="dim")
            console.print(Panel(c_text, title="[bold cyan]Memoria del Agente[/bold cyan]", border_style="cyan"))

        if entropy > 7.5:
            console.print(Panel("[bold yellow]! ADVERTENCIA: Entropía muy alta (>7.5). Posible archivo cifrado o empaquetado.[/bold yellow]", border_style="yellow"))
        
        if is_mismatch or not type_info:
            console.print(Panel("[bold red]! ALERTA CRÍTICA: Discrepancia o Formato Desconocido (Modo Paranoia Sysadmin).[/bold red]", border_style="red"))
            
        if cti_data and cti_data.get("malicious_hits", 0) > 0:
            console.print(Panel(f"[bold red]☠️ PELIGRO: VirusTotal (CTI) reporta {cti_data['malicious_hits']} detecciones positivas para este hash.[/bold red]", border_style="red"))
        
        # Mostrar vulnerabilidades
        if vulnerabilities:
            v_table = Table(title="[bold red]Hallazgos de Seguridad (SAST y PE)[/bold red]", show_header=True, box=None)
            v_table.add_column("Línea / Cabecera", style="cyan")
            v_table.add_column("Riesgo", style="bold red")
            v_table.add_column("Detección")
            
            for v in vulnerabilities[:5]: 
                v_table.add_row(str(v['line']), v['severity'], v['rule'])
                
            console.print(Panel(v_table, border_style="red"))

    # 4. Guardar en Memoria (Aprender)
    memory_results = {
        "timestamp": datetime.now().isoformat(),
        "threat_score": threat_score,
        "findings": [v['rule'] for v in vulnerabilities],
        "iocs": iocs
    }
    memory.learn_analysis(sha256, filepath, memory_results)
    
    with print_lock:
        console.print("-" * 40)
    
    # Añadir al reporte
    if report_list is not None:
        report_entry = {
            "path": filepath,
            "signature": signature,
            "detected_type": file_type,
            "extension_mismatch": is_mismatch,
            "hashes": hashes,
            "entropy": entropy,
            "iocs": iocs,
            "correlations": correlations,
            "vulnerabilities": vulnerabilities,
            "cti_data": cti_data,
            "threat_score": threat_score
        }
        report_list.append(report_entry)


def main():
    parser = argparse.ArgumentParser(description="Identifica tipos de archivos usando números mágicos y detecta spoofing.")
    parser.add_argument("path", help="Ruta al archivo o directorio a escanear")
    parser.add_argument("--output", help="Ruta para guardar el reporte en JSON", default=None)
    parser.add_argument("--pdf", action="store_true", help="Generar dictamen ejecutivo en PDF automáticamente")
    
    args = parser.parse_args()
    
    report_data = [] if (args.output or args.pdf) else None
    
    if os.path.isfile(args.path):
        scan_file(args.path, report_data)
    elif os.path.isdir(args.path):
        logger.info(f"Escaneando directorio: [bold]{args.path}[/bold]")
        files_to_scan = []
        for root, _, files in os.walk(args.path):
            for file in files:
                files_to_scan.append(os.path.join(root, file))
        
        # Barra de progreso para directorios con ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
            futures = [executor.submit(scan_file, fp, report_data) for fp in files_to_scan]
            
            for _ in track(as_completed(futures), total=len(files_to_scan), description="Procesando archivos (Multi-hilo)..."):
                pass
            
    else:
        logger.error(f"La ruta '[bold red]{args.path}[/bold red]' no existe.")

    # Guardar reporte si se solicitó
    if args.output and report_data is not None:
        try:
            # Si no es ruta absoluta, guardarlo en reports/
            output_path = args.output
            if not os.path.isabs(output_path):
                os.makedirs('reports', exist_ok=True)
                output_path = os.path.join('reports', args.output)
            
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=4)
            logger.info(f"Reporte JSON guardado exitosamente en: [bold green]{output_path}[/bold green]")
        except Exception as e:
            logger.error(f"Error al guardar el reporte JSON: {e}")
            
    if args.pdf and report_data is not None:
        generate_pdf_report(report_data)

if __name__ == "__main__":
    main()

