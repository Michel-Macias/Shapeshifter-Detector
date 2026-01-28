#!/usr/bin/env python3
"""
Investigación Forense Detallada de Vulnerabilidades
Extrae y clasifica todas las vulnerabilidades encontradas en los reportes
"""

import json
from pathlib import Path
from collections import defaultdict

def investigate_vulnerabilities(reports_dir="reports"):
    """Analiza en detalle todas las vulnerabilidades encontradas."""
    
    vulnerabilities_by_file = defaultdict(list)
    vulnerabilities_by_severity = defaultdict(list)
    
    reports = list(Path(reports_dir).glob("*.json"))
    
    for report_file in reports:
        try:
            with open(report_file, 'r') as f:
                data = json.load(f)
            
            if not data:
                continue
            
            for entry in data:
                file_path = entry.get('path', 'Unknown')
                vulns = entry.get('vulnerabilities', [])
                
                if vulns:
                    for vuln in vulns:
                        vuln_detail = {
                            'file': file_path,
                            'rule': vuln['rule'],
                            'severity': vuln['severity'],
                            'line': vuln['line'],
                            'snippet': vuln['content'],
                            'report_source': report_file.name
                        }
                        vulnerabilities_by_file[file_path].append(vuln_detail)
                        vulnerabilities_by_severity[vuln['severity']].append(vuln_detail)
        
        except Exception as e:
            print(f"⚠️  Error procesando {report_file}: {e}")
    
    return vulnerabilities_by_file, vulnerabilities_by_severity

def print_detailed_report(vuln_by_file, vuln_by_severity):
    """Imprime un informe forense detallado."""
    
    total_files_with_vulns = len(vuln_by_file)
    total_vulns = sum(len(v) for v in vuln_by_file.values())
    
    print("\n" + "="*80)
    print("🔍 INVESTIGACIÓN FORENSE DE VULNERABILIDADES".center(80))
    print("="*80 + "\n")
    
    print(f"📊 Resumen:")
    print(f"   • Archivos con vulnerabilidades: {total_files_with_vulns}")
    print(f"   • Total de vulnerabilidades: {total_vulns}")
    print(f"   • Críticas: {len(vuln_by_severity.get('Crítica', []))}")
    print(f"   • Altas: {len(vuln_by_severity.get('Alta', []))}")
    print(f"   • Medias: {len(vuln_by_severity.get('Media', []))}")
    
    print("\n" + "-"*80)
    print("🚨 ARCHIVOS SOSPECHOSOS (ordenados por severidad)")
    print("-"*80 + "\n")
    
    # Ordenar archivos por cantidad de vulnerabilidades críticas/altas
    files_sorted = sorted(
        vuln_by_file.items(),
        key=lambda x: sum(1 for v in x[1] if v['severity'] in ['Crítica', 'Alta']),
        reverse=True
    )
    
    for idx, (file_path, vulns) in enumerate(files_sorted[:20], 1):
        # Clasificar severidad
        critical = sum(1 for v in vulns if v['severity'] == 'Crítica')
        high = sum(1 for v in vulns if v['severity'] == 'Alta')
        medium = sum(1 for v in vulns if v['severity'] == 'Media')
        
        # Determinar emoji según riesgo
        if critical > 0:
            emoji = "🔴"
            risk = "CRÍTICO"
        elif high > 0:
            emoji = "🟠"
            risk = "ALTO"
        else:
            emoji = "🟡"
            risk = "MEDIO"
        
        filename = file_path.split('/')[-1]
        print(f"{emoji} [{risk}] {filename}")
        print(f"   Ruta: {file_path}")
        print(f"   Vulnerabilidades: Crítica={critical}, Alta={high}, Media={medium}")
        
        # Mostrar las 3 primeras vulnerabilidades de este archivo
        for v in vulns[:3]:
            print(f"   └─ Línea {v['line']}: {v['rule']} ({v['severity']})")
            print(f"      Código: {v['snippet'][:70]}...")
        
        if len(vulns) > 3:
            print(f"   └─ ... y {len(vulns) - 3} más")
        print()
    
    if len(files_sorted) > 20:
        print(f"   ... y {len(files_sorted) - 20} archivos más con vulnerabilidades")
    
    # Análisis de patrones
    print("\n" + "-"*80)
    print("📈 PATRONES DE ATAQUE DETECTADOS")
    print("-"*80 + "\n")
    
    from collections import Counter
    all_rules = [v['rule'] for vulns in vuln_by_file.values() for v in vulns]
    rule_counts = Counter(all_rules)
    
    for rule, count in rule_counts.most_common(10):
        print(f"   [{count:3d}] {rule}")

if __name__ == "__main__":
    vuln_by_file, vuln_by_severity = investigate_vulnerabilities()
    print_detailed_report(vuln_by_file, vuln_by_severity)
