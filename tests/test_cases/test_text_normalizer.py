"""
Tests para el módulo de normalización de texto.
"""

import unittest
import os
import shutil
import pandas as pd
from src.core.text_normalizer import TextNormalizer

class TestTextNormalizer(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.normalizer = TextNormalizer()
        self.test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'test_output')
        
        # Crear directorio de pruebas si no existe
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
            
    def tearDown(self):
        """Limpieza después de cada prueba"""
        # Eliminar directorio de pruebas y su contenido
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
    def test_folder_creation_from_template(self):
        """
        Test que simula el caso real de uso:
        1. Lee la plantilla Excel
        2. Crea las carpetas con los nombres normalizados
        3. Verifica que las carpetas se crearon correctamente
        """
        try:
            # Leer la plantilla Excel
            template_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                'data', 
                'test_cases.xlsx'
            )
            df = pd.read_excel(template_path)
            
            created_folders = []
            original_names = []
            
            # Procesar cada fila
            for _, row in df.iterrows():
                # Obtener y formatear los datos
                id_str = str(row['ID']) if pd.notna(row['ID']) else ""
                names_str = str(row['NOMBRES']) if pd.notna(row['NOMBRES']) else ""
                surnames_str = str(row['APELLIDOS']) if pd.notna(row['APELLIDOS']) else ""
                
                # Formar el nombre completo
                original_name = f"{id_str} - {names_str} {surnames_str}".strip()
                normalized_name = self.normalizer.normalize_text(original_name)
                
                if normalized_name != "- ":  # Ignorar entradas vacías
                    # Crear la carpeta
                    folder_path = os.path.join(self.test_dir, normalized_name)
                    os.makedirs(folder_path, exist_ok=True)
                    
                    created_folders.append(normalized_name)
                    original_names.append(original_name)
            
            # Imprimir resultados para verificación manual
            print("\nResultados de la creación de carpetas:")
            print("-" * 60)
            print("Original -> Normalizado")
            print("-" * 60)
            
            for original, normalized in zip(original_names, created_folders):
                print(f"{original} -> {normalized}")
                
                # Verificar que la carpeta existe
                folder_path = os.path.join(self.test_dir, normalized)
                self.assertTrue(os.path.exists(folder_path), 
                              f"La carpeta no se creó: {normalized}")
                self.assertTrue(os.path.isdir(folder_path), 
                              f"La ruta no es un directorio: {normalized}")
                
            print("-" * 60)
            print(f"Total de carpetas creadas: {len(created_folders)}")
            
            # Verificar que no hay carpetas duplicadas
            self.assertEqual(len(created_folders), len(set(created_folders)), 
                           "Se encontraron nombres de carpetas duplicados")
            
        except Exception as e:
            self.fail(f"Error en la prueba: {str(e)}")
            
    def test_basic_cases(self):
        """Prueba casos básicos de normalización"""
        cases = [
            ("123 - JUAN PEREZ", "123 - JUAN PEREZ"),
            ("- MARIA GARCIA", "- MARIA GARCIA")
        ]
        for input_text, expected in cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(self.normalizer.normalize_text(input_text), expected)
                
    def test_special_chars(self):
        """Prueba normalización de caracteres especiales"""
        cases = [
            ("1 - MARÍA JOSÉ", "1 - MARIA JOSE"),
            ("2 - JOSÉ ÁNGEL", "2 - JOSE ANGEL"),
            ("3 - PEÑA NIETO", "3 - PENA NIETO")
        ]
        for input_text, expected in cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(self.normalizer.normalize_text(input_text), expected)
                
    def test_special_ids(self):
        """Prueba IDs alfanuméricos y con guiones"""
        cases = [
            ("B-456 - ANA MARIA", "B-456 - ANA MARIA"),
            ("XYZ-789 - LUIS", "XYZ-789 - LUIS"),
            ("025656-MARIA-CLARA", "025656 - MARIA CLARA")
        ]
        for input_text, expected in cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(self.normalizer.normalize_text(input_text), expected)
                
    def test_edge_cases(self):
        """Prueba casos especiales y bordes"""
        cases = [
            ("", "- "),
            (None, "- "),
            ("456 - ", "456 - "),
            (" - ", "- "),
            ("---", "- ")
        ]
        for input_text, expected in cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(self.normalizer.normalize_text(input_text), expected)

if __name__ == '__main__':
    unittest.main()
