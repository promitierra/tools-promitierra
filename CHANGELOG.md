* Registro de Cambios

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
