#!/usr/bin/env python
"""
Script para ejecutar pruebas automatizadas para el proyecto Herramientas ProMITIERRA.
Detecta automáticamente las pruebas usando pytest y permite especificar opciones.
"""
import sys
import pytest
import argparse
from pathlib import Path

# Configurar los paths
project_root = Path(__file__).parents[2]  # Ajustado para reflejar la nueva ubicación
sys.path.append(str(project_root))

def run_tests():
    """Función para ejecutar pruebas con argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description='Ejecutar pruebas para Herramientas ProMITIERRA')
    parser.add_argument('--unit', action='store_true', help='Ejecutar solo pruebas unitarias')
    parser.add_argument('--integration', action='store_true', help='Ejecutar solo pruebas de integración')
    parser.add_argument('--no-cov', action='store_true', help='Desactivar reporte de cobertura')
    args, remaining = parser.parse_known_args()
    
    pytest_args = []
    
    # Agregar directorio específico según la opción
    if args.unit:
        pytest_args.append('tests/unit')
    elif args.integration:
        pytest_args.append('tests/integration')
    else:
        pytest_args.append('tests')
    
    # Desactivar cobertura si se solicita
    if args.no_cov:
        pytest_args.append('--no-cov')
    
    # Agregar argumentos adicionales
    pytest_args.extend(remaining)
    
    print(f"Ejecutando pytest con argumentos: {' '.join(pytest_args)}")
    
    # Ejecutar pytest con los argumentos configurados
    return pytest.main(pytest_args)

if __name__ == "__main__":
    sys.exit(run_tests()) 