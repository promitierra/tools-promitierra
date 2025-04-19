# Guía para ejecutar pruebas unitarias

## Descripción
Esta guía explica cómo ejecutar correctamente las pruebas unitarias en el proyecto Herramientas ProMiTIERRA, utilizando el sistema de pruebas configurado con pytest.

## Configuración de pruebas
El proyecto utiliza pytest como framework de pruebas con configuraciones específicas definidas en `pytest.ini`:

- Cobertura de código con pytest-cov
- Reportes de cobertura en varios formatos
- Marcadores personalizados para diferentes tipos de pruebas

## Ejecutar pruebas

### Recomendación: Usar el script run_tests.py

La manera recomendada para ejecutar pruebas es utilizando el script `run_tests.py`, que gestiona correctamente el entorno virtual y las configuraciones:

```bash
# Ejecutar todas las pruebas
python run_tests.py

# Ejecutar un archivo de pruebas específico
python run_tests.py tests/unit/test_helpers.py

# Ejecutar un directorio específico
python run_tests.py tests/unit/
```

### Alternativas (no recomendadas)

No se recomienda usar directamente el comando pytest debido a posibles problemas con el entorno virtual:

```bash
# ⚠️ No recomendado - Puede causar errores de módulos faltantes
pytest tests/unit/test_helpers.py -v
```

## Solución de problemas comunes

### Error: "No module named pytest"

**Problema**: El comando muestra "No module named pytest" aunque pytest esté instalado.

**Solución**: Este error suele ocurrir cuando se utiliza un ejecutable Python incorrecto. Utilice el script `run_tests.py` que está configurado para usar el Python del entorno virtual.

### Error: "unrecognized arguments: --cov=src"

**Problema**: Aparece un error relacionado con argumentos de cobertura.

**Solución**: Las opciones de cobertura están definidas en `pytest.ini`. Al ejecutar pytest directamente, use el flag `--override-ini="addopts="` o use `run_tests.py`.

## Estructura de pruebas

- `tests/unit/`: Pruebas unitarias
- `tests/integration/`: Pruebas de integración

## Referencias
- [Documentación oficial de pytest](https://docs.pytest.org/)
- [Documentación de pytest-cov](https://pytest-cov.readthedocs.io/) 