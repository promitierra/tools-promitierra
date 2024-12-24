"""
Main window module for the PDF converter application.
"""
import os
from pathlib import Path
from typing import Optional, Callable
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from ..core import ImageProcessor, PDFConverter
from .progress_dialog import ProgressDialog

class MainWindow(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.image_processor = ImageProcessor()
        self.pdf_converter = PDFConverter()
        self.progress_dialog: Optional[ProgressDialog] = None
        
        self._setup_window()
        self._create_widgets()
        
    def _setup_window(self):
        """Configure main window properties."""
        self.title("Imagen a PDF")
        self.geometry("600x400")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
    def _create_widgets(self):
        """Create and configure GUI widgets."""
        # Input frame
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        # Input directory selection
        self.input_var = tk.StringVar()
        input_entry = ctk.CTkEntry(
            input_frame,
            textvariable=self.input_var,
            placeholder_text="Selecciona carpeta de imágenes...",
            width=400
        )
        input_entry.grid(row=0, column=0, padx=5, pady=5)
        
        input_btn = ctk.CTkButton(
            input_frame,
            text="Buscar",
            command=self._select_input_directory
        )
        input_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Output frame
        output_frame = ctk.CTkFrame(self)
        output_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        # Output file selection
        self.output_var = tk.StringVar()
        output_entry = ctk.CTkEntry(
            output_frame,
            textvariable=self.output_var,
            placeholder_text="Selecciona archivo PDF de salida...",
            width=400
        )
        output_entry.grid(row=0, column=0, padx=5, pady=5)
        
        output_btn = ctk.CTkButton(
            output_frame,
            text="Guardar",
            command=self._select_output_file
        )
        output_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Options frame
        options_frame = ctk.CTkFrame(self)
        options_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        
        # Pattern filter
        pattern_label = ctk.CTkLabel(options_frame, text="Patrón de archivos:")
        pattern_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.pattern_var = tk.StringVar(value="*")
        pattern_entry = ctk.CTkEntry(
            options_frame,
            textvariable=self.pattern_var,
            width=200
        )
        pattern_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Convert button
        convert_btn = ctk.CTkButton(
            self,
            text="Convertir a PDF",
            command=self._start_conversion
        )
        convert_btn.grid(row=3, column=0, padx=10, pady=10)
        
    def _select_input_directory(self):
        """Open dialog to select input directory."""
        directory = filedialog.askdirectory(
            title="Seleccionar carpeta de imágenes"
        )
        if directory:
            self.input_var.set(directory)
            # Set default output name
            if not self.output_var.get():
                default_output = os.path.join(
                    directory,
                    f"{Path(directory).name}.pdf"
                )
                self.output_var.set(default_output)
                
    def _select_output_file(self):
        """Open dialog to select output PDF file."""
        filename = filedialog.asksaveasfilename(
            title="Guardar PDF como",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.output_var.set(filename)
            
    def _update_progress(self, current: int, total: int):
        """Update progress dialog."""
        if self.progress_dialog:
            self.progress_dialog.update_progress(current, total)
            
    def _start_conversion(self):
        """Start PDF conversion process."""
        input_dir = self.input_var.get()
        output_file = self.output_var.get()
        
        if not input_dir or not output_file:
            messagebox.showerror(
                "Error",
                "Por favor selecciona la carpeta de entrada y el archivo de salida"
            )
            return
            
        try:
            # Show progress dialog
            self.progress_dialog = ProgressDialog(self)
            self.progress_dialog.show()
            
            # Start conversion
            self.pdf_converter.convert_directory(
                input_dir,
                output_file,
                self.pattern_var.get(),
                self._update_progress
            )
            
            messagebox.showinfo(
                "Éxito",
                "Conversión completada exitosamente"
            )
            
        except Exception as e:
            if isinstance(e, InterruptedError):
                messagebox.showinfo(
                    "Cancelado",
                    "Conversión cancelada por el usuario"
                )
            else:
                messagebox.showerror(
                    "Error",
                    f"Error durante la conversión: {str(e)}"
                )
                
        finally:
            if self.progress_dialog:
                self.progress_dialog.hide()
                self.progress_dialog = None
