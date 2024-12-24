# Herramientas ProMITIERRA

Aplicación de escritorio para convertir imágenes a PDF con funcionalidades avanzadas.S

## Características

- Conversión de imágenes a PDF
- Soporte para múltiples formatos (JPG, PNG, GIF, BMP, TIFF)
- Interfaz gráfica moderna y amigable
- Creación de carpetas desde plantilla Excel
- Normalización de nombres
- Barra de progreso y cancelación
- Compresión configurable

## Estructura del Proyecto

```
├── src/                    # Código fuente
│   ├── core/              # Lógica principal
│   │   ├── image_processor.py
│   │   ├── pdf_converter.py
│   │   └── text_normalizer.py
│   ├── gui/               # Interfaz gráfica
│   │   ├── main_window.py
│   │   └── progress_dialog.py
│   └── main.py            # Punto de entrada
├── tests/                 # Pruebas
│   ├── test_cases/       # Casos de prueba
│   └── data/             # Datos de prueba
├── build_tools/          # Herramientas de construcción
│   ├── scripts/         # Scripts de construcción
│   └── resources/       # Recursos (iconos, etc.)
├── docs/                 # Documentación
├── requirements.txt      # Dependencias
└── README.md            # Este archivo
```

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/imagenTopdf.exe.git
cd imagenTopdf.exe
```

2. Crear y activar entorno virtual:

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Uso

1. Ejecutar la aplicación:

```bash
python src/main.py
```

2. Usar la interfaz gráfica para:
   - Seleccionar la carpeta con imágenes
   - Elegir el archivo PDF de salida
   - Configurar opciones (opcional)
   - Iniciar la conversión

## Desarrollo

### Pruebas

Ejecutar pruebas:

```bash
pytest tests/
```

Cobertura de código:

```bash
coverage run -m pytest tests/
coverage report
```

### Linting y Formateo

Análisis de código:

```bash
pylint src/ tests/
```

Formateo de código:

```bash
black src/ tests/
```

### Generar Ejecutable

```bash
python build_tools/scripts/build_exe.py
```

## Contribuir

1. Fork el proyecto
2. Crear rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -am 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.
