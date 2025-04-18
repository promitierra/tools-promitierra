# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - YYYY-MM-DD

### Added
- Nuevo script `src/scripts/generar_pdf_imagenes.py` para crear PDFs desde imágenes con opciones configurables ([6981a42](https://github.com/promitierra/tools-promitierra/commit/6981a42)).
- Nuevo script `src/scripts/optimizar_imagenes.py` para optimización de imágenes ([6981a42](https://github.com/promitierra/tools-promitierra/commit/6981a42)).
- Scripts `scripts/renombrar_archivos_ippta.py` y `scripts/renombrar_entrega_ippta.py` para renombrado específico de archivos IPPTA ([40d6e2b](https://github.com/promitierra/tools-promitierra/commit/40d6e2b)).
- Scripts `src/scripts/renombrar_entrega_ippta.py` y `src/scripts/renombrar_entrega_planeador.py` (versiones movidas/actualizadas) ([6981a42](https://github.com/promitierra/tools-promitierra/commit/6981a42)).
- Implementación de un sistema robusto para renombrar archivos (`src/utils/file_operations.py`) con soporte para patrones, validación y vista previa ([7ef19dd](https://github.com/promitierra/tools-promitierra/commit/7ef19dd)).
- Implementación de un sistema de callbacks (`src/utils/callbacks.py`) para notificar progreso y errores durante operaciones de archivos ([7ef19dd](https://github.com/promitierra/tools-promitierra/commit/7ef19dd)).
- Pruebas unitarias para el nuevo sistema de renombrado de archivos (`tests/test_file_operations.py`) ([7ef19dd](https://github.com/promitierra/tools-promitierra/commit/7ef19dd)).
- Pruebas para los scripts específicos de procesamiento IPPTA (`tests/test_generar_pdf_ippta.py`, `tests/test_renombrar_ippta.py`) ([304b4b3](https://github.com/promitierra/tools-promitierra/commit/304b4b3)).
- Guía de usuario en formato Sphinx (`.rst`) para el script `generar_pdf_imagenes.py` ([18420a9](https://github.com/promitierra/tools-promitierra/commit/18420a9)).
- Nueva regla de Cursor (`.cursor/rules/sphinx-documentation-best-practices.mdc`) para guiar la creación de documentación con Sphinx ([b8d2ec7](https://github.com/promitierra/tools-promitierra/commit/b8d2ec7)).
- Script `run_tests.py` para facilitar la ejecución de pruebas ([a453479](https://github.com/promitierra/tools-promitierra/commit/a453479)).

### Changed
- Actualizada la estructura de la documentación Sphinx para incluir la nueva guía `generar_pdf_imagenes` ([18420a9](https://github.com/promitierra/tools-promitierra/commit/18420a9)).
- Actualizados archivos de configuración (`.gitignore`, `requirements.txt`) y entorno de desarrollo/pruebas (`.coverage`, `coverage.xml`, `tools-promitierra.code-workspace`, `docs/ROADMAP.md`) ([a453479](https://github.com/promitierra/tools-promitierra/commit/a453479)).
- Refactorizados los scripts moviéndolos a la subcarpeta `src/scripts` ([0cf3c5f](https://github.com/promitierra/tools-promitierra/commit/0cf3c5f)).

### Removed
- Eliminado archivo de documentación Markdown redundante (`docs/generar_pdf_imagenes.md`) después de migrar a Sphinx ([f44e452](https://github.com/promitierra/tools-promitierra/commit/f44e452)).

## [0.2.3] - 2024-12-25

### Agregado
- Implementada funcionalidad para redimensionar archivos PDF a tamaño carta
- Agregada conversión de archivos PDF a imágenes PNG
- Soporte para centrado automático del contenido al redimensionar PDFs
- Preservación de la orientación original (vertical/horizontal) al redimensionar

### Mejorado
- Optimizado el proceso de extracción de imágenes desde PDFs
- Mejorada la calidad de las imágenes PNG generadas (300 DPI)
- Implementada verificación de integridad para archivos generados

## [0.2.2] - 2024-12-24

### Agregado
- Implementada preservación de la estructura de directorios
- Los PDFs ahora se crean en la misma ubicación que las imágenes originales
- Mejorado el soporte para archivos ZIP:
  - Mantiene la estructura de directorios dentro del ZIP
  - Nombres de archivo con fecha y hora para evitar sobrescrituras

### Mejorado
- Simplificada la interfaz de usuario
- Mejorada la retroalimentación visual del proceso
- Actualizada la documentación con los nuevos cambios

### Corregido
- Solucionado problema con la creación de directorios anidados
- Corregido el manejo de rutas relativas en el ZIP
- Mejorado el manejo de errores en callbacks

## [0.2.1] - 2024-12-23

### Agregado
- Implementado soporte para procesamiento paralelo
- Agregada opción para generar archivo ZIP
- Mejorado manejo de memoria para imágenes grandes

### Mejorado
- Optimizado el rendimiento de conversión
- Agregada barra de progreso y mensajes de estado
- Implementado manejo de errores robusto

## [0.2.0] - 2024-12-21

### Inicial
- Lanzamiento inicial de la aplicación
- Interfaz gráfica básica
- Soporte para formatos principales de imagen
- Conversión básica a PDF
