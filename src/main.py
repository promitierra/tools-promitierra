"""
Main entry point for the PDF converter application.
"""
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gui import MainWindow

def main():
    """Application entry point."""
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
