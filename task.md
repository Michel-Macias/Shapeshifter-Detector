# 📋 Plan de Refactorización y Optimización de Memoria

Este plan detalla las tareas para mejorar la robustez y escalabilidad de **Shapeshifter-Detector**, abordando los problemas de consumo de memoria y profesionalización de la gestión de eventos.

## 🎯 Objetivos de Calidad
- [ ] **Optimización de Memoria**: Procesar archivos de cualquier tamaño mediante lectura por bloques (chunks) para evitar errores OOM (Out of Memory).
- [ ] **Logging Profesional**: Sustituir `print` por el módulo `logging` con niveles adecuados (INFO, ERROR, DEBUG).
- [ ] **Metodología TDD**: Cada cambio debe ser validado mediante el ciclo Red-Green-Refactor.

---

## 🛠️ Tareas

### Fase 1: Optimización de Entropía (TDD)
- [x] **TDD-Red**: Crear un test que verifique la entropía de un archivo "grande" (simulado o mockeado) procesado por bloques.
- [x] **TDD-Green**: Refactorizar `calculate_entropy` en `src/core.py` para usar lectura incremental.
- [x] **Refactor**: Limpiar y documentar el nuevo método.

### Fase 2: Optimización de Extracción de Strings (TDD)
- [x] **TDD-Red**: Crear un test que valide la extracción de strings procesando el archivo secuencialmente sin cargarlo entero en RAM.
- [x] **TDD-Green**: Refactorizar `extract_strings` en `src/core.py`.
- [x] **Refactor**: Optimizar el buffer de búsqueda de caracteres imprimibles.

### Fase 3: Sistema de Logging
- [x] **Configuración**: Crear un logger centralizado en `src/core.py` o un nuevo `src/logger.py`.
- [x] **Migración**: Sustituir todos los `print` en `src/core.py` y `src/cli.py` por llamadas al logger.
- [x] **Verificación**: Asegurar que la salida en CLI y Dashboard siga siendo impecable (usando `RichHandler` de Rich si es posible).

---

## 🛡️ Verificación Final
- [x] Ejecutar suite completa de tests: `python3 -m unittest discover tests`.
- [x] Prueba de rendimiento con archivo > 100MB.

