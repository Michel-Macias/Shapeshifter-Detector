import os
from datetime import datetime
from fpdf import FPDF
from src.logger import logger

class PDFReportGenerator(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Título
        self.cell(0, 10, 'Reporte Ejecutivo - Identify-Files Forensics', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        # A 1.5 cm del final
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Número de página
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(report_data, output_filename=None):
    """
    Genera un archivo PDF a partir del array de datos del reporte escaneado.
    """
    if not report_data:
        logger.warning("No hay datos para generar el reporte PDF.")
        return
        
    try:
        pdf = PDFReportGenerator()
        pdf.add_page()
        
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 10, f"Fecha del Escaneo Automático: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
        pdf.cell(0, 10, f"Total de artefactos examinados: {len(report_data)}", 0, 1)
        pdf.ln(10)
        
        for item in report_data:
            path = item.get("path", "N/A")
            filename = os.path.basename(path)
            threat_score = item.get("threat_score", 0)  # Deberemos inyectarlo en cli.py
            
            # Subtítulo por archivo
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f"Archivo: {filename}", 0, 1)
            pdf.set_font('Arial', '', 10)
            
            # Metadatos del Archivo
            pdf.cell(0, 8, f"-> Ruta: {path}", 0, 1)
            pdf.cell(0, 8, f"-> SHA256: {item.get('hashes', {}).get('sha256', 'N/A')}", 0, 1)
            pdf.cell(0, 8, f"-> Entropía: {item.get('entropy', 0):.2f}", 0, 1)
            
            if item.get("extension_mismatch"):
                pdf.set_text_color(255, 0, 0)
                pdf.cell(0, 8, f"-> [!] DISCREPANCIA EXTENSION DETECTADA (SPOOFING)", 0, 1)
                pdf.set_text_color(0, 0, 0)
                
            # Threat Intel (VT) Si existe
            cti = item.get("cti_data")
            if cti and cti.get("malicious_hits", 0) > 0:
                pdf.set_text_color(255, 0, 0)
                pdf.cell(0, 8, f"-> [!] VIRUSTOTAL HITS: {cti['malicious_hits']}/{cti['total_scans']}", 0, 1)
                pdf.set_text_color(0, 0, 0)
                
            # Vulnerabilidades extraídas
            vulns = item.get("vulnerabilities", [])
            if vulns:
                pdf.cell(0, 8, "Hallazgos SAST / PE Anómalos:", 0, 1)
                pdf.set_font('Arial', 'I', 9)
                for v in vulns[:5]:
                    pdf.cell(0, 6, f"  - {v['rule']} (Impacto: {v['severity']})", 0, 1)
                pdf.set_font('Arial', '', 10)
            
            pdf.ln(5)

        if not output_filename:
            os.makedirs('reports', exist_ok=True)
            output_filename = os.path.join('reports', f"ExSys_Report_{datetime.now().strftime('%Y%m%d%H%M')}.pdf")
            
        pdf.output(output_filename)
        logger.info(f"Reporte Operativo PDF generado exitosamente en [bold green]{output_filename}[/bold green]")
    except Exception as e:
        logger.error(f"Falla al generar el Engine de PDF: {e}")
