"""
Pruebas unitarias para el módulo FolderCreator.
"""
import os
import tempfile
import unittest
import pandas as pd

from src.core.folder_creator import FolderCreator

class TestFolderCreator(unittest.TestCase):
    """Pruebas para la creación de carpetas desde plantillas Excel."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.temp_dir = tempfile.mkdtemp()
        self.folder_creator = FolderCreator()
    
    def test_crear_plantilla(self):
        """Probar la creación de una plantilla Excel."""
        plantilla_path = os.path.join(self.temp_dir, 'plantilla_test.xlsx')
        
        # Crear plantilla
        exito, mensaje = self.folder_creator.crear_plantilla(plantilla_path)
        
        # Verificar
        self.assertTrue(exito)
        self.assertTrue(os.path.exists(plantilla_path))
        
        # Leer plantilla
        df = pd.read_excel(plantilla_path)
        
        # Verificar columnas
        columnas_esperadas = ['ID', 'NOMBRES', 'APELLIDOS', 'CATEGORIA']
        self.assertTrue(all(col in df.columns for col in columnas_esperadas))
    
    def test_procesar_plantilla_exitoso(self):
        """Probar procesamiento de plantilla Excel."""
        # Crear plantilla de prueba
        plantilla_path = os.path.join(self.temp_dir, 'plantilla_proceso.xlsx')
        df = pd.DataFrame({
            'ID': ['001', '002'],
            'NOMBRES': ['Juan', 'María'],
            'APELLIDOS': ['Pérez', 'García']
        })
        df.to_excel(plantilla_path, index=False)
        
        # Procesar plantilla
        exito, mensaje = self.folder_creator.procesar_plantilla(
            plantilla_path, 
            self.temp_dir
        )
        
        # Verificar
        self.assertTrue(exito)
        self.assertIn("Carpetas creadas: 2", mensaje)
        
        # Verificar carpetas creadas directamente en el directorio temporal
        carpetas_esperadas = [
            '1 - JUAN PEREZ',
            '2 - MARIA GARCIA'
        ]
        for carpeta in carpetas_esperadas:
            ruta_carpeta = os.path.join(self.temp_dir, carpeta)
            self.assertTrue(os.path.exists(ruta_carpeta), 
                         f"No se creó la carpeta {carpeta}")
    
    def test_procesar_plantilla_con_callbacks(self):
        """Probar procesamiento de plantilla con callbacks."""
        class MockCallbacks:
            def __init__(self):
                self.carpetas_creadas = []
                self.carpetas_existentes = []
                self.errores = []
                self.start_called = False
            
            def on_folder_created(self, nombre_carpeta):
                self.carpetas_creadas.append(nombre_carpeta)
            
            def on_folder_exists(self, nombre_carpeta):
                self.carpetas_existentes.append(nombre_carpeta)
            
            def on_folder_error(self, nombre_carpeta, error):
                self.errores.append((nombre_carpeta, error))
                
            def on_start(self, total):
                self.start_called = True
        
        # Crear plantilla de prueba
        plantilla_path = os.path.join(self.temp_dir, 'plantilla_callbacks.xlsx')
        df = pd.DataFrame({
            'ID': ['001', '002'],  # No duplicados
            'NOMBRES': ['Juan', 'María']
        })
        df.to_excel(plantilla_path, index=False)
        
        # Crear una carpeta existente para simular que ya existe
        os.makedirs(os.path.join(self.temp_dir, '1 - JUAN'), exist_ok=True)
        
        # Callbacks
        callbacks = MockCallbacks()
        
        # Procesar plantilla
        exito, mensaje = self.folder_creator.procesar_plantilla(
            plantilla_path, 
            self.temp_dir,
            callbacks
        )
        
        # Verificar
        self.assertTrue(exito)
        self.assertTrue(callbacks.start_called)
        
        # Verificar que solo se creó una carpeta (la otra ya existía)
        self.assertEqual(len(callbacks.carpetas_creadas), 1)
        
        # Verificar nombres creados
        created_names = [name.upper() for name in callbacks.carpetas_creadas]
        self.assertIn('2 - MARIA', created_names)
        
        # Verificar si se registró la carpeta existente
        if callbacks.carpetas_existentes:
            self.assertEqual(len(callbacks.carpetas_existentes), 1)
            existing_names = [name.upper() for name in callbacks.carpetas_existentes]
            self.assertIn('1 - JUAN', existing_names)
    
    def test_procesar_plantilla_sin_columnas_requeridas(self):
        """Probar procesamiento de plantilla sin columnas requeridas."""
        # Crear plantilla sin columnas requeridas
        plantilla_path = os.path.join(self.temp_dir, 'plantilla_invalida.xlsx')
        df = pd.DataFrame({
            'COLUMNA_INVALIDA': ['Dato']
        })
        df.to_excel(plantilla_path, index=False)
        
        # Procesar plantilla
        exito, mensaje = self.folder_creator.procesar_plantilla(
            plantilla_path, 
            self.temp_dir
        )
        
        # Verificar
        self.assertFalse(exito)
        self.assertIn("Columna 'ID' no encontrada", mensaje)

if __name__ == '__main__':
    unittest.main()
