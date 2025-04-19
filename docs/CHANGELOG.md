# Registro de Cambios (Changelog)

Este documento registra los cambios notables en el proyecto Herramientas ProMITIERRA.

## [Unreleased]

### Agregado
- Sistema de gestión de configuración con `ConfigManager` para administrar preferencias del usuario y ajustes de rendimiento
- Soporte para agrupación de carpetas por categoría en `FolderCreator`
- Verificación de espacio disponible antes de crear carpetas
- Nueva función para cancelar procesos en curso
- Validación mejorada de plantillas Excel

### Mejorado
- Optimización del manejo de memoria en `PDFConverter` para imágenes grandes
- Conversión de PDF a PNG con extracción automática de páginas cuando no hay imágenes incrustadas
- Normalización de nombres de carpetas con manejo de caracteres inválidos
- Pruebas unitarias adicionales para las nuevas funcionalidades
- Ajuste automático del número de workers según disponibilidad del sistema

### Corregido
- Manejo mejorado de imágenes con transparencia
- Verificación de integridad después de conversión de imágenes

## [1.0.0] - 2023-12-15

### Agregado
- Funcionalidad de conversión masiva de imágenes a PDF
- Creación de carpetas a partir de plantillas Excel
- Conversión de PDFs a imágenes PNG
- Redimensionamiento de PDFs a tamaño carta
- Interfaz gráfica con pestañas para diferentes herramientas 