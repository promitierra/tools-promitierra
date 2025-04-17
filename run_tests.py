#!/usr/bin/env python
import unittest
import sys
from pathlib import Path

# Configurar los paths
project_root = Path(__file__).parent
sys.path.append(str(project_root))

if __name__ == "__main__":
    # Descubrir y ejecutar todos los tests
    test_suite = unittest.defaultTestLoader.discover('tests', pattern='test_*.py')
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Salir con código de error si hay fallos
    sys.exit(not result.wasSuccessful()) 