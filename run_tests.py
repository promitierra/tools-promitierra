#!/usr/bin/env python
"""
Script para ejecutar pruebas - redirección al script principal en tests/utils/
"""
import sys
from pathlib import Path

# Redirigir a la nueva ubicación
try:
    from tests.utils.run_tests import run_tests
    sys.exit(run_tests())
except ImportError:
    print("Error: No se pudo importar el módulo de pruebas. Asegúrate de que la estructura del proyecto es correcta.")
    sys.exit(1) 