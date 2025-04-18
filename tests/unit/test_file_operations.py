import os
import re
import pytest
import tempfile
from pathlib import Path

from src.utils.file_operations import FileRenamer
from src.utils.callbacks import RenameCallbacks


class TestFileRenamer:
    
    def setup_method(self):
        # Crear una estructura de carpetas y archivos temporales para las pruebas
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Crear estructura de carpetas
        self.subfolder1 = os.path.join(self.temp_dir.name, "subfolder1")
        self.subfolder2 = os.path.join(self.temp_dir.name, "subfolder2")
        os.makedirs(self.subfolder1, exist_ok=True)
        os.makedirs(self.subfolder2, exist_ok=True)
        
        # Crear archivos de prueba en la carpeta principal
        self.test_file1 = os.path.join(self.temp_dir.name, "test_file1.txt")
        self.test_file2 = os.path.join(self.temp_dir.name, "test_file2.txt")
        self.test_file3 = os.path.join(self.temp_dir.name, "already_correct.txt")
        
        # Crear archivos de prueba en las subcarpetas
        self.test_file_sub1 = os.path.join(self.subfolder1, "subfile1.txt")
        self.test_file_sub2 = os.path.join(self.subfolder2, "subfile2.txt")
        self.test_file_sub3 = os.path.join(self.subfolder2, "already_correct_sub.txt")
        
        # Escribir contenido en los archivos
        for file_path in [self.test_file1, self.test_file2, self.test_file3,
                         self.test_file_sub1, self.test_file_sub2, self.test_file_sub3]:
            with open(file_path, "w") as f:
                f.write(f"Contenido de prueba para {os.path.basename(file_path)}")
        
        # Inicializar el renombrador
        self.renamer = FileRenamer()
    
    def teardown_method(self):
        # Limpiar archivos temporales
        self.temp_dir.cleanup()
    
    def test_validate_filename(self):
        # Probar validación de nombres de archivo
        
        # Caso 1: Nombre válido alfanumérico
        assert self.renamer.validate_filename("test-file_123.txt")[0] is True
        
        # Caso 2: Nombre inválido con caracteres especiales
        assert self.renamer.validate_filename("test/file*.txt")[0] is False
        
        # Caso 3: Nombre válido solo letras
        assert self.renamer.validate_filename("TestFile.txt", "solo_letras")[0] is True
        
        # Caso 4: Nombre inválido para solo letras
        assert self.renamer.validate_filename("test123.txt", "solo_letras")[0] is False
        
        # Caso 5: Patrón de validación inexistente
        assert self.renamer.validate_filename("test.txt", "patron_inexistente")[0] is False
    
    def test_add_validation_pattern(self):
        # Probar agregar nuevos patrones de validación
        
        # Caso 1: Agregar patrón válido
        assert self.renamer.add_validation_pattern("custom", r"^[A-Z]+$") is True
        
        # Caso 2: Intentar agregar patrón que ya existe
        assert self.renamer.add_validation_pattern("alfanumerico", r"^[a-z]+$") is False
        
        # Caso 3: Intentar agregar patrón inválido
        assert self.renamer.add_validation_pattern("invalid", r"[") is False
    
    def test_preview_changes(self):
        # Probar vista previa de cambios
        
        def pattern_func(filename):
            return f"preview_{filename}"
        
        changes = self.renamer.preview_changes(self.temp_dir.name, pattern_func)
        
        # Verificar que se detectaron los cambios correctamente
        assert len(changes) > 0
        assert any(old.endswith("test_file1.txt") for old, _ in changes)
        assert all(new.startswith(os.path.join(os.path.dirname(old), "preview_"))
                  for old, new in changes)
    
    def test_rename_file(self):
        # Probar renombrado de archivo individual
        
        # Caso 1: Renombrado exitoso
        success, _ = self.renamer.rename_file(self.test_file1, "renamed_file.txt")
        assert success is True
        assert os.path.exists(os.path.join(self.temp_dir.name, "renamed_file.txt"))
        
        # Caso 2: Archivo no existe
        success, _ = self.renamer.rename_file(
            os.path.join(self.temp_dir.name, "nonexistent.txt"),
            "new_name.txt"
        )
        assert success is False
        
        # Caso 3: Nombre inválido
        success, _ = self.renamer.rename_file(self.test_file2, "invalid/name.txt")
        assert success is False
        
        # Caso 4: Mantener extensión
        success, _ = self.renamer.rename_file(self.test_file3, "new_name", keep_extension=True)
        assert success is True
        assert os.path.exists(os.path.join(self.temp_dir.name, "new_name.txt"))
    
    def test_rename_files_batch(self):
        # Probar renombrado por lotes
        
        def pattern_func(filename):
            if "already_correct" in filename:
                return filename
            return f"batch_{filename}"
        
        callbacks = RenameCallbacks()
        
        # Caso 1: Renombrado recursivo
        results = self.renamer.rename_files_batch(
            self.temp_dir.name,
            pattern_func,
            recursive=True,
            callbacks=callbacks
        )
        
        # Verificar resultados
        assert len(results) == 3  # carpeta principal + 2 subcarpetas
        assert os.path.exists(os.path.join(self.temp_dir.name, "batch_test_file1.txt"))
        assert os.path.exists(os.path.join(self.subfolder1, "batch_subfile1.txt"))
        
        # Caso 2: Solo carpeta principal
        results = self.renamer.rename_files_batch(
            self.temp_dir.name,
            pattern_func,
            recursive=False
        )
        
        assert len(results) == 1  # solo carpeta principal
        
        # Caso 3: Carpeta no existe
        results = self.renamer.rename_files_batch(
            os.path.join(self.temp_dir.name, "nonexistent"),
            pattern_func
        )
        assert list(results.values())[0][0][0] is False
    
    def test_undo_operation(self):
        # Probar deshacer operación
        
        # Realizar algunos renombrados
        self.renamer.rename_file(self.test_file1, "undo_test1.txt")
        self.renamer.rename_file(self.test_file2, "undo_test2.txt")
        
        # Verificar que los archivos fueron renombrados
        assert os.path.exists(os.path.join(self.temp_dir.name, "undo_test1.txt"))
        assert os.path.exists(os.path.join(self.temp_dir.name, "undo_test2.txt"))
        
        # Deshacer la operación
        success, _ = self.renamer.undo_last_operation()
        assert success is True
        
        # Verificar que los archivos volvieron a su nombre original
        assert os.path.exists(self.test_file1)
        assert os.path.exists(self.test_file2)
    
    def test_callbacks(self):
        # Probar sistema de callbacks
        
        callbacks = RenameCallbacks()
        
        def pattern_func(filename):
            return f"callback_{filename}"
        
        # Iniciar proceso por lotes
        callbacks.on_start_batch(3)
        
        # Ejecutar renombrado con callbacks
        self.renamer.rename_files_batch(
            self.temp_dir.name,
            pattern_func,
            recursive=False,
            callbacks=callbacks
        )
        
        # Verificar que los callbacks fueron llamados
        assert len(callbacks.renamed_files) > 0
        assert callbacks.processed_files > 0
        
        # Verificar resumen
        summary = callbacks.get_summary()
        assert summary['total_files'] == 3
        assert summary['renamed_files'] > 0
        assert 'success_rate' in summary