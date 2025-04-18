# Pruebas (Tests) para Herramientas ProMITIERRA

Este directorio contiene las pruebas automatizadas para el proyecto Herramientas ProMITIERRA.

## Estructura de Directorios

```
tests/
├── unit/              # Pruebas unitarias (componentes individuales)
├── integration/       # Pruebas de integración (interacción entre componentes)
├── data/              # Datos para pruebas
│   ├── input/         # Archivos de entrada para pruebas
│   └── expected/      # Resultados esperados para comparación
├── conftest.py        # Configuración compartida de pytest
└── README.md          # Este archivo
```

## Convenciones de Nombres

- **Archivos**: Usar formato `test_[nombre_modulo].py`
- **Métodos**: `test_[función]_[escenario]_[resultado_esperado]`

## Ejecución de Pruebas

Para ejecutar todas las pruebas:
```
python -m pytest
```

Para ejecutar solo pruebas unitarias:
```
python -m pytest tests/unit
```

Para ejecutar solo pruebas de integración:
```
python -m pytest tests/integration
```

Para ejecutar tests con reporte de cobertura:
```
python -m pytest --cov=src
```

## Fixtures Compartidos

Los fixtures compartidos se encuentran en `conftest.py` e incluyen:

- `temp_dir`: Crea un directorio temporal para las pruebas y lo elimina después
- `test_files_dir`: Retorna la ruta al directorio de archivos de prueba
- `expected_files_dir`: Retorna la ruta al directorio de archivos esperados para comparaciones

## Mejores Prácticas

1. **Independencia**: Cada test debe ser autónomo y no depender de otros tests
2. **Cobertura**: Cubrir el camino feliz, casos de error y casos límite
3. **Simplicidad**: Una aseveración principal por test
4. **Aislamiento**: Usar mocks para recursos externos

## Estructura de Tests (AAA)

```python
def test_example():
    # Arrange - Preparar datos y objetos
    converter = PDFConverter()

    # Act - Ejecutar acción
    result = converter.convert_image('imagen.jpg')

    # Assert - Verificar resultado
    assert result == True
``` 