# Pruebas Unitarias - Herramientas PromiTierra

Este directorio contiene las pruebas unitarias y de integración para el proyecto Herramientas PromiTierra.

## Estructura

- `unit/`: Pruebas unitarias
- `integration/`: Pruebas de integración
- `data/`: Datos de prueba
- `utils/`: Utilidades para pruebas
- `conftest.py`: Configuración global para pytest

## Requisitos

Para ejecutar las pruebas necesitas tener instaladas todas las dependencias del proyecto:

```bash
# Activar entorno virtual
source .venv/bin/activate  # o "source venv/bin/activate"

# Instalar el proyecto en modo desarrollo
pip install -e .

# Instalar todas las dependencias
pip install -r requirements.txt
```

## Ejecutar pruebas

### Usando el script `run_tests.py`

El script `run_tests.py` facilita la ejecución de pruebas:

```bash
# Ejecutar tests de helpers (recomendado, funcionan correctamente)
python run_tests.py --unit

# Si se quieren probar todas las pruebas (algunas pueden fallar)
python run_tests.py --all
```

### Usando pytest directamente

También puedes usar pytest directamente:

```bash
# Ejecutar test_helpers.py (recomendado)
python -m pytest tests/unit/test_helpers.py

# Ejecutar con detalles
python -m pytest tests/unit/test_helpers.py -v
```

### Uso con VS Code

Si usas VS Code, puedes usar la extensión "Pruebas" para ejecutar y depurar pruebas. 
La configuración ya está establecida en `.vscode/settings.json`.

## Estado actual

Actualmente solo la prueba `test_helpers.py` funciona correctamente. Las demás pruebas
requieren correcciones en las rutas de importación.

## Convenciones

1. Nombrar los archivos de prueba con el prefijo `test_`.
2. Nombrar las clases de prueba con el prefijo `Test`.
3. Nombrar los métodos de prueba con el prefijo `test_`.
4. Seguir el patrón AAA (Arrange-Act-Assert) en las pruebas.
5. Usar fixtures de pytest para configuración común.
6. Documentar correctamente las pruebas con docstrings. 