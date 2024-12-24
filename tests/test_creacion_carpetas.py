import unittest
import os
import shutil
import pandas as pd
from imagen_a_pdf import ImagenAPdfApp

class TestCreacionCarpetas(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.app = ImagenAPdfApp()
        self.directorio_pruebas = os.path.join(os.path.dirname(__file__), 'carpetas_prueba')
        
        # Crear directorio de pruebas si no existe
        if not os.path.exists(self.directorio_pruebas):
            os.makedirs(self.directorio_pruebas)
            
    def tearDown(self):
        """Limpieza después de cada prueba"""
        # Eliminar directorio de pruebas y su contenido
        if os.path.exists(self.directorio_pruebas):
            shutil.rmtree(self.directorio_pruebas)
            
    def test_creacion_carpetas_desde_plantilla(self):
        """
        Test que simula el caso real de uso:
        1. Lee la plantilla Excel
        2. Crea las carpetas con los nombres normalizados
        3. Verifica que las carpetas se crearon correctamente
        """
        try:
            # Leer la plantilla Excel
            ruta_plantilla = os.path.join(os.path.dirname(__file__), '..', 'Plantilla Nombres Carpetas.xlsx')
            df = pd.read_excel(ruta_plantilla)
            
            carpetas_creadas = []
            nombres_originales = []
            
            # Procesar cada fila
            for _, fila in df.iterrows():
                # Obtener y formatear los datos
                id_str = str(fila['ID']) if pd.notna(fila['ID']) else ""
                nombres_str = str(fila['NOMBRES']) if pd.notna(fila['NOMBRES']) else ""
                apellidos_str = str(fila['APELLIDOS']) if pd.notna(fila['APELLIDOS']) else ""
                
                # Formar el nombre completo
                nombre_original = f"{id_str} - {nombres_str} {apellidos_str}".strip()
                nombre_normalizado = self.app.normalizar_texto(nombre_original)
                
                if nombre_normalizado != "- ":  # Ignorar entradas vacías
                    # Crear la carpeta
                    ruta_carpeta = os.path.join(self.directorio_pruebas, nombre_normalizado)
                    os.makedirs(ruta_carpeta, exist_ok=True)
                    
                    carpetas_creadas.append(nombre_normalizado)
                    nombres_originales.append(nombre_original)
            
            # Imprimir resultados para verificación manual
            print("\nResultados de la creación de carpetas:")
            print("-" * 60)
            print("Original -> Normalizado")
            print("-" * 60)
            
            for original, normalizado in zip(nombres_originales, carpetas_creadas):
                print(f"{original} -> {normalizado}")
                
                # Verificar que la carpeta existe
                ruta_carpeta = os.path.join(self.directorio_pruebas, normalizado)
                self.assertTrue(os.path.exists(ruta_carpeta), 
                              f"La carpeta no se creó: {normalizado}")
                self.assertTrue(os.path.isdir(ruta_carpeta), 
                              f"La ruta no es un directorio: {normalizado}")
                
            print("-" * 60)
            print(f"Total de carpetas creadas: {len(carpetas_creadas)}")
            
            # Verificar que no hay carpetas duplicadas
            self.assertEqual(len(carpetas_creadas), len(set(carpetas_creadas)), 
                           "Se encontraron nombres de carpetas duplicados")
            
        except Exception as e:
            self.fail(f"Error en la prueba: {str(e)}")

if __name__ == '__main__':
    unittest.main()
