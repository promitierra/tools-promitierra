import subprocess
import sys
import os

def install_dependencies():
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Comprobar si estamos en un entorno virtual
    in_venv = sys.prefix != sys.base_prefix
    print(f"¿Estamos en un entorno virtual?: {in_venv}")
    print(f"Python ejecutable: {sys.executable}")
    print(f"Ruta de búsqueda de Python: {sys.path}")
    
    # Instalar las dependencias principales
    packages = [
        "customtkinter==5.2.2",
        "pandas==2.2.1",
        "PyPDF2==3.0.1",
        "Pillow==10.2.0",
        "opencv-python==4.8.1.78"
    ]
    
    for package in packages:
        print(f"Instalando {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} instalado correctamente")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al instalar {package}: {e}")
    
    # Verificar las instalaciones
    try:
        print("\nVerificando instalaciones...")
        import customtkinter
        print("✅ customtkinter importado correctamente")
        
        import pandas
        print("✅ pandas importado correctamente")
        
        import PyPDF2
        print("✅ PyPDF2 importado correctamente")
        
        from PIL import Image
        print("✅ Pillow importado correctamente")
        
        import cv2
        print("✅ opencv-python importado correctamente")
        
        print("\n✅ Todas las dependencias están instaladas y funcionando correctamente.")
    except ImportError as e:
        print(f"❌ Error al importar una dependencia: {e}")

if __name__ == "__main__":
    install_dependencies() 