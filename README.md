# Herramientas ProMITIERRA v0.2.3

Aplicación python autoejecutable con herramientas que ahorran tiempo en trabajo de oficina.

- **Creación masiva de Carpetas**: Genera estructuras de directorios automáticamente desde plantillas Excel.
- **Convertir Imágenes a PDF**: Convierte rápidamente imágenes a documentos PDF, usando procesamiento paralelo y preservando la estructura de carpetas.
  - Soporte para múltiples formatos de imagen:
    - PNG, JPG, JPEG, BMP, TIFF, WEBP, GIF
    - Manejo case-insensitive de extensiones (*.jpg, *.JPG, etc.)
    - Preservación de la estructura de directorios:
  - Mantiene la jerarquía de carpetas al convertir
  - Opción para generar archivo ZIP con los PDFs
      - Estructura idéntica en el archivo ZIP
**Consolidar Imágenes de un directorio en un documento PDF**
  - Incluye script dedicado (`src/scripts/generar_pdf_imagenes.py`) con opciones avanzadas (márgenes, orientación, numeración).
- **Redimensionar PDF**: Ajusta todas las páginas de documentos PDFs a tamaño carta, manteniendo orientación y con opción de centrado.
  - Preservación de la orientación original (vertical/horizontal)
  - Opción para centrar automáticamente el contenido
  - Escalado proporcional para evitar distorsiones
- **Conversión de PDF a imágenes PNG**: Convierte páginas de PDF a imágenes PNG de alta calidad.
  - Extracción de imágenes incrustadas en PDFs
  - Generación de imágenes de alta calidad (300 DPI)
  - Verificación de integridad de archivos generados
  - **Optimizar Imágenes**: Reduce el tamaño de archivos de imagen (`src/scripts/optimizar_imagenes.py`).
  - **Renombrado de Archivos**: Utilidades para renombrar archivos en lote según patrones específicos (ej. `src/scripts/renombrar_entrega_ippta.py`, `src/scripts/renombrar_entrega_planeador.py`).

## Características

- **Interfaz Gráfica Intuitiva**: Fácil de usar para las tareas principales.
- **Procesamiento Eficiente**: Uso de procesamiento paralelo para conversiones rápidas.
- **Flexibilidad**:
    - Conversión simple (PDFs en carpetas originales) o modo comprimido (ZIP).
    - Múltiples formatos de imagen soportados (PNG, JPG, JPEG, BMP, TIFF, WEBP, GIF).
    - Opciones configurables para generación de PDF (vía script).
- **Calidad y Precisión**:
    - Redimensionamiento a tamaño carta con preservación de orientación y centrado opcional.
    - Conversión a PNG de alta calidad (300 DPI).
    - Verificación de integridad de archivos generados.
- **Organización**:
    - Preservación de la estructura de directorios original.
    - Sistema de renombrado de archivos con validación y vista previa (`src/utils/file_operations.py`).
- **Manejo de Errores**: Reporte detallado sin detener operaciones en lote.
  - Manejo eficiente de memoria para imágenes grandes
-   Soporte para cancelación de operaciones
- **Soporte para Desarrolladores**: Scripts individuales para tareas específicas y utilidades reutilizables.


## Requisitos

- Python 3.8 o superior (para desarrollo)
- Windows 10 o superior (para ejecutable)
- Dependencias listadas en `requirements.txt` (Pillow, CustomTkinter, etc.)

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/promitierra/tools-promitierra.git
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

1.  **Ejecutable (Usuario Final)**:
    *   Descarga la última versión desde [Releases](https://github.com/promitierra/tools-promitierra/releases).
    *   Ejecuta `Herramientas ProMITIERRA.exe`.
    *   Utiliza las pestañas de la interfaz gráfica según se describe en el [TUTORIAL.md](TUTORIAL.md).

2.  **Desde Código Fuente (Desarrollo)**:
    *   Clona el repositorio: `git clone https://github.com/promitierra/tools-promitierra.git`
    *   Instala dependencias: `uv pip install -r requirements.txt`
    *   Ejecuta la aplicación principal: `python main.py`
    *   Ejecuta scripts individuales (ej.): `python src/scripts/generar_pdf_imagenes.py ruta/a/imagenes --opciones`

### Modos de Operación (GUI - Imágenes a PDF)

La aplicación ofrece dos modos de operación:

1. **Conversión Simple**:

   - Los PDFs se crean en las mismas ubicaciones que las imágenes originales
   - Se mantiene la estructura exacta de directorios
   - Ejemplo: si tienes `fotos/2023/enero/imagen.jpg`, se creará `fotos/2023/enero/imagen.pdf`
2. **Modo Comprimido (ZIP)**:

   - Genera un archivo ZIP con todos los PDFs
   - Mantiene la estructura de directorios dentro del ZIP
   - El archivo ZIP se crea en el directorio raíz seleccionado
   - Nombre del ZIP incluye fecha y hora para evitar sobrescrituras

### Procesamiento de Imágenes

- Las imágenes grandes se redimensionan automáticamente para optimizar memoria
- Conversión a RGB automática para formatos especiales (RGBA, LA, etc.)
- Procesamiento paralelo para mayor velocidad
- Muestra progreso en tiempo real
- Reporta errores individuales sin detener el proceso completo

## Contribuir

Las contribuciones son bienvenidas. Por favor, asegúrate de:

1. Seguir el estilo de código existente
2. Agregar pruebas para nuevas funcionalidades
3. Actualizar la documentación según sea necesario

## Licencia

Este proyecto está licenciado bajo MIT License - ver el archivo LICENSE para detalles.

## Autor

- Luis Fernando Moreno Montoya
- GitHub: @mmlufer
- Email: fernando.moreno@promitierra.org
