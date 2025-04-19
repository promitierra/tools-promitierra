"""
Módulo para gestionar la configuración de la aplicación.
"""
import json
import copy
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """Clase para gestionar la configuración global de la aplicación.
    
    Permite leer/escribir configuraciones desde/hacia un archivo JSON.
    """
    
    # Valores por defecto
    DEFAULT_CONFIG = {
        "performance": {
            "max_workers": 4,       # Número máximo de workers
            "memory_limit_mb": 1024, # Límite de memoria en MB
            "use_gpu": False        # Usar aceleración GPU si está disponible
        },
        "ui": {
            "theme": "dark",        # Tema visual (dark/light/system)
            "font_size": 12,        # Tamaño de fuente
            "language": "es",       # Idioma (es/en)
            "show_tooltips": True   # Mostrar ayudas contextuales
        },
        "paths": {
            "last_input_dir": "",   # Último directorio de entrada usado
            "last_output_dir": "",  # Último directorio de salida usado
            "temp_dir": ""          # Directorio temporal personalizado
        },
        "pdf_converter": {
            "compression_quality": 85, # Calidad de compresión (0-100)
            "max_image_size": 3000,    # Tamaño máximo de imagen en píxeles
            "create_zip": True         # Crear ZIP por defecto
        },
        "folder_creator": {
            "normalize_names": True,  # Normalizar nombres (quitar acentos)
            "use_categories": True,   # Usar categorías para organizar carpetas
            "default_category": "SIN_CATEGORIA" # Categoría por defecto
        }
    }
    
    def __init__(self, config_file: str = None):
        """Inicializa el gestor de configuración.
        
        Args:
            config_file: Ruta al archivo de configuración. Si es None, se usa
                la ubicación por defecto en el directorio del usuario.
        """
        if config_file is None:
            # Usar directorio de usuario + .promitierra
            self.config_dir = Path.home() / ".promitierra"
            self.config_dir.mkdir(exist_ok=True)
            self.config_file = self.config_dir / "config.json"
        else:
            self.config_file = Path(config_file)
            self.config_dir = self.config_file.parent
            self.config_dir.mkdir(exist_ok=True)
        
        # Cargar configuración
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde el archivo.
        
        Returns:
            Diccionario con la configuración.
        """
        if not self.config_file.exists():
            # Si no existe el archivo, usar valores por defecto
            return copy.deepcopy(self.DEFAULT_CONFIG)
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Asegurar que todos los valores por defecto estén presentes
            self._ensure_defaults(config)
            return config
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
            # Si hay error, usar valores por defecto
            return copy.deepcopy(self.DEFAULT_CONFIG)
    
    def _ensure_defaults(self, config: Dict[str, Any]) -> None:
        """Asegura que todos los valores por defecto estén presentes.
        
        Args:
            config: Diccionario de configuración a verificar/completar.
        """
        for section, values in self.DEFAULT_CONFIG.items():
            if section not in config:
                config[section] = copy.deepcopy(values)
            else:
                for key, value in values.items():
                    if key not in config[section]:
                        config[section][key] = value
    
    def save_config(self) -> bool:
        """Guarda la configuración actual en el archivo.
        
        Returns:
            True si se guardó correctamente, False en caso contrario.
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
            return False
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Obtiene un valor de configuración.
        
        Args:
            section: Sección de configuración (ej: 'performance', 'ui')
            key: Clave del valor
            default: Valor por defecto si no existe
        
        Returns:
            Valor de configuración o default si no existe
        """
        try:
            return self.config[section][key]
        except KeyError:
            return default
    
    def set(self, section: str, key: str, value: Any) -> None:
        """Establece un valor de configuración.
        
        Args:
            section: Sección de configuración
            key: Clave del valor
            value: Nuevo valor
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
    
    def update_path(self, path_type: str, new_path: str) -> None:
        """Actualiza una ruta en la configuración de paths.
        
        Args:
            path_type: Tipo de ruta ('last_input_dir', 'last_output_dir', etc.)
            new_path: Nueva ruta
        """
        if path_type in self.config["paths"]:
            self.config["paths"][path_type] = new_path
    
    def reset_section(self, section: str) -> None:
        """Restablece una sección a sus valores por defecto.
        
        Args:
            section: Sección a restablecer
        """
        if section in self.DEFAULT_CONFIG:
            # Es importante crear una copia profunda para evitar referencias
            self.config[section] = copy.deepcopy(self.DEFAULT_CONFIG[section])
    
    def reset_all(self) -> None:
        """Restablece toda la configuración a valores por defecto."""
        # Es importante crear una copia profunda para evitar referencias
        self.config = copy.deepcopy(self.DEFAULT_CONFIG)
    
    def get_memory_limit(self) -> int:
        """Obtiene el límite de memoria en bytes.
        
        Returns:
            Límite de memoria en bytes
        """
        # Convertir MB a bytes
        return self.get('performance', 'memory_limit_mb', 1024) * 1024 * 1024
    
    def get_max_workers(self) -> int:
        """Obtiene el número máximo de workers para procesamiento.
        
        Returns:
            Número máximo de workers
        """
        import multiprocessing
        max_workers = self.get('performance', 'max_workers', 4)
        # Limitar por el número de CPUs disponibles
        return min(max_workers, multiprocessing.cpu_count()) 