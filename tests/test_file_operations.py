import os
import pytest
import tempfile
from pathlib import Path

from src.utils.file_operations import rename_file, rename_file_with_callback


class TestFileOperations:
    
    def setup_method(self):
        # Crear un archivo temporal para las pruebas
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file_path = os.path.join(self.temp_dir.name, "test_file.txt")
        
        # Crear el archivo de prueba
        with open(self.test_file_path, "w") as f:
            f.write("Contenido de prueba")
    
    def teardown_method(self):
        # Limpiar archivos temporales
        self.temp_dir.cleanup()
    
    def test_rename_file_success(self):
        # Probar renombrar archivo correctamente
        new_name = "archivo_renombrado.txt"
        success, message = rename_file(self.test_file_path, new_name)
        
        # Verificar que la operación fue exitosa
        assert success is True
        assert "correctamente" in message
        
        # Verificar que el archivo original ya no existe
        assert not os.path.exists(self.test_file_path)
        
        # Verificar que el nuevo archivo existe
        new_path = os.path.join(self.temp_dir.name, new_name)
        assert os.path.exists(new_path)
    
    def test_rename_file_keep_extension(self):
        # Probar renombrar archivo manteniendo la extensión
        new_name = "archivo_renombrado"
        success, message = rename_file(self.test_file_path, new_name, keep_extension=True)
        
        # Verificar que la operación fue exitosa
        assert success is True
        
        # Verificar que el nuevo archivo existe con la extensión correcta
        new_path = os.path.join(self.temp_dir.name, f"{new_name}.txt")
        assert os.path.exists(new_path)
    
    def test_rename_file_change_extension(self):
        # Probar renombrar archivo cambiando la extensión
        new_name = "archivo_renombrado.md"
        success, message = rename_file(self.test_file_path, new_name, keep_extension=False)
        
        # Verificar que la operación fue exitosa
        assert success is True
        
        # Verificar que el nuevo archivo existe con la nueva extensión
        new_path = os.path.join(self.temp_dir.name, new_name)
        assert os.path.exists(new_path)
    
    def test_rename_nonexistent_file(self):
        # Probar renombrar un archivo que no existe
        nonexistent_path = os.path.join(self.temp_dir.name, "no_existe.txt")
        success, message = rename_file(nonexistent_path, "nuevo_nombre.txt")
        
        # Verificar que la operación falló
        assert success is False
        assert "no existe" in message.lower()
    
    def test_rename_to_existing_file(self):
        # Crear un segundo archivo con el nombre de destino
        existing_file = os.path.join(self.temp_dir.name, "existing.txt")
        with open(existing_file, "w") as f:
            f.write("Este archivo ya existe")
        
        # Intentar renombrar el archivo de prueba con un nombre que ya existe
        success, message = rename_file(self.test_file_path, "existing.txt")
        
        # Verificar que la operación falló
        assert success is False
        assert "ya existe" in message.lower()
        
        # Verificar que ambos archivos siguen existiendo
        assert os.path.exists(self.test_file_path)
        assert os.path.exists(existing_file)
    
    def test_rename_file_with_callback(self):
        # Crear un objeto de callback para las pruebas
        class TestCallbacks:
            def __init__(self):
                self.renamed_files = []
                self.errors = []
                
            def on_file_renamed(self, old_name, new_name):
                self.renamed_files.append((old_name, new_name))
                
            def on_file_error(self, file_name, error):
                self.errors.append((file_name, error))
        
        callbacks = TestCallbacks()
        new_name = "renamed_with_callback.txt"
        
        # Probar renombrar con callbacks
        success, message = rename_file_with_callback(
            self.test_file_path, new_name, callbacks=callbacks
        )
        
        # Verificar que la operación fue exitosa
        assert success is True
        
        # Verificar que el callback fue llamado
        assert len(callbacks.renamed_files) == 1
        assert callbacks.renamed_files[0][0] == "test_file.txt"
        assert callbacks.renamed_files[0][1] == new_name
        assert len(callbacks.errors) == 0
    
    def test_rename_file_with_callback_error(self):
        # Crear un objeto de callback para las pruebas
        class TestCallbacks:
            def __init__(self):
                self.renamed_files = []
                self.errors = []
                
            def on_file_renamed(self, old_name, new_name):
                self.renamed_files.append((old_name, new_name))
                
            def on_file_error(self, file_name, error):
                self.errors.append((file_name, error))
        
        callbacks = TestCallbacks()
        nonexistent_path = os.path.join(self.temp_dir.name, "no_existe.txt")
        
        # Probar renombrar con callbacks un archivo que no existe
        success, message = rename_file_with_callback(
            nonexistent_path, "nuevo_nombre.txt", callbacks=callbacks
        )
        
        # Verificar que la operación falló
        assert success is False
        
        # Verificar que el callback de error fue llamado
        assert len(callbacks.renamed_files) == 0
        assert len(callbacks.errors) == 1
        assert callbacks.errors[0][0] == "no_existe.txt"