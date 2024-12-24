# ImagenToPDF

Aplicación para convertir imágenes a PDF de forma rápida y eficiente.

## Características

- Conversión rápida de imágenes a PDF usando procesamiento paralelo
- Soporte para múltiples formatos de imagen:
  - PNG, JPG, JPEG, BMP, TIFF, WEBP, GIF, HEIC, HEIF
  - Manejo case-insensitive de extensiones (*.jpg, *.JPG, etc.)
- Filtrado de imágenes por patrones personalizados (ej: `foto_*.jpg`, `*.png`)
- Interfaz gráfica moderna e intuitiva
- Opción para generar archivo ZIP con los PDFs
- Manejo eficiente de memoria para imágenes grandes
- Soporte para cancelación de operaciones

## Requisitos

- Python 3.8 o superior
- Pillow >= 10.3.0 (Importante: versión mínima por seguridad)
- CustomTkinter >= 5.2.2
- Threading

## Seguridad

Este proyecto se mantiene actualizado con las últimas correcciones de seguridad. La versión mínima de Pillow (10.3.0) es requerida para prevenir una vulnerabilidad de ejecución de código arbitrario en PIL.ImageMath.eval.

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
python src/app/main.py
```

2. Usa la interfaz gráfica para:
   - Seleccionar la carpeta con imágenes
   - Aplicar filtros por patrón (opcional)
   - Elegir si deseas generar un ZIP
   - Iniciar la conversión

### Filtros de Búsqueda

Puedes usar patrones para filtrar las imágenes que deseas convertir:
- `*.jpg` - Todas las imágenes JPG
- `foto_*.png` - Imágenes PNG que empiecen con "foto_"
- `IMG_20*.jpg` - Fotos JPG que empiecen con "IMG_20"

## Desarrollo

### Estructura del Proyecto
```
imagenTopdf.exe/
├── src/
│   └── app/
│       ├── main.py
│       ├── gui.py
│       └── pdf_converter.py
├── tests/
│   └── test_pdf_converter.py
├── requirements.txt
├── README.md
└── ROADMAP.md
```

### Pruebas

Ejecuta las pruebas unitarias:
```bash
python -m unittest tests/test_pdf_converter.py -v
```

## Contribuir

1. Haz un Fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
