import unittest
import os
import tempfile
import shutil
import pandas as pd
from src.app.folder_creator import FolderCreator

class TestFolderCreator(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.temp_dir = tempfile.mkdtemp()
        self.creator = FolderCreator()
        
        # Crear plantilla de prueba
        self.test_excel = os.path.join(self.temp_dir, 'test.xlsx')
        df = pd.DataFrame({
            'ID': ['1', '2', '3'],
            'NOMBRES': ['Juan', 'María', 'Pedro'],
            'APELLIDOS': ['Pérez', 'García', 'López']
        })
        df.to_excel(self.test_excel, index=False)
        
        # Crear plantilla inválida
        self.invalid_excel = os.path.join(self.temp_dir, 'invalid.xlsx')
        df_invalid = pd.DataFrame({
            'NOMBRE': ['Juan'],  # Columnas incorrectas
            'EDAD': [25]
        })
        df_invalid.to_excel(self.invalid_excel, index=False)

    def tearDown(self):
        """Limpieza después de cada prueba"""
        shutil.rmtree(self.temp_dir)

    def test_crear_plantilla(self):
        """Prueba la creación de plantilla Excel"""
        plantilla_path = os.path.join(self.temp_dir, 'plantilla.xlsx')
        success, message = self.creator.crear_plantilla(plantilla_path)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(plantilla_path))
        
        # Verificar estructura
        df = pd.read_excel(plantilla_path)
        self.assertListEqual(list(df.columns), ['ID', 'NOMBRES', 'APELLIDOS'])

    def test_procesar_plantilla_valida(self):
        """Prueba el procesamiento de una plantilla válida"""
        output_dir = os.path.join(self.temp_dir, 'output')
        
        class MockCallbacks:
            def __init__(self):
                self.created = []
                self.errors = []
            def on_folder_created(self, name): self.created.append(name)
            def on_folder_error(self, name, error): self.errors.append((name, error))
            def on_folder_exists(self, name): pass
            
        callbacks = MockCallbacks()
        success, result = self.creator.procesar_plantilla(self.test_excel, output_dir, callbacks)
        
        self.assertTrue(success)
        self.assertEqual(len(callbacks.created), 3)
        self.assertEqual(len(callbacks.errors), 0)
        
        # Verificar carpetas creadas
        self.assertTrue(os.path.exists(os.path.join(output_dir, '1 - Juan Pérez')))
        self.assertTrue(os.path.exists(os.path.join(output_dir, '2 - María García')))
        self.assertTrue(os.path.exists(os.path.join(output_dir, '3 - Pedro López')))

    def test_procesar_plantilla_invalida(self):
        """Prueba el procesamiento de una plantilla inválida"""
        output_dir = os.path.join(self.temp_dir, 'output')
        
        class MockCallbacks:
            def __init__(self):
                self.created = []
                self.errors = []
            def on_folder_created(self, name): self.created.append(name)
            def on_folder_error(self, name, error): self.errors.append((name, error))
            def on_folder_exists(self, name): pass
            
        callbacks = MockCallbacks()
        success, result = self.creator.procesar_plantilla(self.invalid_excel, output_dir, callbacks)
        
        self.assertFalse(success)
        self.assertEqual(len(callbacks.created), 0)

    def test_nombres_especiales(self):
        """Prueba la creación de carpetas con nombres especiales"""
        special_excel = os.path.join(self.temp_dir, 'special.xlsx')
        df = pd.DataFrame({
            'ID': ['1', '2'],  
            'NOMBRES': ['Ana María', 'José #'],
            'APELLIDOS': ['Pérez.', 'García?']
        })
        df.to_excel(special_excel, index=False)
        
        output_dir = os.path.join(self.temp_dir, 'output')
        
        class MockCallbacks:
            def __init__(self):
                self.created = []
                self.errors = []
            def on_folder_created(self, name): self.created.append(name)
            def on_folder_error(self, name, error): self.errors.append((name, error))
            def on_folder_exists(self, name): pass
            
        callbacks = MockCallbacks()
        success, result = self.creator.procesar_plantilla(special_excel, output_dir, callbacks)
        
        self.assertTrue(success)
        self.assertEqual(len(callbacks.created), 2)  

    def test_carpetas_duplicadas(self):
        """Prueba el manejo de carpetas duplicadas"""
        duplicate_excel = os.path.join(self.temp_dir, 'duplicate.xlsx')
        df = pd.DataFrame({
            'ID': ['1', '1'],  # IDs duplicados
            'NOMBRES': ['Juan', 'Juan'],
            'APELLIDOS': ['Pérez', 'Pérez']
        })
        df.to_excel(duplicate_excel, index=False)
        
        output_dir = os.path.join(self.temp_dir, 'output')
        os.makedirs(output_dir)
        
        class MockCallbacks:
            def __init__(self):
                self.created = []
                self.existing = []
            def on_folder_created(self, name): self.created.append(name)
            def on_folder_error(self, name, error): pass
            def on_folder_exists(self, name): self.existing.append(name)
            
        callbacks = MockCallbacks()
        success, result = self.creator.procesar_plantilla(duplicate_excel, output_dir, callbacks)
        
        self.assertTrue(success)
        self.assertEqual(len(callbacks.created), 1)
        self.assertEqual(len(callbacks.existing), 1)

    def test_permisos_directorio(self):
        """Prueba el manejo de errores de permisos"""
        if os.name != 'nt':  # Skip en Windows
            restricted_dir = os.path.join(self.temp_dir, 'restricted')
            os.makedirs(restricted_dir)
            os.chmod(restricted_dir, 0o000)
            
            class MockCallbacks:
                def __init__(self):
                    self.errors = []
                def on_folder_created(self, name): pass
                def on_folder_error(self, name, error): self.errors.append((name, error))
                def on_folder_exists(self, name): pass
                
            callbacks = MockCallbacks()
            success, result = self.creator.procesar_plantilla(self.test_excel, restricted_dir, callbacks)
            
            self.assertFalse(success)
            self.assertTrue(len(callbacks.errors) > 0)
