"""
Main application logic module.
"""
from typing import Optional, Dict, Any, Callable
import os
from pathlib import Path
import tempfile
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd

from .pdf_converter import PDFConverter
from .text_normalizer import TextNormalizer

class ImagenAPdfApp:
    """Main application class combining PDF conversion and folder creation."""
    
    def __init__(self):
        self.pdf_converter = PDFConverter()
        self.text_normalizer = TextNormalizer()
        self.procesando = False
        self._setup_gui()
        
    def _setup_gui(self):
        """Initialize GUI components."""
        self.ventana = ctk.CTk()
        self.ventana.title("Herramientas ProMITIERRA")
        self.ventana.geometry("800x600")
        
        # Create tabs
        self.tab_control = ctk.CTkTabview(self.ventana)
        self.tab_control.pack(expand=True, fill="both", padx=10, pady=5)
        
        # Main tab
        self.pestaña_principal = self.tab_control.add("Convertir Imágenes")
        self.crear_contenido_pestaña_principal()
        
        # Folders tab
        self.pestaña_carpetas = self.tab_control.add("Crear Carpetas")
        self.crear_contenido_pestaña_carpetas()
        
    def crear_contenido_pestaña_principal(self):
        """Create main tab content."""
        frame = ctk.CTkFrame(self.pestaña_principal)
        frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Directory selection
        self.btn_seleccionar = ctk.CTkButton(
            frame,
            text="Seleccionar Carpeta",
            command=self.seleccionar_carpeta
        )
        self.btn_seleccionar.pack(pady=10)
        
        # Compression options
        self.var_compresion = ctk.BooleanVar(value=False)
        self.check_compresion = ctk.CTkCheckBox(
            frame,
            text="Modo Comprimido",
            variable=self.var_compresion
        )
        self.check_compresion.pack(pady=5)
        
        # Pattern filter
        pattern_frame = ctk.CTkFrame(frame)
        pattern_frame.pack(pady=5, fill="x")
        
        ctk.CTkLabel(pattern_frame, text="Patrón:").pack(side="left", padx=5)
        self.entry_patron = ctk.CTkEntry(pattern_frame)
        self.entry_patron.pack(side="left", fill="x", expand=True, padx=5)
        self.entry_patron.insert(0, "*")
        
        # Details area
        self.detalles_text = ctk.CTkTextbox(frame, height=200)
        self.detalles_text.pack(pady=10, fill="both", expand=True)
        self.detalles_text.configure(state="disabled")
        
    def crear_contenido_pestaña_carpetas(self):
        """Create folders tab content."""
        frame = ctk.CTkFrame(self.pestaña_carpetas)
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
        
    def seleccionar_carpeta(self):
        """Handle folder selection and processing."""
        if self.procesando:
            self.pdf_converter.cancelar_proceso()
            self.btn_seleccionar.configure(text="Seleccionar Carpeta")
            return
            
        directorio = filedialog.askdirectory(
            title="Seleccionar carpeta con imágenes"
        )
        if directorio:
            self.procesar_carpeta(directorio)
            
    def procesar_carpeta(self, directorio: str):
        """Process all images in the directory."""
        try:
            self.procesando = True
            self.btn_seleccionar.configure(text="Cancelar")
            self.agregar_detalle(f"Procesando carpeta: {directorio}")
            
            # Prepare callbacks
            callbacks = {
                'on_progress': self.actualizar_progreso,
                'on_complete': self.proceso_completado,
                'on_error': self.manejar_error
            }
            
            # Start processing
            self.pdf_converter.procesar_carpeta(
                directorio,
                self.var_compresion.get(),
                callbacks,
                self.entry_patron.get()
            )
            
        except Exception as e:
            self.manejar_error(str(e))
            
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
                
            # Read Excel file
            df = pd.read_excel(ruta_excel)
            
            # Create folders
            for _, row in df.iterrows():
                nombre = self.text_normalizer.normalize_text(
                    f"{row.get('ID', '')} - {row.get('NOMBRE', '')}"
                )
                ruta_carpeta = os.path.join(directorio_salida, nombre)
                os.makedirs(ruta_carpeta, exist_ok=True)
                self.agregar_estado(f"Creada carpeta: {nombre}")
                
            messagebox.showinfo(
                "Éxito",
                "Carpetas creadas exitosamente"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al procesar plantilla: {str(e)}"
            )
            
    def actualizar_progreso(self, actual: int, total: int):
        """Update progress in details area."""
        self.agregar_detalle(f"Procesando archivo {actual} de {total}")
        
    def proceso_completado(self):
        """Handle process completion."""
        self.procesando = False
        self.btn_seleccionar.configure(text="Seleccionar Carpeta")
        self.agregar_detalle("Proceso completado exitosamente")
        
    def manejar_error(self, error: str):
        """Handle process errors."""
        self.procesando = False
        self.btn_seleccionar.configure(text="Seleccionar Carpeta")
        self.agregar_detalle(f"Error: {error}")
        
    def agregar_detalle(self, texto: str):
        """Add text to details area."""
        self.detalles_text.configure(state="normal")
        self.detalles_text.insert("end", texto + "\n")
        self.detalles_text.see("end")
        self.detalles_text.configure(state="disabled")
        
    def agregar_estado(self, texto: str):
        """Add text to status area."""
        self.estado_text.configure(state="normal")
        self.estado_text.insert("end", texto + "\n")
        self.estado_text.see("end")
        self.estado_text.configure(state="disabled")
        
    def iniciar(self):
        """Start the application."""
        self.ventana.mainloop()
