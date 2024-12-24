"""
Main window module for the PDF converter application.
"""
import os
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox
import threading
import pandas as pd
from datetime import datetime

from ..core.image_processor import ImageProcessor
from ..core.text_normalizer import TextNormalizer

class MainWindow(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.image_processor = ImageProcessor()
        self.text_normalizer = TextNormalizer()
        self.procesando = False
        self.modo_comprimido = ctk.BooleanVar(value=False)
        self.directorio_salida = None
        
        self._setup_window()
        self._create_widgets()
        
    def _setup_window(self):
        """Configure main window properties."""
        self.title("Herramientas de Productividad")
        self.geometry("500x500")
        self.resizable(False, False)
        
        # Configure theme
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
    def _create_widgets(self):
        """Create and configure GUI widgets."""
        # Create tab view
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Add tabs in desired order
        self.tab_folders = self.notebook.add("Crear Carpetas")
        self.tab_convert = self.notebook.add("imagenes a PDFs")
        
        # Create tab contents
        self._create_folders_tab()
        self._create_convert_tab()
        
    def _create_folders_tab(self):
        """Create content for folders tab."""
        # Main frame with minimal padding
        frame = ctk.CTkFrame(self.tab_folders)
        frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Title
        titulo = ctk.CTkLabel(frame, text="Creación Masiva de Carpetas", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack(pady=5)

        # Description
        descripcion1 = ctk.CTkLabel(frame, 
            text="Descarga la plantilla Excel, completa los datos con ID, NOMBRES y APELLIDOS.",
            font=ctk.CTkFont(size=12),
            text_color="#CCCCCC"
        )
        descripcion1.pack(pady=2)

        descripcion2 = ctk.CTkLabel(frame, 
            text="Luego, carga el archivo para crear automáticamente las carpetas.",
            font=ctk.CTkFont(size=12),
            text_color="#CCCCCC"
        )
        descripcion2.pack(pady=(0,5))
        
        # First row frame (template and load)
        row1_frame = ctk.CTkFrame(frame)
        row1_frame.pack(fill="x", padx=10, pady=10)
        
        # Left column: Download template
        btn_download = ctk.CTkButton(
            row1_frame,
            text="📥 Descargar Plantilla",
            command=self._download_template
        )
        btn_download.pack(side="left", padx=5)
        
        # Right column: Load template
        btn_load = ctk.CTkButton(
            row1_frame,
            text="📤 Cargar Plantilla",
            command=self._load_template
        )
        btn_load.pack(side="right", padx=5)
        
        # Status label
        self.folders_status_label = ctk.CTkLabel(frame, 
            text="Estado: Esperando plantilla...",
            font=ctk.CTkFont(size=12)
        )
        self.folders_status_label.pack(pady=10)
        
        # Details area
        self.folders_details_text = ctk.CTkTextbox(frame, height=100)
        self.folders_details_text.pack(fill="x", padx=10, pady=(5,10))
        self.folders_details_text.configure(state="disabled")

        # Add footer
        self._create_footer(frame)
        
    def _create_convert_tab(self):
        """Create content for convert tab."""
        # Main frame with minimal padding
        frame = ctk.CTkFrame(self.tab_convert)
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Title
        titulo = ctk.CTkLabel(frame, text="Conversor de Imágenes a PDF", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack(pady=5)

        # Compress checkbox
        self.cb_compress = ctk.CTkCheckBox(
            frame,
            text="Generar archivos PDFs en un nuevo archivo ZIP",
            variable=self.modo_comprimido,
            onvalue=True,
            offvalue=False
        )
        self.cb_compress.pack(pady=10)

        # Select folder button
        self.btn_select = ctk.CTkButton(
            frame,
            text="📁 Seleccionar Carpeta de Imágenes",
            command=self._select_folder
        )
        self.btn_select.pack(pady=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(frame)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)

        # Progress label
        self.progress_label = ctk.CTkLabel(frame, text="0%")
        self.progress_label.pack(pady=5)

        # Status label
        self.status_label = ctk.CTkLabel(
            frame,
            text="Estado: Esperando selección de carpeta...",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)

        # Details area
        self.details_text = ctk.CTkTextbox(frame, height=75)
        self.details_text.pack(fill="x", padx=10, pady=(5,10))
        self.details_text.configure(state="disabled")

        # Add footer
        self._create_footer(frame)
        
    def _create_footer(self, parent_frame):
        """Create footer with credits."""
        # Internal frame for credits
        credits_internal = ctk.CTkFrame(parent_frame, fg_color="transparent")
        credits_internal.pack(side="bottom", fill="x", pady=(10, 3))

        # First line: Developer and year
        credits_line1 = ctk.CTkLabel(
            credits_internal,
            text="Desarrollado por: Luis Fernando Moreno Montoya | 2024",
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC"
        )
        credits_line1.pack(pady=(10, 3))
        
        # Second line: Special message (split for heart color)
        message_frame = ctk.CTkFrame(credits_internal, fg_color="transparent")
        message_frame.pack(pady=(3, 10))

        # First part of message
        part1 = ctk.CTkLabel(
            message_frame,
            text="Hecho con ",
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC"
        )
        part1.pack(side="left")

        # Red heart
        heart = ctk.CTkLabel(
            message_frame,
            text="♥",
            font=ctk.CTkFont(size=13),
            text_color="#FF0000"
        )
        heart.pack(side="left")
        
    def _download_template(self):
        """Handle template download."""
        try:
            # Create new workbook
            wb = pd.DataFrame(columns=['ID', 'NOMBRES', 'APELLIDOS'])
            
            # Save dialog
            filename = filedialog.asksaveasfilename(
                title="Guardar plantilla como",
                defaultextension=".xlsx",
                initialfile="Plantilla Nombres Carpetas.xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            
            if filename:
                # Save template
                wb.to_excel(filename, index=False)
                messagebox.showinfo(
                    "Éxito",
                    "Plantilla descargada exitosamente"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al descargar plantilla: {str(e)}"
            )
            
    def _load_template(self):
        """Handle template loading and folder creation."""
        try:
            # Select Excel file
            excel_path = filedialog.askopenfilename(
                title="Seleccionar plantilla Excel",
                filetypes=[("Excel files", "*.xlsx")]
            )
            
            if not excel_path:
                return
                
            # Select output directory
            output_dir = filedialog.askdirectory(
                title="Seleccionar directorio de salida"
            )
            
            if not output_dir:
                return
                
            # Update status
            self.folders_status_label.configure(text="Estado: Procesando...")
            self._add_folder_detail(f"Cargando plantilla: {excel_path}")
            
            # Read Excel file
            df = pd.read_excel(excel_path)
            
            # Validate required columns
            if 'ID' not in df.columns or 'NOMBRES' not in df.columns:
                messagebox.showerror(
                    "Error",
                    "La plantilla debe tener las columnas 'ID' y 'NOMBRES'"
                )
                self.folders_status_label.configure(text="Estado: Error")
                return
                
            # Create folders
            folders_created = 0
            self.folders_details_text.configure(state="normal")
            self.folders_details_text.delete("1.0", "end")
            
            for _, row in df.iterrows():
                # Normalize folder name
                folder_name = self.text_normalizer.normalize_text(
                    f"{row['ID']} - {row['NOMBRES']}"
                )
                
                if 'APELLIDOS' in df.columns and not pd.isna(row['APELLIDOS']):
                    folder_name += f" {row['APELLIDOS']}"
                    
                # Ensure the folder name is in uppercase
                folder_name = folder_name.upper()
                
                folder_path = os.path.join(output_dir, folder_name)
                
                # Create folder
                os.makedirs(folder_path, exist_ok=True)
                folders_created += 1
                
                # Update progress
                self._add_folder_detail(f"✓ Creada carpeta: {folder_name}")
                
            # Show success message
            self.folders_status_label.configure(text=f"Estado: {folders_created} carpetas creadas")
            messagebox.showinfo(
                "Éxito",
                f"Se han creado {folders_created} carpetas exitosamente"
            )
            
        except Exception as e:
            self.folders_status_label.configure(text="Estado: Error")
            messagebox.showerror(
                "Error",
                f"Error durante la creación de carpetas: {str(e)}"
            )
            
    def _select_folder(self):
        """Handle folder selection for image conversion."""
        if self.procesando:
            self.procesando = False
            self.btn_select.configure(text="📁 Seleccionar Carpeta de Imágenes")
            return
            
        directory = filedialog.askdirectory(
            title="Seleccionar carpeta con imágenes"
        )
        
        if directory:
            self._process_folder(directory)
            
    def _process_folder(self, directory: str):
        """Process all images in the directory."""
        try:
            self.procesando = True
            self.btn_select.configure(text="🛑 Cancelar Proceso")
            self._add_detail(f"Procesando carpeta: {directory}")
            
            # Get output file name
            if self.modo_comprimido.get():
                output_file = filedialog.asksaveasfilename(
                    title="Guardar ZIP como",
                    defaultextension=".zip",
                    filetypes=[("ZIP files", "*.zip")],
                    initialfile=os.path.basename(directory) + ".zip"
                )
            else:
                output_file = filedialog.asksaveasfilename(
                    title="Guardar PDF como",
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")],
                    initialfile=os.path.basename(directory) + ".pdf"
                )
                
            if not output_file:
                self.procesando = False
                self.btn_select.configure(text="📁 Seleccionar Carpeta de Imágenes")
                return
                
            # Start conversion in a thread
            thread = threading.Thread(
                target=self._convert_images,
                args=(directory, output_file)
            )
            thread.start()
            
        except Exception as e:
            self.procesando = False
            self.btn_select.configure(text="📁 Seleccionar Carpeta de Imágenes")
            messagebox.showerror(
                "Error",
                f"Error al procesar carpeta: {str(e)}"
            )
            
    def _convert_images(self, input_dir: str, output_file: str):
        """Convert images to PDF in a separate thread."""
        try:
            # Update progress callback
            def update_progress(current: int, total: int):
                progress = current / total
                self.progress_bar.set(progress)
                self.progress_label.configure(text=f"{int(progress * 100)}%")
                self._add_detail(f"Procesando archivo {current} de {total}")
                
            # Convert images
            self.image_processor.batch_convert_to_pdf(
                input_dir,
                output_file,
                "*",  # Pattern filter
                update_progress,
                self.modo_comprimido.get()
            )
            
            # Show success message
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
            self.procesando = False
            self.btn_select.configure(text="📁 Seleccionar Carpeta de Imágenes")
            
    def _add_detail(self, text: str):
        """Add text to details area."""
        self.details_text.configure(state="normal")
        self.details_text.insert("end", text + "\n")
        self.details_text.see("end")
        self.details_text.configure(state="disabled")
        
    def _add_folder_detail(self, text: str):
        """Add text to folders details area."""
        self.folders_details_text.configure(state="normal")
        self.folders_details_text.insert("end", text + "\n")
        self.folders_details_text.see("end")
        self.folders_details_text.configure(state="disabled")
        
    def run(self):
        """Start the application."""
        self.mainloop()
