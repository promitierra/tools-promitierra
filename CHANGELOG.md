# Registro de Cambios

## [1.2.1] - 2024-12-24

### Seguridad
- Actualizada la dependencia de Pillow a >=10.3.0 para corregir una vulnerabilidad de seguridad en `PIL.ImageMath.eval`
- Mejorada la gestión de dependencias con versiones específicas

### Cambios
- Agregadas dependencias de desarrollo (pytest, coverage)
- Actualizada la documentación de requisitos
- Mejorada la estructura del archivo requirements.txt

## [1.2.0] - 2024-12-23

### Agregado
- Implementado soporte para patrones personalizados en la búsqueda de imágenes
- Agregado manejo case-insensitive para extensiones de archivo
- Nuevos formatos de imagen soportados: HEIC, HEIF
- Tooltips informativos en la interfaz

### Optimizado
- Mejorado el rendimiento de búsqueda de archivos
- Implementada búsqueda case-insensitive eficiente
- Optimizado el manejo de memoria

### Corregido
- Solucionado problema con duplicados en la búsqueda de archivos
- Mejorado el manejo de errores en la conversión

## [1.1.0] - 2024-12-22

### Agregado
- Implementado procesamiento paralelo con ThreadPool
- Agregada funcionalidad de cancelación de operaciones
- Mejorado el manejo de memoria para imágenes grandes

### Optimizado
- Migración a pathlib para manejo de rutas
- Mejorada la eficiencia en la búsqueda de archivos

## [1.0.0] - 2024-12-21

### Inicial
- Lanzamiento inicial de la aplicación
- Interfaz gráfica básica
- Soporte para formatos principales de imagen
- Conversión básica a PDF
