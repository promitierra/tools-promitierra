"""
Main entry point for the PDF converter application.
"""
import sys
from pathlib import Path

# Add src directory to Python path
src_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from src.app.gui import ImagenAPdfGUI

def main():
    """Punto de entrada principal de la aplicación"""
    app = ImagenAPdfGUI()
    app.iniciar()

if __name__ == "__main__":
    main()
