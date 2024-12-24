"""
Módulo unificado para creación de carpetas desde plantillas Excel.
"""
from typing import Tuple, Optional, Callable
import os
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox

from .text_normalizer import TextNormalizer

class FolderCreator:
    """Clase para crear carpetas desde plantillas Excel con validaciones robustas."""
    
    def __init__(self):
        """Inicializar el creador de carpetas."""
        self.text_normalizer = TextNormalizer()
        
    def crear_plantilla(self, ruta_plantilla: str) -> Tuple[bool, str]:
        """Crear una plantilla de Excel con columnas predefinidas.
        
        Args:
            ruta_plantilla: Ruta donde se guardará la plantilla
        
        Returns:
            Tupla con (éxito, mensaje)
        """
        try:
            # Crear DataFrame con columnas estándar
            df = pd.DataFrame(columns=['ID', 'NOMBRES', 'APELLIDOS'])
            
            # Guardar plantilla
            df.to_excel(ruta_plantilla, index=False)
            
            return True, f"Plantilla creada en {ruta_plantilla}"
        
        except Exception as e:
            return False, f"Error al crear plantilla: {str(e)}"
    
    def crear_contenido_pestaña(self, parent: ctk.CTkFrame):
        """Create tab content."""
        frame = ctk.CTkFrame(parent)
        frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Excel template selection
        self.btn_plantilla = ctk.CTkButton(
            frame,
            text="Cargar Plantilla Excel",
            command=self.cargar_plantilla
        )
        self.btn_plantilla.pack(pady=10)
        
        # Output directory selection
        self.btn_directorio = ctk.CTkButton(
            frame,
            text="Seleccionar Directorio de Salida",
            command=self.seleccionar_directorio_salida
        )
        self.btn_directorio.pack(pady=10)
        
        # Status area
        self.estado_text = ctk.CTkTextbox(frame, height=200)
        self.estado_text.pack(pady=10, fill="both", expand=True)
        self.estado_text.configure(state="disabled")
        
    def cargar_plantilla(self):
        """Load and process Excel template."""
        try:
            ruta_excel = filedialog.askopenfilename(
                title="Seleccionar plantilla Excel",
                filetypes=[("Excel files", "*.xlsx")]
            )
            if not ruta_excel:
                return
                
            directorio_salida = filedialog.askdirectory(
                title="Seleccionar directorio de salida"
            )
            if not directorio_salida:
                return
                
            # Procesar plantilla
            exito, mensaje = self.procesar_plantilla(ruta_excel, directorio_salida)
            if exito:
                messagebox.showinfo(
                    "Éxito",
                    mensaje
                )
            else:
                messagebox.showerror(
                    "Error",
                    mensaje
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al procesar plantilla: {str(e)}"
            )
            
    def seleccionar_directorio_salida(self):
        """Select output directory."""
        directorio = filedialog.askdirectory(
            title="Seleccionar directorio de salida"
        )
        if directorio:
            self.agregar_estado(f"Directorio seleccionado: {directorio}")
            
    def agregar_estado(self, texto: str):
        """Add text to status area."""
        self.estado_text.configure(state="normal")
        self.estado_text.insert("end", texto + "\n")
        self.estado_text.see("end")
        self.estado_text.configure(state="disabled")
        
    def procesar_plantilla(
        self, 
        ruta_excel: str, 
        directorio_salida: str, 
        callbacks: Optional[object] = None
    ) -> Tuple[bool, str]:
        """Procesar plantilla Excel y crear carpetas.
        
        Args:
            ruta_excel: Ruta al archivo Excel
            directorio_salida: Directorio donde se crearán las carpetas
            callbacks: Objeto con métodos de callback
        
        Returns:
            Tupla con (éxito, mensaje)
        """
        try:
            # Leer plantilla
            df = pd.read_excel(ruta_excel)
            
            # Validar columnas
            columnas_requeridas = ['ID', 'NOMBRES']
            for col in columnas_requeridas:
                if col not in df.columns:
                    raise ValueError(f"Columna '{col}' no encontrada en la plantilla")
            
            # Crear carpetas
            carpetas_creadas = 0
            carpetas_existentes = 0
            
            # Eliminar filas duplicadas
            df_unico = df.drop_duplicates(subset=['ID', 'NOMBRES'])
            
            for _, row in df.iterrows():  # Usar df original
                # Normalizar nombre
                nombre_base = f"{row['ID']} - {row['NOMBRES']}"
                
                # Agregar apellidos si existen
                if 'APELLIDOS' in df.columns and pd.notna(row.get('APELLIDOS', '')):
                    nombre_base += f" {row['APELLIDOS']}"
                
                # Normalizar nombre de carpeta
                nombre_carpeta = self.text_normalizer.normalize_text(nombre_base)
                ruta_carpeta = os.path.join(directorio_salida, nombre_carpeta)
                
                # Manejar carpetas existentes
                if os.path.exists(ruta_carpeta):
                    if hasattr(callbacks, 'on_folder_exists'):
                        callbacks.on_folder_exists(nombre_carpeta)
                    carpetas_existentes += 1
                    continue
                
                try:
                    # Crear carpeta
                    os.makedirs(ruta_carpeta, exist_ok=False)
                    carpetas_creadas += 1
                    
                    # Callback de carpeta creada
                    if hasattr(callbacks, 'on_folder_created'):
                        callbacks.on_folder_created(nombre_carpeta)
                
                except FileExistsError:
                    # Manejar carpetas existentes
                    if hasattr(callbacks, 'on_folder_exists'):
                        callbacks.on_folder_exists(nombre_carpeta)
                    carpetas_existentes += 1
                
                except PermissionError as e:
                    # Manejar errores de permisos
                    if hasattr(callbacks, 'on_folder_error'):
                        callbacks.on_folder_error(nombre_carpeta, str(e))
            
            # Mensaje de resumen
            mensaje = (
                f"Proceso completado. "
                f"Carpetas creadas: {carpetas_creadas}, "
                f"Carpetas existentes: {carpetas_existentes}"
            )
            
            return True, mensaje
        
        except Exception as e:
            # Manejar errores generales
            if hasattr(callbacks, 'on_folder_error'):
                callbacks.on_folder_error('', str(e))
            
            return False, str(e)
