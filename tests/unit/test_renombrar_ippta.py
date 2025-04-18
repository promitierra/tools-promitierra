import os
import pytest
import tempfile
from pathlib import Path
import sys

# Agregar el directorio raíz del proyecto al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from scripts.renombrar_archivos_ippta import patron_renombrado
from src.utils.file_operations import FileRenamer
from src.utils.callbacks import RenameCallbacks


def test_patron_renombrado():
    """Prueba la función de patrón de renombrado"""
    
    # Caso 1: Archivo con ID que debe ser renombrado
    assert patron_renombrado("12345_documento.pdf") == "12345_IPPTA"
    
    # Caso 2: Archivo que ya tiene el formato correcto
    assert patron_renombrado("67890_IPPTA.pdf") == "67890_IPPTA.pdf"
    
    # Caso 3: Archivo sin ID
    assert patron_renombrado("documento_sin_id.pdf") == "documento_sin_id.pdf"
    
    # Caso 4: Archivo oculto
    assert patron_renombrado(".archivo_oculto") == ".archivo_oculto"


class TestRenombradoIPPTA:
    
    def setup_method(self):
        # Crear una estructura temporal para las pruebas
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_files = [
            "12345_documento.pdf",
            "67890_IPPTA.pdf",
            "documento_sin_id.pdf",
            "98765_con_espacios.pdf",
            ".archivo_oculto",
            "54321_IPPTA_duplicado.pdf"
        ]
        
        # Crear los archivos de prueba
        for filename in self.test_files:
            file_path = os.path.join(self.temp_dir.name, filename)
            with open(file_path, "w") as f:
                f.write(f"Contenido de prueba para {filename}")
        
        # Crear instancias de las clases necesarias
        self.renamer = FileRenamer()
        self.callbacks = RenameCallbacks()
        
        # Agregar el patrón de validación IPPTA
        self.renamer.add_validation_pattern('ippta', r'^\d+_IPPTA(?:\.[^.]+)?$')
    
    def teardown_method(self):
        # Limpiar archivos temporales
        self.temp_dir.cleanup()
    
    def test_preview_changes(self):
        """Prueba la vista previa de cambios"""
        
        # Obtener vista previa de cambios
        changes = self.renamer.preview_changes(self.temp_dir.name, patron_renombrado)
        
        # Verificar que se detectan los archivos que necesitan cambios
        assert len(changes) > 0
        
        # Verificar que los archivos que ya tienen el formato correcto no se incluyen
        assert not any(old.endswith("67890_IPPTA.pdf") for old, _ in changes)
        
        # Verificar que los archivos sin ID no se incluyen en los cambios
        assert not any(old.endswith("documento_sin_id.pdf") for old, _ in changes)
    
    def test_rename_batch_with_validation(self):
        """Prueba el renombrado por lotes con validación"""
        
        # Iniciar el proceso de renombrado
        self.callbacks.on_start_batch(len(self.test_files))
        
        # Crear un archivo que generará un error de validación
        invalid_file = os.path.join(self.temp_dir.name, "invalid_12345.pdf")
        with open(invalid_file, "w") as f:
            f.write("Archivo inválido")
        
        results = self.renamer.rename_files_batch(
            self.temp_dir.name,
            lambda x: "invalid_name" if "invalid" in x else patron_renombrado(x),
            recursive=True,
            keep_extension=True,
            callbacks=self.callbacks,
            validation_pattern='ippta'
        )
        
        # Verificar que se completó el proceso
        self.callbacks.on_batch_complete()
        summary = self.callbacks.get_summary()
        
        # Verificar que se renombraron los archivos correctos
        assert os.path.exists(os.path.join(self.temp_dir.name, "12345_IPPTA.pdf"))
        assert os.path.exists(os.path.join(self.temp_dir.name, "67890_IPPTA.pdf"))
        assert os.path.exists(os.path.join(self.temp_dir.name, "documento_sin_id.pdf"))
        
        # Verificar que se registraron los errores para nombres inválidos
        assert len(self.callbacks.errors) > 0
        assert any("invalid_name" in error[1] for error in self.callbacks.errors)
    
    def test_undo_operation(self):
        """Prueba la funcionalidad de deshacer cambios"""
        
        # Realizar algunos renombrados
        self.renamer.rename_files_batch(
            self.temp_dir.name,
            patron_renombrado,
            recursive=True,
            keep_extension=True
        )
        
        # Verificar que se realizaron los cambios
        assert os.path.exists(os.path.join(self.temp_dir.name, "12345_IPPTA.pdf"))
        
        # Deshacer los cambios
        success, _ = self.renamer.undo_last_operation()
        assert success is True
        
        # Verificar que se restauraron los nombres originales
        assert os.path.exists(os.path.join(self.temp_dir.name, "12345_documento.pdf"))
    
    def test_error_handling(self):
        """Prueba el manejo de errores"""
        
        # Caso 1: Carpeta inexistente
        results = self.renamer.rename_files_batch(
            os.path.join(self.temp_dir.name, "no_existe"),
            patron_renombrado
        )
        assert list(results.values())[0][0][0] is False
        
        # Caso 2: Archivo bloqueado
        blocked_file = os.path.join(self.temp_dir.name, "blocked_12345.pdf")
        with open(blocked_file, "w") as f:
            f.write("Archivo bloqueado")
            # Intentar renombrar mientras está abierto
            results = self.renamer.rename_file(blocked_file, "12345_IPPTA.pdf")
            assert results[0] is False 