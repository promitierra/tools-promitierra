import unittest
import os
import tempfile
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from src.app.pdf_converter import PDFConverter
from PIL import Image

class TestPDFConverter(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.temp_dir = tempfile.mkdtemp()
        self.converter = PDFConverter()
        
        # Crear imágenes de prueba
        self.crear_imagenes_prueba()
        
    def tearDown(self):
        """Limpieza después de cada prueba"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def crear_imagenes_prueba(self):
        """Crear imágenes de prueba en diferentes formatos"""
        # Imagen RGB normal
        img_rgb = Image.new('RGB', (100, 100), color='red')
        img_rgb.save(os.path.join(self.temp_dir, 'test_rgb.png'))
        
        # Imagen RGBA con transparencia
        img_rgba = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
        img_rgba.save(os.path.join(self.temp_dir, 'test_rgba.png'))
        
        # Imagen en escala de grises
        img_gray = Image.new('L', (100, 100), color=128)
        img_gray.save(os.path.join(self.temp_dir, 'test_gray.jpg'))
        
        # Imagen grande para prueba de redimensionamiento
        img_large = Image.new('RGB', (3000, 3000), color='blue')
        img_large.save(os.path.join(self.temp_dir, 'test_large.jpg'))
        
        # Crear una imagen corrupta
        with open(os.path.join(self.temp_dir, 'corrupted.jpg'), 'wb') as f:
            f.write(b'Not an image file')
        
        # Crear subdirectorio con imagen
        os.makedirs(os.path.join(self.temp_dir, 'subdir'))
        img_sub = Image.new('RGB', (100, 100), color='green')
        img_sub.save(os.path.join(self.temp_dir, 'subdir', 'test_sub.png'))
    
    def test_conversion_simple(self):
        """Prueba conversión básica de imagen a PDF"""
        class MockCallbacks:
            def __init__(self):
                self.started = False
                self.files_found = 0
                self.converted = []
                self.errors = []
                self.completed = False
                
            def on_start(self): self.started = True
            def on_images_found(self, total): self.files_found = total
            def on_file_converted(self, name): self.converted.append(name)
            def on_file_error(self, name, error): self.errors.append((name, error))
            def on_complete(self, *args): self.completed = True
            def on_progress(self, *args): pass
            def on_processing_file(self, *args): pass
            def on_finish(self): pass
            
        callbacks = MockCallbacks()
        self.converter.procesar_carpeta(self.temp_dir, False, callbacks)
        
        self.assertTrue(callbacks.started)
        self.assertEqual(callbacks.files_found, 6)  # Total de imágenes
        self.assertEqual(len(callbacks.converted), 5)  # Imágenes convertidas exitosamente
        self.assertEqual(len(callbacks.errors), 1)  # 1 imagen corrupta
        self.assertTrue(callbacks.completed)
    
    def test_conversion_paralela(self):
        """Prueba que la conversión paralela funciona correctamente"""
        tiempos = []
        for num_workers in [1, 2, 4]:  # Probar con diferente número de workers
            self.converter.max_workers = num_workers
            
            inicio = time.time()
            class TimingCallbacks:
                def __init__(self):
                    self.completed = False
                def on_start(self): pass
                def on_images_found(self, total): pass
                def on_file_converted(self, name): pass
                def on_file_error(self, name, error): pass
                def on_complete(self, *args): self.completed = True
                def on_progress(self, *args): pass
                def on_processing_file(self, *args): pass
                def on_finish(self): pass
            
            callbacks = TimingCallbacks()
            self.converter.procesar_carpeta(self.temp_dir, False, callbacks)
            tiempo_total = time.time() - inicio
            tiempos.append(tiempo_total)
        
        # El tiempo con más workers debería ser menor
        self.assertLess(tiempos[2], tiempos[0])
    
    def test_cancelacion(self):
        """Prueba la funcionalidad de cancelación"""
        class CancelCallbacks:
            def __init__(self):
                self.files_processed = 0
                self.finished = False
            def on_start(self): pass
            def on_images_found(self, total): pass
            def on_file_converted(self, name): self.files_processed += 1
            def on_file_error(self, name, error): pass
            def on_complete(self, *args): pass
            def on_progress(self, *args): pass
            def on_processing_file(self, *args): pass
            def on_finish(self): self.finished = True
        
        callbacks = CancelCallbacks()
        
        # Iniciar conversión en un hilo separado
        import threading
        thread = threading.Thread(
            target=self.converter.procesar_carpeta,
            args=(self.temp_dir, False, callbacks)
        )
        thread.start()
        
        # Esperar un momento y cancelar
        time.sleep(0.1)
        self.converter.cancelar_proceso()
        thread.join()
        
        # Verificar que se canceló correctamente
        self.assertTrue(callbacks.finished)
        self.assertLess(callbacks.files_processed, 6)  # No todas las imágenes procesadas
    
    def test_manejo_memoria(self):
        """Prueba el manejo de memoria con imágenes grandes"""
        # Crear una imagen muy grande
        img_huge = Image.new('RGB', (4000, 4000), color='red')
        huge_path = os.path.join(self.temp_dir, 'huge.jpg')
        img_huge.save(huge_path)
        
        class MemoryCallbacks:
            def __init__(self):
                self.converted = []
            def on_start(self): pass
            def on_images_found(self, total): pass
            def on_file_converted(self, name): self.converted.append(name)
            def on_file_error(self, name, error): pass
            def on_complete(self, *args): pass
            def on_progress(self, *args): pass
            def on_processing_file(self, *args): pass
            def on_finish(self): pass
        
        callbacks = MemoryCallbacks()
        self.converter.procesar_carpeta(self.temp_dir, False, callbacks)
        
        # Verificar que la imagen fue convertida
        self.assertIn('huge.jpg', callbacks.converted)
        
        # Verificar que el PDF resultante existe y tiene un tamaño razonable
        pdf_path = os.path.join(self.temp_dir, 'huge.pdf')
        self.assertTrue(os.path.exists(pdf_path))
        pdf_size = os.path.getsize(pdf_path)
        original_size = os.path.getsize(huge_path)
        self.assertLess(pdf_size, original_size)  # El PDF debe ser más pequeño
    
    def test_formatos_imagen(self):
        """Prueba la conversión de diferentes formatos de imagen"""
        # Crear un directorio temporal específico para esta prueba
        test_dir = os.path.join(self.temp_dir, 'formatos_test')
        os.makedirs(test_dir)
        
        formatos = {
            'RGB': (255, 0, 0),
            'RGBA': (255, 0, 0, 128),
            'L': 128,
            'P': (255, 0, 0)
        }
        
        # Crear imágenes en diferentes formatos
        for formato, color in formatos.items():
            if formato == 'P':
                img = Image.new('RGB', (100, 100), color).convert('P')
            else:
                img = Image.new(formato, (100, 100), color)
            
            test_file = os.path.join(test_dir, f'test_{formato.lower()}.png')
            img.save(test_file)
            
            # Verificar que la imagen se creó correctamente
            self.assertTrue(os.path.exists(test_file), f"No se pudo crear la imagen {formato}")
        
        class FormatCallbacks:
            def __init__(self):
                self.converted = []
                self.errors = []
            def on_start(self): pass
            def on_images_found(self, total): pass
            def on_file_converted(self, name): 
                print(f"Convertido: {name}")
                self.converted.append(name)
            def on_file_error(self, name, error): 
                print(f"Error en {name}: {error}")
                self.errors.append((name, error))
            def on_complete(self, *args): pass
            def on_progress(self, *args): pass
            def on_processing_file(self, *args): pass
            def on_finish(self): pass
        
        callbacks = FormatCallbacks()
        self.converter.procesar_carpeta(test_dir, False, callbacks)
        
        # Verificar cada formato individualmente
        for formato in formatos:
            test_file = f'test_{formato.lower()}.png'
            self.assertIn(test_file, callbacks.converted, 
                         f"Fallo al convertir formato {formato}")
            
            # Verificar que el PDF se creó correctamente
            pdf_path = os.path.join(test_dir, f'test_{formato.lower()}.pdf')
            self.assertTrue(os.path.exists(pdf_path), 
                          f"No se creó el PDF para formato {formato}")
        
        # Verificar que no hubo errores
        if callbacks.errors:
            for nombre, error in callbacks.errors:
                print(f"Error inesperado en {nombre}: {error}")
        self.assertEqual(len(callbacks.errors), 0, 
                        "Se encontraron errores en la conversión")
    
    def test_filtrado_patron(self):
        """Prueba el filtrado por patrón personalizado"""
        # Crear imágenes con diferentes nombres
        patrones = {
            'foto_1.jpg': 'RGB',
            'foto_2.png': 'RGB',
            'imagen_1.jpg': 'RGB',
            'imagen_2.png': 'RGB',
            'test.jpg': 'RGB'
        }
        
        # Crear las imágenes
        test_dir = os.path.join(self.temp_dir, 'patron_test')
        os.makedirs(test_dir)
        
        for nombre, modo in patrones.items():
            img = Image.new(modo, (100, 100), color='red')
            img.save(os.path.join(test_dir, nombre))
        
        class PatronCallbacks:
            def __init__(self):
                self.converted = []
            def on_start(self): pass
            def on_images_found(self, total): self.total = total
            def on_file_converted(self, name): self.converted.append(name)
            def on_file_error(self, name, error): pass
            def on_complete(self, *args): pass
            def on_progress(self, *args): pass
            def on_processing_file(self, *args): pass
            def on_finish(self): pass
        
        # Probar diferentes patrones
        pruebas = [
            ('foto_*.jpg', 1),    # Debe encontrar foto_1.jpg
            ('*.png', 2),         # Debe encontrar foto_2.png e imagen_2.png
            ('imagen_*.*', 2),    # Debe encontrar imagen_1.jpg e imagen_2.png
            ('test.*', 1),        # Debe encontrar test.jpg
            ('*.jpg', 3)          # Debe encontrar todos los .jpg
        ]
        
        for patron, esperados in pruebas:
            callbacks = PatronCallbacks()
            self.converter.procesar_carpeta(test_dir, False, callbacks, patron)
            self.assertEqual(
                len(callbacks.converted), 
                esperados, 
                f"Patrón '{patron}' encontró {len(callbacks.converted)} archivos, esperaba {esperados}"
            )
    
    def test_extension_case(self):
        """Prueba que las extensiones son case-insensitive"""
        # Crear imágenes con extensiones en diferentes casos
        extensiones = ['.jpg', '.PNG']  # Solo dos extensiones diferentes
        test_dir = os.path.join(self.temp_dir, 'extension_test')
        os.makedirs(test_dir)
        
        # Crear dos archivos con nombres diferentes
        img = Image.new('RGB', (100, 100), color='red')
        img.save(os.path.join(test_dir, f'test1{extensiones[0]}'))  # test1.jpg
        img.save(os.path.join(test_dir, f'test2{extensiones[1]}'))  # test2.PNG
        
        class ExtCallbacks:
            def __init__(self):
                self.converted = []
            def on_start(self): pass
            def on_images_found(self, total): self.total = total
            def on_file_converted(self, name): self.converted.append(name)
            def on_file_error(self, name, error): pass
            def on_complete(self, *args): pass
            def on_progress(self, *args): pass
            def on_processing_file(self, *args): pass
            def on_finish(self): pass
        
        callbacks = ExtCallbacks()
        self.converter.procesar_carpeta(test_dir, False, callbacks)
        
        # Debería encontrar las dos imágenes independientemente del caso
        self.assertEqual(len(callbacks.converted), len(extensiones))
