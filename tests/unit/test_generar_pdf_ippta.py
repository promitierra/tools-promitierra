import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import shutil
from PIL import Image

# Agregar el directorio src al path para poder importar el módulo
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.scripts.generar_pdf_ippta import generar_pdf_con_imagenes, main

class TestGenerarPdfIppta(unittest.TestCase):
    
    def setUp(self):
        # Crear directorio temporal para las pruebas
        self.temp_dir = tempfile.mkdtemp()
        
        # Crear algunas imágenes de prueba
        self.crear_imagen_prueba(os.path.join(self.temp_dir, "imagen1.jpg"), 800, 600)  # Horizontal
        self.crear_imagen_prueba(os.path.join(self.temp_dir, "imagen2.jpg"), 600, 800)  # Vertical
        
        # Ruta del PDF de salida
        self.ruta_salida = os.path.join(self.temp_dir, "test_output.pdf")
    
    def tearDown(self):
        # Eliminar directorio temporal después de las pruebas
        shutil.rmtree(self.temp_dir)
    
    def crear_imagen_prueba(self, ruta, ancho, alto):
        """Crea una imagen de prueba con dimensiones específicas"""
        img = Image.new('RGB', (ancho, alto), color=(255, 255, 255))
        # Dibujar líneas para simular contenido
        for i in range(0, ancho, 50):
            for j in range(0, alto, 50):
                img.putpixel((i, j), (0, 0, 0))
        img.save(ruta)
    
    def test_generar_pdf_con_imagenes(self):
        """Prueba la generación básica del PDF"""
        generar_pdf_con_imagenes(self.temp_dir, self.ruta_salida)
        
        # Verificar que el PDF se creó correctamente
        self.assertTrue(os.path.exists(self.ruta_salida))
        self.assertTrue(os.path.getsize(self.ruta_salida) > 0)
    
    def test_rotacion_imagen_vertical(self):
        """Prueba que las imágenes verticales se rotan correctamente"""
        # Crear una imagen vertical específica para esta prueba
        ruta_vertical = os.path.join(self.temp_dir, "vertical_test.jpg")
        self.crear_imagen_prueba(ruta_vertical, 600, 800)  # Vertical
        
        # Llamar a la función con un mock para capturar la rotación
        with patch('PIL.Image.Image.rotate') as mock_rotate:
            mock_rotate.return_value = Image.new('RGB', (800, 600))  # Simulamos la rotación
            generar_pdf_con_imagenes(self.temp_dir, self.ruta_salida)
            
            # Verificar que se llamó a rotate al menos una vez
            self.assertTrue(mock_rotate.called)
    
    def test_manejo_errores_imagen_corrupta(self):
        """Prueba el manejo de errores con una imagen corrupta"""
        # Crear un archivo corrupto
        ruta_corrupta = os.path.join(self.temp_dir, "corrupta.jpg")
        with open(ruta_corrupta, 'wb') as f:
            f.write(b'DATOS_CORRUPTOS')
        
        # Verificar que se maneja la excepción
        with self.assertRaises(Exception):
            generar_pdf_con_imagenes(self.temp_dir, self.ruta_salida)
    
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function(self, mock_args):
        """Prueba la función main con argumentos simulados"""
        # Configurar los argumentos simulados
        mock_args.return_value = MagicMock(
            directorio=self.temp_dir,
            output=self.ruta_salida,
            debug=False
        )
        
        # Llamar a la función main
        main()
        
        # Verificar que el PDF se creó correctamente
        self.assertTrue(os.path.exists(self.ruta_salida))
        self.assertTrue(os.path.getsize(self.ruta_salida) > 0)
    
    def test_debug_mode(self):
        """Prueba que el modo debug funciona correctamente"""
        with patch('reportlab.pdfgen.canvas.Canvas.line') as mock_line:
            generar_pdf_con_imagenes(self.temp_dir, self.ruta_salida, debug=True)
            
            # En modo debug, se deben dibujar líneas para los márgenes
            self.assertTrue(mock_line.called)
            # Verificar que se llamó 4 veces (para los 4 márgenes)
            self.assertGreaterEqual(mock_line.call_count, 4)

if __name__ == '__main__':
    unittest.main() 