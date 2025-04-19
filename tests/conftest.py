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
from typing import List
import importlib

# Añadir directorio raíz del proyecto al sys.path para que los módulos sean importables
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Verificar si hay un entorno virtual activado y añadirlo al path si existe
if "VIRTUAL_ENV" in os.environ:
    venv_path = os.path.join(os.environ["VIRTUAL_ENV"], "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages")
    print(f"Añadiendo al sys.path: {venv_path}")
    sys.path.insert(0, venv_path)

# Verificar si estamos usando venv en la carpeta del proyecto
venv_dir = BASE_DIR / "venv" / "lib"
if venv_dir.exists():
    for py_dir in venv_dir.glob("python*"):
        site_packages = py_dir / "site-packages"
        if site_packages.exists():
            print(f"Añadiendo al sys.path: {site_packages}")
            sys.path.insert(0, str(site_packages))

# Verificar si estamos usando .venv en la carpeta del proyecto
venv_alt_dir = BASE_DIR / ".venv" / "lib"
if venv_alt_dir.exists():
    for py_dir in venv_alt_dir.glob("python*"):
        site_packages = py_dir / "site-packages"
        if site_packages.exists():
            print(f"Añadiendo al sys.path: {site_packages}")
            sys.path.insert(0, str(site_packages))

# Verificar disponibilidad de dependencias críticas
DEPENDENCIAS_CRITICAS = [
    "PIL", "pandas", "customtkinter", "fitz", "PyPDF2"
]

def verificar_dependencias(dependencias: List[str]) -> None:
    """Verifica si las dependencias necesarias están disponibles."""
    for dep in dependencias:
        try:
            importlib.import_module(dep)
            print(f"✅ Dependencia {dep} disponible")
        except ImportError:
            print(f"❌ Error al importar {dep}: No module named '{dep}'")

print("Rutas de búsqueda actuales:")
for path in sys.path[:5]:  # Mostrar solo las primeras 5 rutas para no saturar
    print(f"- {path}")

verificar_dependencias(DEPENDENCIAS_CRITICAS)

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
