import unittest
import tkinter as tk
import os
import tempfile
from datetime import datetime
from src.utils.helpers import agregar_detalle, actualizar_progreso, generar_nombre_zip, validar_directorio

class TestHelpers(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.root = tk.Tk()
        self.text_widget = tk.Text(self.root)
        self.progress_bar = tk.ttk.Progressbar(self.root)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Limpieza después de cada prueba"""
        self.root.destroy()
        if os.path.exists(self.temp_dir):
            for root, dirs, files in os.walk(self.temp_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.temp_dir)

    def test_agregar_detalle(self):
        """Prueba la función de agregar detalles"""
        # Probar diferentes tipos de mensajes
        tipos = {
            "info": "ℹ️",
            "error": "❌",
            "success": "✅",
            "warning": "⚠️"
        }
        
        for tipo, prefijo in tipos.items():
            agregar_detalle(self.text_widget, f"Mensaje de {tipo}", tipo)
            contenido = self.text_widget.get("1.0", tk.END)
            self.assertIn(prefijo, contenido)
            self.assertIn(f"Mensaje de {tipo}", contenido)
            
        # Probar formato de timestamp
        agregar_detalle(self.text_widget, "Mensaje con timestamp")
        contenido = self.text_widget.get("1.0", tk.END)
        timestamp_format = r"\[\d{2}:\d{2}:\d{2}\]"
        self.assertRegex(contenido, timestamp_format)

    def test_actualizar_progreso(self):
        """Prueba la actualización de la barra de progreso"""
        valores = [0, 0.5, 1]
        for valor in valores:
            actualizar_progreso(self.progress_bar, valor)
            self.assertEqual(self.progress_bar["value"], valor * 100)

    def test_generar_nombre_zip(self):
        """Prueba la generación de nombres ZIP"""
        nombre = generar_nombre_zip()
        otro_nombre = generar_nombre_zip()
        
        # Verificar formato básico
        self.assertTrue(nombre.startswith("PDFs_"))
        self.assertTrue(nombre.endswith(".zip"))
        
        # Verificar que los nombres son únicos
        self.assertNotEqual(nombre, otro_nombre)

    def test_validar_directorio(self):
        """Prueba la validación de directorios"""
        # Directorio válido
        valido, mensaje = validar_directorio(self.temp_dir)
        self.assertTrue(valido)
        self.assertEqual(mensaje, "")
        
        # Directorio que no existe
        no_existe = os.path.join(self.temp_dir, "no_existe")
        valido, mensaje = validar_directorio(no_existe)
        self.assertFalse(valido)
        self.assertEqual(mensaje, "El directorio no existe")
        
        # Archivo en lugar de directorio
        archivo = os.path.join(self.temp_dir, "archivo.txt")
        with open(archivo, "w") as f:
            f.write("test")
        valido, mensaje = validar_directorio(archivo)
        self.assertFalse(valido)
        self.assertEqual(mensaje, "La ruta no es un directorio")
        
        # Prueba de permisos (solo en sistemas Unix)
        if os.name != 'nt':
            dir_restringido = os.path.join(self.temp_dir, "restringido")
            os.makedirs(dir_restringido)
            os.chmod(dir_restringido, 0o000)
            valido, mensaje = validar_directorio(dir_restringido)
            self.assertFalse(valido)
            self.assertEqual(mensaje, "No hay permisos suficientes en el directorio")
