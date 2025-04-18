import os
import unittest
import tempfile
import shutil
import fitz  # PyMuPDF
from PIL import Image
import io
import logging
import sys

# Importar el módulo a probar
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from imagenes_pdf_a_png import convert_pdf_to_png, find_pdf_files

class TestPdfToPngConverter(unittest.TestCase):
    def setUp(self):
        # Crear un directorio temporal para las pruebas
        self.test_dir = tempfile.mkdtemp()
        
        # Configurar logging para las pruebas
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
        
        # Directorio actual donde se encuentra el script
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
    
    def tearDown(self):
        # Limpiar el directorio temporal después de las pruebas
        shutil.rmtree(self.test_dir)
    
    def create_pdf_with_one_image(self, filename):
        """Crear un PDF con una sola imagen"""
        pdf_path = os.path.join(self.test_dir, filename)
        
        # Crear un documento PDF
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)  # A4
        
        # Crear una imagen simple
        img_data = Image.new('RGB', (300, 300), color='red')
        img_bytes = io.BytesIO()
        img_data.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Insertar la imagen en el PDF
        page.insert_image(fitz.Rect(100, 100, 400, 400), stream=img_bytes.getvalue())
        
        # Guardar el PDF
        doc.save(pdf_path)
        doc.close()
        
        return pdf_path
    
    def create_pdf_with_two_images(self, filename):
        """Crear un PDF con dos imágenes"""
        pdf_path = os.path.join(self.test_dir, filename)
        
        # Crear un documento PDF
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)  # A4
        
        # Crear dos imágenes simples
        img1_data = Image.new('RGB', (200, 200), color='blue')
        img1_bytes = io.BytesIO()
        img1_data.save(img1_bytes, format='PNG')
        img1_bytes.seek(0)
        
        img2_data = Image.new('RGB', (200, 200), color='green')
        img2_bytes = io.BytesIO()
        img2_data.save(img2_bytes, format='PNG')
        img2_bytes.seek(0)
        
        # Insertar las imágenes en el PDF
        page.insert_image(fitz.Rect(50, 50, 250, 250), stream=img1_bytes.getvalue())
        page.insert_image(fitz.Rect(300, 300, 500, 500), stream=img2_bytes.getvalue())
        
        # Guardar el PDF
        doc.save(pdf_path)
        doc.close()
        
        return pdf_path
    
    def create_pdf_with_multiple_images(self, filename):
        """Crear un PDF con múltiples imágenes en varias páginas"""
        pdf_path = os.path.join(self.test_dir, filename)
        
        # Crear un documento PDF
        doc = fitz.open()
        
        # Página 1 con 2 imágenes
        page1 = doc.new_page(width=595, height=842)  # A4
        img1_data = Image.new('RGB', (200, 200), color='red')
        img1_bytes = io.BytesIO()
        img1_data.save(img1_bytes, format='PNG')
        img1_bytes.seek(0)
        
        img2_data = Image.new('RGB', (200, 200), color='blue')
        img2_bytes = io.BytesIO()
        img2_data.save(img2_bytes, format='PNG')
        img2_bytes.seek(0)
        
        page1.insert_image(fitz.Rect(50, 50, 250, 250), stream=img1_bytes.getvalue())
        page1.insert_image(fitz.Rect(300, 300, 500, 500), stream=img2_bytes.getvalue())
        
        # Página 2 con 1 imagen
        page2 = doc.new_page(width=595, height=842)  # A4
        img3_data = Image.new('RGB', (300, 300), color='green')
        img3_bytes = io.BytesIO()
        img3_data.save(img3_bytes, format='PNG')
        img3_bytes.seek(0)
        
        page2.insert_image(fitz.Rect(100, 100, 400, 400), stream=img3_bytes.getvalue())
        
        # Guardar el PDF
        doc.save(pdf_path)
        doc.close()
        
        return pdf_path
    
    def create_pdf_without_images(self, filename):
        """Crear un PDF sin imágenes incrustadas"""
        pdf_path = os.path.join(self.test_dir, filename)
        
        # Crear un documento PDF
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)  # A4
        
        # Agregar texto al PDF
        text_point = fitz.Point(72, 72)
        page.insert_text(text_point, "Este es un PDF sin imágenes incrustadas", fontsize=12)
        
        # Guardar el PDF
        doc.save(pdf_path)
        doc.close()
        
        return pdf_path
    
    def create_empty_pdf(self, filename):
        """Crear un PDF vacío"""
        pdf_path = os.path.join(self.test_dir, filename)
        
        # Crear un documento PDF sin páginas
        doc = fitz.open()
        doc.save(pdf_path)
        doc.close()
        
        return pdf_path
    
    def test_convert_pdf_with_one_image(self):
        """Probar la conversión de un PDF con una sola imagen"""
        pdf_path = self.create_pdf_with_one_image("test_one_image.pdf")
        
        # Ejecutar la conversión
        result = convert_pdf_to_png(pdf_path)
        
        # Verificar que la conversión fue exitosa
        self.assertTrue(result)
        
        # Verificar que se creó el archivo PNG
        png_path = os.path.splitext(pdf_path)[0] + ".png"
        self.assertTrue(os.path.exists(png_path))
        
        # Verificar que el archivo PNG es válido
        try:
            with Image.open(png_path) as img:
                img.verify()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"El archivo PNG no es válido: {str(e)}")
    
    def test_convert_pdf_with_two_images(self):
        """Probar la conversión de un PDF con dos imágenes"""
        pdf_path = self.create_pdf_with_two_images("test_two_images.pdf")
        
        # Ejecutar la conversión
        result = convert_pdf_to_png(pdf_path)
        
        # Verificar que la conversión fue exitosa
        self.assertTrue(result)
        
        # Verificar que se crearon los archivos PNG con el formato correcto
        png_base_path = os.path.splitext(pdf_path)[0]
        png_path1 = f"{png_base_path}_1.png"
        png_path2 = f"{png_base_path}_2.png"
        
        self.assertTrue(os.path.exists(png_path1))
        self.assertTrue(os.path.exists(png_path2))
        
        # Verificar que los archivos PNG son válidos
        try:
            with Image.open(png_path1) as img:
                img.verify()
            with Image.open(png_path2) as img:
                img.verify()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Uno de los archivos PNG no es válido: {str(e)}")
    
    def test_convert_pdf_with_multiple_images(self):
        """Probar la conversión de un PDF con múltiples imágenes en varias páginas"""
        pdf_path = self.create_pdf_with_multiple_images("test_multiple_images.pdf")
        
        # Ejecutar la conversión
        result = convert_pdf_to_png(pdf_path)
        
        # Verificar que la conversión fue exitosa
        self.assertTrue(result)
        
        # Verificar que se crearon los archivos PNG con el formato correcto para múltiples imágenes
        png_base_path = os.path.splitext(pdf_path)[0]
        
        # Buscar archivos que coincidan con el patrón esperado
        png_files = [f for f in os.listdir(self.test_dir) if f.startswith(os.path.basename(png_base_path)) and f.endswith(".png")]
        
        # Debe haber al menos 3 imágenes (2 en la página 1 y 1 en la página 2)
        self.assertGreaterEqual(len(png_files), 3)
        
        # Verificar que los archivos PNG son válidos
        for png_file in png_files:
            png_path = os.path.join(self.test_dir, png_file)
            try:
                with Image.open(png_path) as img:
                    img.verify()
            except Exception as e:
                self.fail(f"El archivo PNG {png_file} no es válido: {str(e)}")
    
    def test_convert_pdf_without_images(self):
        """Probar la conversión de un PDF sin imágenes incrustadas"""
        pdf_path = self.create_pdf_without_images("test_no_images.pdf")
        
        # Ejecutar la conversión
        result = convert_pdf_to_png(pdf_path)
        
        # Verificar que la conversión fue exitosa (debería recurrir a la conversión de página)
        self.assertTrue(result)
        
        # Verificar que se creó el archivo PNG
        png_path = os.path.splitext(pdf_path)[0] + ".png"
        self.assertTrue(os.path.exists(png_path))
        
        # Verificar que el archivo PNG es válido
        try:
            with Image.open(png_path) as img:
                img.verify()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"El archivo PNG no es válido: {str(e)}")
    
    def test_convert_empty_pdf(self):
        """Probar la conversión de un PDF vacío"""
        pdf_path = self.create_empty_pdf("test_empty.pdf")
        
        # Ejecutar la conversión
        result = convert_pdf_to_png(pdf_path)
        
        # Verificar que la conversión falló (PDF sin páginas)
        self.assertFalse(result)
    
    def test_find_pdf_files(self):
        """Probar la función de búsqueda de archivos PDF"""
        # Crear varios archivos PDF en el directorio de prueba
        self.create_pdf_with_one_image("test1.pdf")
        self.create_pdf_with_two_images("test2.pdf")
        self.create_pdf_with_multiple_images("test3.pdf")
        
        # Crear un subdirectorio con más archivos PDF
        subdir = os.path.join(self.test_dir, "subdir")
        os.makedirs(subdir)
        
        # Crear un PDF en el subdirectorio
        doc = fitz.open()
        page = doc.new_page()
        doc.save(os.path.join(subdir, "test4.pdf"))
        doc.close()
        
        # Ejecutar la función de búsqueda
        pdf_files = find_pdf_files(self.test_dir)
        
        # Verificar que se encontraron todos los archivos PDF
        self.assertEqual(len(pdf_files), 4)

if __name__ == "__main__":
    unittest.main()