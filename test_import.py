import sys
import os

# Obtener ruta al directorio de paquetes del entorno virtual
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv/lib/python3.12/site-packages')
print(f"Añadiendo al sys.path: {env_path}")
sys.path.insert(0, env_path)

# Intentar importar customtkinter
try:
    import customtkinter
    print(f"✅ CustomTkinter importado correctamente. Versión: {customtkinter.__version__}")
except ImportError as e:
    print(f"❌ Error al importar customtkinter: {e}")

# Intentar importar otros paquetes
try:
    import pandas
    print(f"✅ Pandas importado correctamente. Versión: {pandas.__version__}")
except ImportError as e:
    print(f"❌ Error al importar pandas: {e}")

try:
    import PyPDF2
    print(f"✅ PyPDF2 importado correctamente. Versión: {PyPDF2.__version__}")
except ImportError as e:
    print(f"❌ Error al importar PyPDF2: {e}")

try:
    from PIL import Image
    import PIL
    print(f"✅ Pillow importado correctamente. Versión: {PIL.__version__}")
except ImportError as e:
    print(f"❌ Error al importar PIL: {e}")

print("\nRutas de búsqueda actuales:")
for path in sys.path:
    print(f"- {path}") 