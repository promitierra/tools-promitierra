# Herramientas ProMITIERRA v0.2.1

Aplicación python autoejecutable con herramientas que ahorran tiempo en trabajo de oficina.

- Herramienta que crea carpetas automaticamente, nombrándolas de acuerdo a los valores incluidos en plantilla de excel.
- Herramienta para convertir todas las imágenes en varios formatos dentro de un directorio y sus subcarpetas a formato PDF de forma rápida y eficiente.

## Características

- Conversión rápida de imágenes a PDF usando procesamiento paralelo
- Soporte para múltiples formatos de imagen:
  - PNG, JPG, JPEG, BMP, TIFF, WEBP, GIF
  - Manejo case-insensitive de extensiones (*.jpg, *.JPG, etc.)
- Interfaz gráfica moderna e intuitiva
- Opción para generar archivo ZIP con los PDFs
- Preservación de la estructura de directorios:
  - Mantiene la jerarquía de carpetas al convertir
  - Estructura idéntica en el archivo ZIP
- Manejo eficiente de memoria para imágenes grandes
- Soporte para cancelación de operaciones

## Requisitos

- Python 3.8 o superior
- Pillow >= 10.3.0
- CustomTkinter >= 5.2.2
- Threading

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tuusuario/imagenTopdf.exe.git
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

1. Ejecuta la aplicación:

```bash
python main.py
```

2. Usa la interfaz gráfica para:
   - Seleccionar la carpeta con imágenes
   - Elegir si deseas generar un archivo ZIP
   - Iniciar la conversión

### Modo de Operación

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
