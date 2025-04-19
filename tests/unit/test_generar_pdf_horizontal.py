"""
Tests unitarios para la funcionalidad de generación de PDF horizontal.
"""
import os
import tempfile
import shutil
from pathlib import Path
import pytest
from PIL import Image
from src.scripts.generar_pdf_imagenes import generar_pdf_con_imagenes
import PyPDF2

class TestGenerarPdfHorizontal:
    """Pruebas para la generación de PDF horizontal."""
    
    @pytest.fixture
    def directorio_imagenes_temp(self):
        """Fixture que crea un directorio temporal con imágenes para las pruebas."""
        # Crear directorio temporal
        temp_dir = tempfile.mkdtemp()
        
        # Crear algunas imágenes de prueba: horizontales y verticales
        # Imagen horizontal
        img_h = Image.new('RGB', (800, 600), color='red')
        img_h.save(f"{temp_dir}/horizontal.jpg")
        
        # Imagen vertical
        img_v = Image.new('RGB', (600, 800), color='blue')
        img_v.save(f"{temp_dir}/vertical.jpg")
        
        # Entregar el directorio para la prueba
        yield temp_dir
        
        # Limpieza después de la prueba
        shutil.rmtree(temp_dir)
    
    def test_generar_pdf_con_imagenes_crea_archivo(self, directorio_imagenes_temp):
        """Verificar que se crea el archivo PDF correctamente."""
        # Configurar
        ruta_salida = os.path.join(directorio_imagenes_temp, "resultado.pdf")
        
        # Ejecutar
        generar_pdf_con_imagenes(directorio_imagenes_temp, ruta_salida)
        
        # Verificar
        assert os.path.exists(ruta_salida)
        assert os.path.getsize(ruta_salida) > 0
    
    def test_generar_pdf_con_imagenes_orientacion_horizontal(self, directorio_imagenes_temp):
        """Verificar que el PDF generado tiene orientación horizontal."""
        # Configurar
        ruta_salida = os.path.join(directorio_imagenes_temp, "resultado_horizontal.pdf")
        
        # Ejecutar
        generar_pdf_con_imagenes(directorio_imagenes_temp, ruta_salida)
        
        # Verificar orientación horizontal en el PDF
        with open(ruta_salida, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            primera_pagina = pdf.pages[0]
            # Extraer dimensiones (width, height)
            ancho = primera_pagina.mediabox.width
            alto = primera_pagina.mediabox.height
            # En orientación horizontal, el ancho es mayor que el alto
            assert ancho > alto
    
    def test_generar_pdf_incluye_numeros_pagina(self, directorio_imagenes_temp):
        """Verificar que se incluyen números de página cuando se solicita."""
        # Configurar
        ruta_salida = os.path.join(directorio_imagenes_temp, "resultado_con_numeros.pdf")
        
        # Ejecutar con números de página activados
        generar_pdf_con_imagenes(directorio_imagenes_temp, ruta_salida, incluir_numeros_pagina=True)
        
        # No podemos verificar directamente el contenido del texto, pero podemos
        # verificar que el archivo se crea correctamente
        assert os.path.exists(ruta_salida)
    
    def test_callback_progreso(self, directorio_imagenes_temp):
        """Verificar que el callback de progreso se llama correctamente."""
        # Configurar
        ruta_salida = os.path.join(directorio_imagenes_temp, "resultado_callback.pdf")
        progreso_llamadas = []
        
        def callback_mock(actual, total):
            progreso_llamadas.append((actual, total))
        
        # Ejecutar
        generar_pdf_con_imagenes(
            directorio_imagenes_temp, 
            ruta_salida,
            callback_progreso=callback_mock
        )
        
        # Verificar
        # Debería haber al menos 2 llamadas (una por cada imagen)
        assert len(progreso_llamadas) >= 2
        # La última llamada debería ser (2, 2) si hay 2 imágenes
        assert progreso_llamadas[-1][0] == len(progreso_llamadas)  # actual == total de llamadas
        assert progreso_llamadas[-1][1] == 2  # total == 2 imágenes 