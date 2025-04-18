"""
Configuración central para pruebas de Herramientas ProMITIERRA.
Este módulo contiene fixtures y configuraciones compartidas para todas las pruebas.
"""
import os
import sys
import shutil
import tempfile
import pytest
from pathlib import Path

# Añadir directorio src al path de Python
src_path = str(Path(__file__).parent.parent)
sys.path.insert(0, src_path)

@pytest.fixture
def temp_dir():
    """Crea un directorio temporal para las pruebas y lo elimina después."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Limpiar después de la prueba
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

@pytest.fixture
def test_files_dir():
    """Retorna la ruta al directorio de archivos de prueba."""
    return Path(__file__).parent / "data" / "input"

@pytest.fixture
def expected_files_dir():
    """Retorna la ruta al directorio de archivos esperados para comparaciones."""
    return Path(__file__).parent / "data" / "expected"

# Configuración para evitar advertencias de recursos descartados en pruebas asíncronas
@pytest.fixture(autouse=True)
def setup_tear_down():
    """Configuración y limpieza global para todas las pruebas."""
    # Código que se ejecuta antes de cada prueba
    yield
    # Código que se ejecuta después de cada prueba
