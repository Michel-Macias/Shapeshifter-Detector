import argparse
import os
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import track
from src.core import get_file_signature, identify_type, calculate_hashes, calculate_entropy, extract_strings
from src.logger import logger

console = Console()

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
    """
    signature = get_file_signature(filepath)
    type_info = identify_type(signature)
    
    # Análisis Forense
    hashes = calculate_hashes(filepath)
    entropy = calculate_entropy(filepath)
    strings = extract_strings(filepath)
    
    file_type = type_info['type'] if type_info else "Desconocido"
    is_mismatch = check_mismatch(filepath, type_info)
    
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
    
    if strings:
        strings_preview = ", ".join(strings[:5])
        table.add_row("Strings (Preview)", Text(strings_preview, style="dim"))

    # Mostrar tabla
    console.print(Panel(table, title="[bold blue]Resultados del Escaneo[/bold blue]", border_style="blue"))

    # Alertas
    if entropy > 7.5:
        console.print(Panel("[bold yellow]! ADVERTENCIA: Entropía muy alta (>7.5). Posible archivo cifrado o empaquetado.[/bold yellow]", border_style="yellow"))
    
    if is_mismatch:
        console.print(Panel("[bold red]! ALERTA CRÍTICA: La extensión no coincide con el tipo real. Posible intento de Spoofing.[/bold red]", border_style="red"))
    
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
            "strings_preview": strings[:20]
        }
        report_list.append(report_entry)


def main():
    parser = argparse.ArgumentParser(description="Identifica tipos de archivos usando números mágicos y detecta spoofing.")
    parser.add_argument("path", help="Ruta al archivo o directorio a escanear")
    parser.add_argument("--output", help="Ruta para guardar el reporte en formato JSON", default=None)
    
    args = parser.parse_args()
    
    report_data = [] if args.output else None
    
    if os.path.isfile(args.path):
        scan_file(args.path, report_data)
    elif os.path.isdir(args.path):
        logger.info(f"Escaneando directorio: [bold]{args.path}[/bold]")
        files_to_scan = []
        for root, _, files in os.walk(args.path):
            for file in files:
                files_to_scan.append(os.path.join(root, file))
        
        # Barra de progreso para directorios
        for filepath in track(files_to_scan, description="Procesando archivos..."):
            scan_file(filepath, report_data)
            
    else:
        logger.error(f"La ruta '[bold red]{args.path}[/bold red]' no existe.")

    # Guardar reporte si se solicitó
    if args.output and report_data is not None:
        try:
            with open(args.output, 'w') as f:
                json.dump(report_data, f, indent=4)
            logger.info(f"Reporte guardado exitosamente en: [bold green]{args.output}[/bold green]")
        except Exception as e:
            logger.error(f"Error al guardar el reporte: {e}")

if __name__ == "__main__":
    main()

