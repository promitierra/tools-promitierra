import unittest
import pandas as pd
from imagen_a_pdf import ImagenAPdfApp

class TestNormalizacionTexto(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.app = ImagenAPdfApp()
        
    def test_casos_basicos(self):
        """Prueba casos básicos de normalización"""
        casos = [
            ("123 - JUAN PEREZ", "123 - JUAN PEREZ"),
            ("- MARIA GARCIA", "- MARIA GARCIA")
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                self.assertEqual(self.app.normalizar_texto(entrada), esperado)
                
    def test_caracteres_especiales(self):
        """Prueba normalización de caracteres especiales"""
        casos = [
            ("1 - MARÍA JOSÉ", "1 - MARIA JOSE"),
            ("2 - JOSÉ ÁNGEL", "2 - JOSE ANGEL"),
            ("3 - PEÑA NIETO", "3 - PENA NIETO")
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                self.assertEqual(self.app.normalizar_texto(entrada), esperado)
                
    def test_ids_especiales(self):
        """Prueba IDs alfanuméricos y con guiones"""
        casos = [
            ("B-456 - ANA MARIA", "B-456 - ANA MARIA"),
            ("XYZ-789 - LUIS", "XYZ-789 - LUIS"),
            ("025656-MARIA-CLARA", "025656 - MARIA CLARA")
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                self.assertEqual(self.app.normalizar_texto(entrada), esperado)
                
    def test_casos_borde(self):
        """Prueba casos especiales y bordes"""
        casos = [
            ("", "- "),
            (None, "- "),
            ("456 - ", "456 - "),
            (" - ", "- "),
            ("---", "- ")
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                self.assertEqual(self.app.normalizar_texto(entrada), esperado)
                
    def test_espacios_multiples(self):
        """Prueba casos con múltiples espacios"""
        casos = [
            ("1  -  LUIS   FERNANDO", "1 - LUIS FERNANDO"),
            ("123456 --  JUAN  PABLO  PEREZ", "123456 - JUAN PABLO PEREZ"),
            ("  -  ANA  MARIA  ", "- ANA MARIA")
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                self.assertEqual(self.app.normalizar_texto(entrada), esperado)
                
    def test_desde_plantilla(self):
        """Prueba casos desde la plantilla Excel"""
        try:
            # Leer la plantilla
            df = pd.read_excel('../Plantilla Nombres Carpetas.xlsx')
            
            # Probar cada fila
            for _, fila in df.iterrows():
                id_str = str(fila['ID']) if pd.notna(fila['ID']) else ""
                nombres_str = str(fila['NOMBRES']) if pd.notna(fila['NOMBRES']) else ""
                apellidos_str = str(fila['APELLIDOS']) if pd.notna(fila['APELLIDOS']) else ""
                
                # Formar el nombre completo
                entrada = f"{id_str} - {nombres_str} {apellidos_str}".strip()
                resultado = self.app.normalizar_texto(entrada)
                
                # Verificar que el resultado mantiene el formato correcto
                if id_str:
                    self.assertTrue(resultado.startswith(id_str.replace(" ", "")))
                self.assertTrue(" - " in resultado)
                self.assertEqual(resultado, resultado.upper())
                
        except Exception as e:
            self.fail(f"Error al probar con la plantilla: {str(e)}")

if __name__ == '__main__':
    unittest.main()
