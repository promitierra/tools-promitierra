"""
Main entry point for the PDF converter application.
"""
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from src.app.gui import ImagenAPdfGUI

def main():
    """Punto de entrada principal de la aplicación"""
    app = ImagenAPdfGUI()
    app.iniciar()

if __name__ == "__main__":
    main()
