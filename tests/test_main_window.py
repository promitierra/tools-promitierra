"""
Unit tests for MainWindow folder creation functionality.
"""
import os
import tempfile
import pytest
import pandas as pd
from src.gui.main_window import MainWindow
from src.core.text_normalizer import TextNormalizer

@pytest.fixture
def main_window():
    """Create a MainWindow instance."""
    return MainWindow()

@pytest.fixture
def sample_excel():
    """Create a sample Excel file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        # Create test DataFrame
        df = pd.DataFrame({
            'ID': ['1', '2', '3'],
            'NOMBRES': ['Juan', 'María', 'Pedro'],
            'APELLIDOS': ['Pérez', 'García', 'López']
        })
        df.to_excel(tmp.name, index=False)
        yield tmp.name
        os.unlink(tmp.name)

@pytest.fixture
def invalid_excel():
    """Create an invalid Excel file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        # Create invalid DataFrame
        df = pd.DataFrame({
            'NOMBRE': ['Juan'],  # Incorrect column names
            'EDAD': [25]
        })
        df.to_excel(tmp.name, index=False)
        yield tmp.name
        os.unlink(tmp.name)

def test_load_template_with_valid_excel(main_window, sample_excel):
    """Test loading a valid Excel template."""
    with tempfile.TemporaryDirectory() as output_dir:
        # Simulate user interaction
        main_window.notebook.set_current_tab("Crear Carpetas")
        
        # Prepare mock methods
        details_text = []
        def mock_add_detail(text):
            details_text.append(text)
        main_window._add_folder_detail = mock_add_detail
        
        # Simulate loading template
        main_window._load_template()
        
        # Verify details were added
        assert len(details_text) > 0
        assert "Cargando plantilla" in details_text[0]

def test_normalize_folder_names(main_window):
    """Test folder name normalization."""
    normalizer = TextNormalizer()
    
    # Test cases
    test_cases = [
        ("José Luis", "JOSE LUIS"),
        ("María García", "MARIA GARCIA"),
        ("Año 2023", "ANO 2023"),
        ("Nombre con #caracteres especiales", "NOMBRE CON _CARACTERES ESPECIALES")
    ]
    
    for input_text, expected in test_cases:
        normalized = normalizer.normalize_text(input_text)
        assert normalized == expected

def test_folder_creation_from_excel(main_window, sample_excel):
    """Test creating folders from a valid Excel file."""
    with tempfile.TemporaryDirectory() as output_dir:
        # Simulate user interaction
        main_window.notebook.set_current_tab("Crear Carpetas")
        
        # Prepare mock methods
        details_text = []
        def mock_add_detail(text):
            details_text.append(text)
        main_window._add_folder_detail = mock_add_detail
        
        # Load Excel file
        df = pd.read_excel(sample_excel)
        
        # Manually trigger folder creation
        for _, row in df.iterrows():
            folder_name = main_window.text_normalizer.normalize_text(
                f"{row['ID']} - {row['NOMBRES']}"
            )
            
            if 'APELLIDOS' in df.columns and not pd.isna(row['APELLIDOS']):
                folder_name += f" {row['APELLIDOS']}"
            
            folder_path = os.path.join(output_dir, folder_name.upper())
            os.makedirs(folder_path, exist_ok=True)
        
        # Verify folders were created
        created_folders = os.listdir(output_dir)
        assert len(created_folders) == 3
        assert "1 - JUAN PEREZ" in created_folders
        assert "2 - MARIA GARCIA" in created_folders
        assert "3 - PEDRO LOPEZ" in created_folders

def test_handle_invalid_excel(main_window, invalid_excel):
    """Test handling of invalid Excel file."""
    with tempfile.TemporaryDirectory() as output_dir:
        # Simulate user interaction
        main_window.notebook.set_current_tab("Crear Carpetas")
        
        # Prepare mock methods for error handling
        error_messages = []
        def mock_show_error(title, message):
            error_messages.append(message)
        main_window.messagebox.showerror = mock_show_error
        
        # Try to load invalid Excel
        main_window._load_template()
        
        # Verify error was shown
        assert len(error_messages) > 0
        assert "columnas 'ID' y 'NOMBRES'" in error_messages[0]
