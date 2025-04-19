"""
Pruebas unitarias para el módulo ConfigManager.
"""
import unittest
import tempfile
import os

from src.utils.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Pruebas para la gestión de configuración de la aplicación."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        # Crear directorio temporal para pruebas
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "config_test.json")
    
    def test_default_config(self):
        """Probar que la configuración por defecto se carga correctamente."""
        config = ConfigManager(self.config_file)
        
        # Verificar secciones principales
        self.assertIn("performance", config.config)
        self.assertIn("ui", config.config)
        self.assertIn("paths", config.config)
        
        # Verificar valores específicos
        self.assertEqual(config.get("performance", "max_workers"), 4)
        self.assertEqual(config.get("ui", "theme"), "dark")
        self.assertEqual(config.get("pdf_converter", "compression_quality"), 85)
    
    def test_save_and_load(self):
        """Probar que la configuración se guarda y se carga correctamente."""
        # Crear y guardar configuración
        config = ConfigManager(self.config_file)
        config.set("ui", "theme", "light")
        config.set("performance", "max_workers", 8)
        self.assertTrue(config.save_config())
        
        # Verificar que el archivo se creó
        self.assertTrue(os.path.exists(self.config_file))
        
        # Cargar nueva instancia y verificar valores
        config2 = ConfigManager(self.config_file)
        self.assertEqual(config2.get("ui", "theme"), "light")
        self.assertEqual(config2.get("performance", "max_workers"), 8)
    
    def test_get_nonexistent(self):
        """Probar el valor por defecto para claves inexistentes."""
        config = ConfigManager(self.config_file)
        
        # Prueba con valor por defecto
        result = config.get("no_existe", "clave", "valor_default")
        self.assertEqual(result, "valor_default")
        
        # Prueba con None como valor por defecto
        self.assertIsNone(config.get("no_existe", "clave"))
    
    def test_reset_section(self):
        """Probar que se restablece correctamente una sección."""
        config = ConfigManager(self.config_file)
        
        # Modificar valores
        config.set("ui", "theme", "custom")
        config.set("ui", "font_size", 16)
        
        # Verificar cambios
        self.assertEqual(config.get("ui", "theme"), "custom")
        self.assertEqual(config.get("ui", "font_size"), 16)
        
        # Restablecer sección
        config.reset_section("ui")
        
        # Imprimir para debug
        print("\nDEBUG reset_section:")
        print(f"ui theme: {config.get('ui', 'theme')}")
        print(f"ui font_size: {config.get('ui', 'font_size')}")
        
        # Verificar valores por defecto
        self.assertEqual(config.get("ui", "theme"), "dark")
        self.assertEqual(config.get("ui", "font_size"), 12)
    
    def test_reset_all(self):
        """Probar restablecimiento a valores por defecto."""
        config = ConfigManager(self.config_file)
        
        # Modificar valores en varias secciones
        config.set("ui", "theme", "custom")
        config.set("performance", "max_workers", 16)
        config.set("pdf_converter", "create_zip", False)
        
        # Restablecer todo
        config.reset_all()
        
        # Imprimir para debug
        print("\nDEBUG reset_all:")
        print(f"ui theme: {config.get('ui', 'theme')}")
        print(f"performance max_workers: {config.get('performance', 'max_workers')}")
        print(f"pdf_converter create_zip: {config.get('pdf_converter', 'create_zip')}")
        
        # Verificar valores por defecto
        self.assertEqual(config.get("ui", "theme"), "dark")
        self.assertEqual(config.get("performance", "max_workers"), 4)
        self.assertTrue(config.get("pdf_converter", "create_zip"))
    
    def test_update_path(self):
        """Probar la actualización de rutas."""
        config = ConfigManager(self.config_file)
        
        # Establecer ruta
        test_path = "/ruta/de/prueba"
        config.update_path("last_input_dir", test_path)
        
        # Verificar actualización
        self.assertEqual(config.get("paths", "last_input_dir"), test_path)
    
    def test_memory_limit(self):
        """Probar la conversión de límite de memoria."""
        config = ConfigManager(self.config_file)
        
        # Establecer 512 MB
        config.set("performance", "memory_limit_mb", 512)
        
        # Verificar conversión a bytes
        self.assertEqual(config.get_memory_limit(), 512 * 1024 * 1024)
    
    def test_max_workers(self):
        """Probar la obtención del número máximo de workers."""
        config = ConfigManager(self.config_file)
        
        # Establecer un valor alto
        config.set("performance", "max_workers", 1000)
        
        # Verificar que se limita por el número de CPUs
        import multiprocessing
        self.assertEqual(config.get_max_workers(), multiprocessing.cpu_count())


if __name__ == "__main__":
    unittest.main() 