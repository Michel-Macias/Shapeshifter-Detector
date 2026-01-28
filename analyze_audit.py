#!/usr/bin/env python3
"""
Consolidador de Reportes de Auditoría Forense
Genera un informe ejecutivo con las amenazas críticas encontradas.
"""

import json
import os
from pathlib import Path
from collections import Counter

def analyze_reports(reports_dir="reports"):
    """Analiza todos los reportes JSON en el directorio especificado."""
    
    vulnerabilities_critical = []
    spoofing_alerts = []
    high_entropy_files = []
    total_files = 0
    
    reports = list(Path(reports_dir).glob("*.json"))
    
    for report_file in reports:
        try:
            with open(report_file, 'r') as f:
                data = json.load(f)
                
            if not data:  # Reporte vacío
                continue
                
            for entry in data:
                total_files += 1
                
                # Detectar spoofing
                if entry.get('extension_mismatch'):
                    spoofing_alerts.append({
                        'path': entry['path'],
                        'detected': entry['detected_type'],
                        'report': report_file.name
                    })
                
                # Detectar alta entropía (posible cifrado/packing)
                if entry.get('entropy', 0) > 7.5:
                    high_entropy_files.append({
                        'path': entry['path'],
                        'entropy': entry['entropy'],
                        'report': report_file.name
                    })
                
                # Consolidar vulnerabilidades críticas
                for vuln in entry.get('vulnerabilities', []):
                    if vuln.get('severity') in ['Crítica', 'Alta']:
                        vulnerabilities_critical.append({
                            'file': entry['path'],
                            'rule': vuln['rule'],
                            'severity': vuln['severity'],
                            'line': vuln['line'],
                            'report': report_file.name
                        })
        except Exception as e:
            print(f"⚠️  Error procesando {report_file}: {e}")
    
    return {
        'total_files': total_files,
        'total_reports': len(reports),
        'spoofing_alerts': spoofing_alerts,
        'high_entropy': high_entropy_files,
        'vulnerabilities': vulnerabilities_critical
    }

def print_executive_summary(analysis):
    """Imprime un resumen ejecutivo visual."""
    
    print("\n" + "="*70)
    print("🛡️  INFORME EJECUTIVO DE AUDITORÍA FORENSE".center(70))
    print("="*70 + "\n")
    
    print(f"📊 Total de Archivos Analizados: {analysis['total_files']}")
    print(f"📁 Reportes Procesados: {analysis['total_reports']}")
    print("\n" + "-"*70 + "\n")
    
    # Spoofing
    print(f"🎭 ALERTAS DE SPOOFING: {len(analysis['spoofing_alerts'])}")
    if analysis['spoofing_alerts']:
        for alert in analysis['spoofing_alerts'][:5]:
            print(f"   ⚠️  {alert['path']}")
            print(f"      → Detectado como: {alert['detected']}")
    else:
        print("   ✅ No se detectaron intentos de spoofing\n")
    
    # Vulnerabilidades
    print(f"\n🚨 VULNERABILIDADES CRÍTICAS/ALTAS: {len(analysis['vulnerabilities'])}")
    if analysis['vulnerabilities']:
        vuln_types = Counter([v['rule'] for v in analysis['vulnerabilities']])
        for rule, count in vuln_types.most_common(5):
            print(f"   🔴 {rule}: {count} ocurrencia(s)")
    else:
        print("   ✅ No se detectaron patrones de vulnerabilidad críticos\n")
    
    # Entropía
    print(f"\n🔒 ARCHIVOS CON ALTA ENTROPÍA (>7.5): {len(analysis['high_entropy'])}")
    if analysis['high_entropy']:
        print("   (Posibles archivos cifrados o empaquetados)")
        for item in analysis['high_entropy'][:3]:
            print(f"   📦 {os.path.basename(item['path'])} → Entropía: {item['entropy']:.2f}")
    else:
        print("   ✅ No se detectaron archivos con entropía sospechosa\n")
    
    print("\n" + "="*70)
    print("Reportes disponibles en: ./reports/")
    print("="*70 + "\n")

if __name__ == "__main__":
    analysis = analyze_reports()
    print_executive_summary(analysis)
