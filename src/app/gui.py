"""
Módulo de interfaz gráfica para la aplicación.
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from datetime import datetime
from .pdf_converter import PDFConverter
from src.core.folder_creator import FolderCreator
from src.core.pdf_resizer import PDFResizer
from src.core.pdf_to_png_converter import PDFToPNGConverter
from ..utils.helpers import (
    agregar_detalle, 
    actualizar_progreso, 
    generar_nombre_zip,
    validar_directorio
)
import threading

class HelpModal(ctk.CTkToplevel):
    """Ventana modal para mostrar ayuda"""
    def __init__(self, parent, title, help_text):
        super().__init__(parent)
        
        # Configurar ventana modal
        self.title(title)
        self.geometry("600x400")
        self.resizable(False, False)
        
        # Hacer la ventana modal
        self.transient(parent)
        self.grab_set()
        
        # Centrar en la pantalla
        self.center_window()
        
        # Crear contenido
        self.create_widgets(help_text)
        
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self, help_text):
        """Crear los widgets de la ventana de ayuda"""
        # Frame principal con padding
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Área de texto con scroll
        text_frame = ctk.CTkFrame(main_frame)
        text_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Widget de texto
        help_text_widget = ctk.CTkTextbox(
            text_frame,
            wrap="word",
            font=ctk.CTkFont(size=12)
        )
        help_text_widget.pack(fill="both", expand=True)
        
        # Insertar contenido
        help_text_widget.insert("1.0", help_text)
        help_text_widget.configure(state="disabled")
        
        # Botón de cerrar
        btn_cerrar = ctk.CTkButton(
            main_frame,
            text="Cerrar",
            command=self.destroy
        )
        btn_cerrar.pack(pady=(0, 10))

class ImagenAPdfGUI:
    def __init__(self):
        """Inicializar la aplicación"""
        self.ventana = ctk.CTk()
        self.ventana.title("Herramientas ProMITIERRA")
        # Aumentar el tamaño de la ventana para dar más espacio
        self.ventana.geometry("700x750")
        self.ventana.resizable(False, False)
        
        # Variables
        self.modo_comprimido = ctk.BooleanVar(value=False)
        self.centrar_contenido = ctk.BooleanVar(value=False)
        self.procesando = False
        
        # Textos de ayuda para cada pestaña
        self.help_texts = {
            "crear_carpetas": """
# Ayuda - Crear Carpetas

Esta herramienta te permite crear una estructura de carpetas desde un archivo Excel.

## Pasos:
1. Haz clic en "Descargar Plantilla" para obtener el archivo Excel base
2. Llena la plantilla con los nombres de las carpetas que deseas crear
3. Guarda el archivo Excel
4. Haz clic en "Crear Carpetas" y selecciona el archivo Excel que llenaste
5. Selecciona la ubicación donde deseas crear las carpetas

## Formato de la Plantilla:
- Cada fila representa una carpeta a crear
- La columna A debe contener el nombre de la carpeta
- Puedes usar '/' para crear subcarpetas
""",
            "imagenes_pdf": """
# Ayuda - Convertir Imágenes a PDF

Esta herramienta convierte imágenes a archivos PDF.

## Características:
- Mantiene la estructura de carpetas original
- Opción para comprimir los PDFs en un archivo ZIP
- Soporta formatos: JPG, PNG, BMP

## Pasos:
1. (Opcional) Marca "Comprimir PDFs en ZIP" si deseas un archivo comprimido
2. Haz clic en "Seleccionar Carpeta"
3. Elige la carpeta que contiene las imágenes
4. Espera a que se complete el proceso
""",
            "redimensionar_pdf": """
# Ayuda - Redimensionar PDF

Esta herramienta ajusta PDFs al tamaño carta estándar (8.5" x 11").

## Características:
- Preserva la orientación original del contenido
- Opción para centrar el contenido en la página
- Mantiene la calidad del PDF original

## Pasos:
1. (Opcional) Marca "Centrar contenido en la página"
2. Haz clic en "Seleccionar PDF"
3. Elige el archivo PDF a redimensionar
4. Selecciona dónde guardar el PDF redimensionado
""",
            "pdf_png": """
# Ayuda - Convertir PDF a PNG

Esta herramienta convierte archivos PDF a imágenes PNG.

## Características:
- Convierte PDFs individuales o carpetas completas
- Mantiene la calidad de las imágenes
- Crea una imagen PNG por cada página del PDF

## Pasos:
Para un solo archivo:
1. Haz clic en "Seleccionar PDF"
2. Elige el archivo a convertir

Para una carpeta:
1. Haz clic en "Seleccionar Carpeta"
2. Elige la carpeta con los PDFs
3. Espera a que se procesen todos los archivos
"""
        }
        
        # Componentes
        self.pdf_converter = PDFConverter()
        self.folder_creator = FolderCreator()
        self.pdf_resizer = PDFResizer()
        self.pdf_to_png_converter = PDFToPNGConverter()
        
        # Crear interfaz
        self.crear_widgets()
    
    def mostrar_ayuda(self, tab_name):
        """Mostrar ventana de ayuda para la pestaña especificada"""
        if tab_name in self.help_texts:
            HelpModal(self.ventana, f"Ayuda - {tab_name}", self.help_texts[tab_name])

    def crear_tab_base(self, tab, titulo_texto, descripcion_texto="", help_key=""):
        """Método base para crear la estructura estándar de una pestaña
        
        Args:
            tab: Pestaña donde se crearán los elementos
            titulo_texto: Texto del título
            descripcion_texto: Texto de descripción (opcional)
            help_key: Clave para el texto de ayuda
        
        Returns:
            dict: Diccionario con los contenedores principales de la pestaña
        """
        # Contenedor principal con padding estándar
        contenedor = ctk.CTkFrame(tab, fg_color="transparent")
        contenedor.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        # Sección de título con botón de ayuda (10% del espacio)
        titulo_frame = ctk.CTkFrame(contenedor, fg_color="transparent", height=50)
        titulo_frame.pack(fill="x", pady=(10, 5))
        titulo_frame.pack_propagate(False)
        
        # Frame para título y botón de ayuda
        header_frame = ctk.CTkFrame(titulo_frame, fg_color="transparent")
        header_frame.pack(expand=True)
        
        titulo = ctk.CTkLabel(
            header_frame,
            text=titulo_texto,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(side="left", padx=(0, 10))
        
        if help_key:
            help_button = ctk.CTkButton(
                header_frame,
                text="?",
                width=30,
                height=30,
                command=lambda: self.mostrar_ayuda(help_key)
            )
            help_button.pack(side="left")
        
        # Sección de descripción (10% del espacio)
        if descripcion_texto:
            desc_frame = ctk.CTkFrame(contenedor, fg_color="transparent", height=50)
            desc_frame.pack(fill="x", pady=(0, 10))
            desc_frame.pack_propagate(False)
            
            descripcion = ctk.CTkLabel(
                desc_frame,
                text=descripcion_texto,
                font=ctk.CTkFont(size=14),
                wraplength=700
            )
            descripcion.pack(expand=True)
        
        # Frame para controles (15% del espacio)
        controles_frame = ctk.CTkFrame(contenedor, fg_color="transparent", height=75)
        controles_frame.pack(fill="x", pady=(0, 10))
        controles_frame.pack_propagate(False)
        
        # Frame para la barra de progreso y estado (30% del espacio)
        progreso_frame = ctk.CTkFrame(contenedor, fg_color="transparent", height=150)
        progreso_frame.pack(fill="x", pady=(0, 10))
        progreso_frame.pack_propagate(False)
        
        # Barra de progreso
        barra_progreso = ctk.CTkProgressBar(progreso_frame)
        barra_progreso.pack(fill="x", pady=(20, 10), padx=20)
        barra_progreso.set(0)
        
        # Estado
        estado = ctk.CTkLabel(
            progreso_frame,
            text="Esperando acción...",
            font=ctk.CTkFont(size=13)
        )
        estado.pack(pady=(0, 20))
        
        # Área de detalles (40% del espacio restante)
        detalles = ctk.CTkTextbox(
            contenedor,
            height=200
        )
        detalles.pack(fill="both", expand=True)
        
        return {
            "contenedor": contenedor,
            "controles_frame": controles_frame,
            "barra_progreso": barra_progreso,
            "estado": estado,
            "detalles": detalles
        }

    def crear_widgets(self):
        # Preparar la estructura para agregar pestañas
        self.notebook = ctk.CTkTabview(self.ventana)
        self.notebook.pack(pady=(20, 5), padx=20, fill="both", expand=True)
        
        # Pestañas
        self.tab_crear_carpetas = self.notebook.add("Crear Carpetas")
        self.tab_imagenes_a_pdf = self.notebook.add("Imágenes a PDFs")
        self.tab_redimensionar_pdf = self.notebook.add("Redimensionar PDF")
        self.tab_pdf_a_png = self.notebook.add("PDF a PNG")
        
        # Crear contenido
        self.crear_contenido_tab_carpetas()
        self.crear_contenido_tab_imagenes()
        self.crear_contenido_tab_redimensionar()
        self.crear_contenido_tab_pdf_a_png()
        
        # Crear footer global
        self.footer = self.crear_footer(self.ventana)
        self.footer.pack(side="bottom", fill="x", pady=(0, 10), padx=20)

    def crear_contenido_tab_carpetas(self):
        """Crear el contenido de la pestaña de creación de carpetas"""
        elementos = self.crear_tab_base(
            self.tab_crear_carpetas,
            "Crear Carpetas desde Excel",
            "1. Descarga la plantilla Excel\n2. Llena los datos y guarda el archivo",
            "crear_carpetas"
        )
        
        # Botones
        btn_plantilla = ctk.CTkButton(
            elementos["controles_frame"],
            text="Descargar Plantilla",
            command=self.descargar_plantilla
        )
        btn_plantilla.pack(side="left", padx=5, expand=True)

        btn_crear = ctk.CTkButton(
            elementos["controles_frame"],
            text="Crear Carpetas",
            command=self.crear_carpetas
        )
        btn_crear.pack(side="left", padx=5, expand=True)

        # Guardar referencias
        self.detalles_carpetas = elementos["detalles"]

    def crear_contenido_tab_imagenes(self):
        """Crear el contenido de la pestaña de imágenes a PDF"""
        elementos = self.crear_tab_base(
            self.tab_imagenes_a_pdf,
            "Convertir Imágenes a PDF",
            "Convierte imágenes a PDF manteniendo la estructura de carpetas",
            "imagenes_pdf"
        )

        # Checkbox para modo comprimido
        self.check_comprimir = ctk.CTkCheckBox(
            elementos["controles_frame"],
            text="Comprimir PDFs en ZIP",
            variable=self.modo_comprimido
        )
        self.check_comprimir.pack(side="left", padx=10)

        # Botón para seleccionar carpeta
        self.btn_seleccionar = ctk.CTkButton(
            elementos["controles_frame"],
            text="Seleccionar Carpeta",
            command=self.seleccionar_carpeta
        )
        self.btn_seleccionar.pack(side="right", padx=10)

        # Guardar referencias
        self.barra_progreso = elementos["barra_progreso"]
        self.lbl_estado = elementos["estado"]
        self.detalles = elementos["detalles"]

    def crear_contenido_tab_redimensionar(self):
        """Crear el contenido de la pestaña de redimensionamiento de PDF"""
        elementos = self.crear_tab_base(
            self.tab_redimensionar_pdf,
            "Redimensionar PDF a Tamaño Carta",
            "Redimensiona un PDF al tamaño carta, preservando la orientación",
            "redimensionar_pdf"
        )
        
        # Checkbox para centrar contenido
        self.check_centrar = ctk.CTkCheckBox(
            elementos["controles_frame"],
            text="Centrar contenido en la página",
            variable=self.centrar_contenido
        )
        self.check_centrar.pack(side="left", padx=10, pady=10)
        
        # Botón para seleccionar archivo PDF
        self.btn_seleccionar_pdf = ctk.CTkButton(
            elementos["controles_frame"],
            text="Seleccionar PDF",
            command=self.seleccionar_pdf_para_redimensionar
        )
        self.btn_seleccionar_pdf.pack(side="right", padx=10)
        
        # Guardar referencias
        self.barra_progreso_resize = elementos["barra_progreso"]
        self.lbl_estado_resize = elementos["estado"]
        self.detalles_resize = elementos["detalles"]

    def crear_contenido_tab_pdf_a_png(self):
        """Crear el contenido de la pestaña de conversión de PDF a PNG"""
        elementos = self.crear_tab_base(
            self.tab_pdf_a_png,
            "Convertir PDF a PNG",
            "Extrae imágenes de archivos PDF y las guarda como PNG",
            "pdf_png"
        )
        
        # Botones
        self.btn_seleccionar_pdf_png = ctk.CTkButton(
            elementos["controles_frame"],
            text="Seleccionar PDF",
            command=self.seleccionar_pdf_para_png
        )
        self.btn_seleccionar_pdf_png.pack(side="left", padx=5, expand=True)
        
        self.btn_seleccionar_carpeta_png = ctk.CTkButton(
            elementos["controles_frame"],
            text="Seleccionar Carpeta",
            command=self.seleccionar_carpeta_para_png
        )
        self.btn_seleccionar_carpeta_png.pack(side="left", padx=5, expand=True)
        
        # Guardar referencias
        self.barra_progreso_png = elementos["barra_progreso"]
        self.lbl_estado_png = elementos["estado"]
        self.detalles_png = elementos["detalles"]

    def crear_footer(self, frame_padre):
        """Crear el pie de página con créditos"""
        creditos_interno = ctk.CTkFrame(frame_padre, fg_color="transparent")

        creditos_linea1 = ctk.CTkLabel(
            creditos_interno,
            text="Desarrollado por: Luis Fernando Moreno Montoya | 2025",
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC"
        )
        creditos_linea1.pack(pady=(10, 3))
        
        mensaje_frame = ctk.CTkFrame(creditos_interno, fg_color="transparent")
        mensaje_frame.pack(pady=(3, 10))

        parte1 = ctk.CTkLabel(
            mensaje_frame,
            text="Hecho con ",
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC"
        )
        parte1.pack(side="left")

        # Usar el corazón en formato Unicode
        corazon = ctk.CTkLabel(
            mensaje_frame,
            text="\u2764",  # Código Unicode para corazón
            font=ctk.CTkFont(size=14),
            text_color="#FF0000"
        )
        corazon.pack(side="left")

        parte2 = ctk.CTkLabel(
            mensaje_frame,
            text=" por la productividad laboral y el cuidado del tiempo",
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC"
        )
        parte2.pack(side="left")
        
        return creditos_interno

    def descargar_plantilla(self):
        """Descargar plantilla Excel"""
        try:
            ruta = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Guardar plantilla Excel"
            )
            if ruta:
                exito, mensaje = self.folder_creator.crear_plantilla(ruta)
                if exito:
                    agregar_detalle(self.detalles_carpetas, mensaje, "success")
                    messagebox.showinfo("Éxito", mensaje)
                else:
                    agregar_detalle(self.detalles_carpetas, mensaje, "error")
                    messagebox.showerror("Error", mensaje)
        except Exception as e:
            agregar_detalle(self.detalles_carpetas, f"Error: {str(e)}", "error")
            messagebox.showerror("Error", str(e))

    def crear_carpetas(self):
        """Crear carpetas desde plantilla Excel"""
        # Seleccionar archivo Excel
        ruta_excel = filedialog.askopenfilename(
            title="Seleccionar Plantilla Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )
        
        if not ruta_excel:
            return
        
        # Seleccionar directorio de salida
        directorio_salida = filedialog.askdirectory(
            title="Seleccionar Directorio de Salida"
        )
        
        if not directorio_salida:
            return
        
        # Clase de callbacks personalizada
        class FolderCreationCallbacks:
            def __init__(self, gui):
                self.gui = gui
                self.detalles_carpetas = []
            
            def on_folder_created(self, nombre_carpeta):
                detalle = f"Carpeta creada: {nombre_carpeta}"
                self.detalles_carpetas.append(detalle)
                agregar_detalle(self.gui.detalles_carpetas, detalle, "success")
            
            def on_folder_exists(self, nombre_carpeta):
                detalle = f"Carpeta ya existente: {nombre_carpeta}"
                self.detalles_carpetas.append(detalle)
                agregar_detalle(self.gui.detalles_carpetas, detalle, "warning")
            
            def on_folder_error(self, nombre_carpeta, error):
                detalle = f"Error al crear carpeta {nombre_carpeta}: {error}"
                self.detalles_carpetas.append(detalle)
                agregar_detalle(self.gui.detalles_carpetas, detalle, "error")
        
        # Crear callbacks
        callbacks = FolderCreationCallbacks(self)
        
        # Procesar plantilla
        try:
            exito, mensaje = self.folder_creator.procesar_plantilla(
                ruta_excel, 
                directorio_salida,
                callbacks
            )
            
            # Mostrar mensaje de resultado
            if exito:
                messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showerror("Error", mensaje)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def seleccionar_carpeta(self):
        """Seleccionar carpeta para procesar imágenes"""
        if self.procesando:
            messagebox.showwarning(
                "Procesando", 
                "Ya hay un proceso en ejecución. Por favor espere."
            )
            return
            
        directorio = filedialog.askdirectory(
            title="Seleccionar carpeta con imágenes"
        )
        
        if not directorio:
            return
            
        valido, mensaje = validar_directorio(directorio)
        if not valido:
            messagebox.showerror("Error", mensaje)
            return
            
        self.procesando = True
        self.btn_seleccionar.configure(state="disabled")
        self.barra_progreso.set(0)
        self.lbl_estado.configure(text="Procesando imágenes...")
        self.detalles.delete("1.0", "end")
        
        class Callbacks:
            def __init__(self, gui):
                self.gui = gui
                self.started = False
                self.files_found = 0
                self.converted = []
                self.errors = []
                
            def on_start(self):
                """Llamado cuando inicia el proceso"""
                self.started = True
                self.gui.lbl_estado.configure(text="Iniciando proceso...")
                agregar_detalle(
                    self.gui.detalles,
                    "Iniciando proceso de conversión..."
                )
                
            def on_images_found(self, total):
                self.files_found = total
                agregar_detalle(
                    self.gui.detalles,
                    f"Se encontraron {total} imágenes"
                )
                
            def on_no_images(self):
                agregar_detalle(
                    self.gui.detalles,
                    "No se encontraron imágenes en la carpeta",
                    "warning"
                )
                self.gui.btn_seleccionar.configure(state="normal")
                self.gui.procesando = False
                
            def on_file_converted(self, nombre):
                self.converted.append(nombre)
                actualizar_progreso(
                    self.gui.barra_progreso,
                    len(self.converted) / self.files_found if self.files_found > 0 else 0
                )
                agregar_detalle(
                    self.gui.detalles,
                    f"Convertido: {nombre}"
                )
                
            def on_file_error(self, nombre, error):
                """Llamado cuando hay un error al convertir un archivo"""
                self.errors.append(error)
                agregar_detalle(
                    self.gui.detalles,
                    f"Error al convertir {nombre}: {error}",
                    "error"
                )
                
            def on_error(self, error):
                self.errors.append(error)
                agregar_detalle(
                    self.gui.detalles,
                    f"Error: {error}",
                    "error"
                )
                
            def on_progress(self, valor):
                actualizar_progreso(self.gui.barra_progreso, valor)
                
            def on_creating_zip(self):
                """Llamado cuando se está creando el archivo ZIP"""
                self.gui.lbl_estado.configure(text="Creando archivo ZIP...")
                agregar_detalle(
                    self.gui.detalles,
                    "Creando archivo ZIP con los PDFs..."
                )
                
            def on_complete(self, convertidas, total, errores, modo_comprimido):
                """Llamado cuando se completa todo el proceso"""
                mensaje = f"Proceso completado. Convertidas {convertidas} de {total} imágenes"
                if errores > 0:
                    mensaje += f" ({errores} errores)"
                self.gui.lbl_estado.configure(text=mensaje)
                agregar_detalle(
                    self.gui.detalles,
                    mensaje,
                    "success"
                )
                
            def on_finish(self):
                self.gui.btn_seleccionar.configure(state="normal")
                self.gui.procesando = False
                
            def on_zip_created(self, ruta):
                agregar_detalle(
                    self.gui.detalles,
                    f"\nArchivo ZIP creado: {ruta}",
                    "success"
                )
        
        callbacks = Callbacks(self)
        
        # Iniciar conversión en un hilo separado
        threading.Thread(
            target=self.pdf_converter.procesar_carpeta,
            args=(directorio, self.modo_comprimido.get(), callbacks)
        ).start()
    
    def seleccionar_pdf_para_redimensionar(self):
        """Seleccionar archivo PDF para redimensionar"""
        if self.procesando:
            messagebox.showwarning(
                "Procesando", 
                "Ya hay un proceso en ejecución. Por favor espere."
            )
            return
            
        # Seleccionar archivo PDF
        input_pdf = filedialog.askopenfilename(
            title="Seleccionar archivo PDF",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        
        if not input_pdf:
            return
        
        # Solicitar nombre del archivo de salida
        nombre_base = os.path.splitext(input_pdf)[0]
        output_pdf_default = f"{nombre_base}_letter.pdf"
        output_pdf_input = filedialog.asksaveasfilename(
            title="Guardar PDF redimensionado",
            initialfile=os.path.basename(output_pdf_default),
            filetypes=[("Archivos PDF", "*.pdf")],
            defaultextension=".pdf"
        )
        
        if not output_pdf_input:
            return
            
        self.procesando = True
        self.btn_seleccionar_pdf.configure(state="disabled")
        self.barra_progreso_resize.set(0)
        self.lbl_estado_resize.configure(text="Redimensionando PDF...")
        self.detalles_resize.delete("1.0", "end")
        
        # Iniciar redimensionamiento en un hilo separado
        threading.Thread(
            target=self.redimensionar_pdf,
            args=(input_pdf, output_pdf_input, self.centrar_contenido.get())
        ).start()
    
    def redimensionar_pdf(self, input_pdf, output_pdf, centrar):
        """Redimensionar PDF a tamaño carta"""
        try:
            agregar_detalle(
                self.detalles_resize,
                f"Redimensionando: {os.path.basename(input_pdf)}"
            )
            
            # Actualizar progreso
            self.barra_progreso_resize.set(0.2)
            
            # Redimensionar PDF
            resultado = self.pdf_resizer.resize_pdf(input_pdf, output_pdf, centrar)
            
            # Actualizar progreso
            self.barra_progreso_resize.set(1.0)
            
            if resultado:
                mensaje = f"PDF redimensionado exitosamente: {os.path.basename(output_pdf)}"
                self.lbl_estado_resize.configure(text=mensaje)
                agregar_detalle(self.detalles_resize, mensaje, "success")
                messagebox.showinfo("Éxito", mensaje)
            else:
                mensaje = "Error al redimensionar el PDF"
                self.lbl_estado_resize.configure(text=mensaje)
                agregar_detalle(self.detalles_resize, mensaje, "error")
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            mensaje = f"Error: {str(e)}"
            self.lbl_estado_resize.configure(text="Error en el proceso")
            agregar_detalle(self.detalles_resize, mensaje, "error")
            messagebox.showerror("Error", mensaje)
        finally:
            self.btn_seleccionar_pdf.configure(state="normal")
            self.procesando = False
    
    def seleccionar_pdf_para_png(self):
        """Seleccionar archivo PDF para convertir a PNG"""
        if self.procesando:
            messagebox.showwarning(
                "Procesando", 
                "Ya hay un proceso en ejecución. Por favor espere."
            )
            return
            
        # Seleccionar archivo PDF
        input_pdf = filedialog.askopenfilename(
            title="Seleccionar archivo PDF",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        
        if not input_pdf:
            return
            
        self.procesando = True
        self.btn_seleccionar_pdf_png.configure(state="disabled")
        self.btn_seleccionar_carpeta_png.configure(state="disabled")
        self.barra_progreso_png.set(0)
        self.lbl_estado_png.configure(text="Convirtiendo PDF a PNG...")
        self.detalles_png.delete("1.0", "end")
        
        # Iniciar conversión en un hilo separado
        threading.Thread(
            target=self.convertir_pdf_a_png,
            args=(input_pdf,)
        ).start()
    
    def seleccionar_carpeta_para_png(self):
        """Seleccionar carpeta con PDFs para convertir a PNG"""
        if self.procesando:
            messagebox.showwarning(
                "Procesando", 
                "Ya hay un proceso en ejecución. Por favor espere."
            )
            return
            
        # Seleccionar carpeta
        directorio = filedialog.askdirectory(
            title="Seleccionar carpeta con archivos PDF"
        )
        
        if not directorio:
            return
            
        valido, mensaje = validar_directorio(directorio)
        if not valido:
            messagebox.showerror("Error", mensaje)
            return
            
        self.procesando = True
        self.btn_seleccionar_pdf_png.configure(state="disabled")
        self.btn_seleccionar_carpeta_png.configure(state="disabled")
        self.barra_progreso_png.set(0)
        self.lbl_estado_png.configure(text="Buscando archivos PDF...")
        self.detalles_png.delete("1.0", "end")
        
        # Iniciar conversión en un hilo separado
        threading.Thread(
            target=self.convertir_carpeta_pdf_a_png,
            args=(directorio,)
        ).start()
    
    def convertir_pdf_a_png(self, pdf_path):
        """Convertir un archivo PDF a PNG"""
        try:
            agregar_detalle(
                self.detalles_png,
                f"Convirtiendo: {os.path.basename(pdf_path)}"
            )
            
            # Actualizar progreso
            self.barra_progreso_png.set(0.2)
            
            # Convertir PDF a PNG
            resultado = self.pdf_to_png_converter.convert_pdf_to_png(pdf_path)
            
            # Actualizar progreso
            self.barra_progreso_png.set(1.0)
            
            if resultado:
                mensaje = f"PDF convertido exitosamente: {os.path.basename(pdf_path)}"
                self.lbl_estado_png.configure(text=mensaje)
                agregar_detalle(self.detalles_png, mensaje, "success")
                messagebox.showinfo("Éxito", mensaje)
            else:
                mensaje = "Error al convertir el PDF"
                self.lbl_estado_png.configure(text=mensaje)
                agregar_detalle(self.detalles_png, mensaje, "error")
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            mensaje = f"Error: {str(e)}"
            self.lbl_estado_png.configure(text="Error en el proceso")
            agregar_detalle(self.detalles_png, mensaje, "error")
            messagebox.showerror("Error", mensaje)
        finally:
            self.btn_seleccionar_pdf_png.configure(state="normal")
            self.btn_seleccionar_carpeta_png.configure(state="normal")
            self.procesando = False
    
    def convertir_carpeta_pdf_a_png(self, directorio):
        """Convertir todos los PDFs de una carpeta a PNG"""
        try:
            # Buscar archivos PDF
            pdf_files = self.pdf_to_png_converter.find_pdf_files(directorio)
            total_files = len(pdf_files)
            
            if total_files == 0:
                mensaje = "No se encontraron archivos PDF en la carpeta"
                self.lbl_estado_png.configure(text=mensaje)
                agregar_detalle(self.detalles_png, mensaje, "warning")
                messagebox.showwarning("Advertencia", mensaje)
                return
                
            agregar_detalle(
                self.detalles_png,
                f"Encontrados {total_files} archivos PDF para convertir"
            )
            
            # Convertir cada archivo
            successful = 0
            failed = 0
            
            for i, pdf_path in enumerate(pdf_files):
                if not self.procesando:  # Verificar si se canceló el proceso
                    break
                    
                agregar_detalle(
                    self.detalles_png,
                    f"Convirtiendo ({i+1}/{total_files}): {os.path.basename(pdf_path)}"
                )
                
                # Actualizar progreso
                self.barra_progreso_png.set((i+1) / total_files)
                
                # Convertir PDF a PNG
                try:
                    if self.pdf_to_png_converter.convert_pdf_to_png(pdf_path):
                        successful += 1
                        agregar_detalle(
                            self.detalles_png,
                            f"Convertido: {os.path.basename(pdf_path)}",
                            "success"
                        )
                    else:
                        failed += 1
                        agregar_detalle(
                            self.detalles_png,
                            f"Error al convertir: {os.path.basename(pdf_path)}",
                            "error"
                        )
                except Exception as e:
                    failed += 1
                    agregar_detalle(
                        self.detalles_png,
                        f"Error al convertir {os.path.basename(pdf_path)}: {str(e)}",
                        "error"
                    )
            
            # Mostrar resumen
            mensaje = f"Proceso completado. Convertidos {successful} de {total_files} archivos"
            if failed > 0:
                mensaje += f" ({failed} errores)"
                
            self.lbl_estado_png.configure(text=mensaje)
            agregar_detalle(self.detalles_png, mensaje, "success")
            messagebox.showinfo("Proceso completado", mensaje)
                
        except Exception as e:
            mensaje = f"Error: {str(e)}"
            self.lbl_estado_png.configure(text="Error en el proceso")
            agregar_detalle(self.detalles_png, mensaje, "error")
            messagebox.showerror("Error", mensaje)
        finally:
            self.btn_seleccionar_pdf_png.configure(state="normal")
            self.btn_seleccionar_carpeta_png.configure(state="normal")
            self.procesando = False
    
    def iniciar(self):
        """Iniciar la aplicación"""
        self.ventana.mainloop()
