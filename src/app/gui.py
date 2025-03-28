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

class ImagenAPdfGUI:
    def __init__(self):
        # Configuración de la ventana principal
        self.ventana = ctk.CTk()
        self.ventana.title("Herramientas de Productividad")
        self.ventana.geometry("500x500")
        self.ventana.resizable(False, False)
        
        # Configurar el tema
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Variables de control
        self.procesando = False
        self.modo_comprimido = ctk.BooleanVar(value=False)
        self.centrar_contenido = ctk.BooleanVar(value=False)
        self.directorio_salida = None
        
        # Inicializar componentes
        self.pdf_converter = PDFConverter()
        self.folder_creator = FolderCreator()
        self.pdf_resizer = PDFResizer()
        self.pdf_to_png_converter = PDFToPNGConverter()
        
        # Crear interfaz
        self.crear_widgets()
    
    def crear_widgets(self):
        # Preparar la estructura para agregar pestañas
        self.notebook = ctk.CTkTabview(self.ventana)
        self.notebook.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Pestañas
        self.pestaña_carpetas = self.notebook.add("Crear Carpetas")
        self.pestaña_principal = self.notebook.add("imagenes a PDFs")
        self.pestaña_resize_pdf = self.notebook.add("Redimensionar PDF")
        self.pestaña_pdf_a_png = self.notebook.add("PDF a PNG")
        
        # Crear contenido
        self.crear_contenido_pestaña_carpetas()
        self.crear_contenido_pestaña_principal()
        self.crear_contenido_pestaña_resize_pdf()
        self.crear_contenido_pestaña_pdf_a_png()

    def crear_contenido_pestaña_carpetas(self):
        """Crear el contenido de la pestaña de creación de carpetas"""
        # Título y descripción
        titulo = ctk.CTkLabel(
            self.pestaña_carpetas,
            text="Crear Carpetas desde Excel",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(pady=(20, 10))

        descripcion = ctk.CTkLabel(
            self.pestaña_carpetas,
            text="1. Descarga la plantilla Excel\n2. Llena los datos y guarda el archivo",
            font=ctk.CTkFont(size=14)
        )
        descripcion.pack(pady=(0, 20))

        # Frame para botones
        botones_frame = ctk.CTkFrame(self.pestaña_carpetas, fg_color="transparent")
        botones_frame.pack(fill="x", padx=20)

        # Botón para descargar plantilla
        btn_plantilla = ctk.CTkButton(
            botones_frame,
            text="Descargar Plantilla",
            command=self.descargar_plantilla
        )
        btn_plantilla.pack(side="left", padx=5, expand=True)

        # Botón para crear carpetas
        btn_crear = ctk.CTkButton(
            botones_frame,
            text="Crear Carpetas",
            command=self.crear_carpetas
        )
        btn_crear.pack(side="left", padx=5, expand=True)

        # Área de detalles
        self.detalles_carpetas = ctk.CTkTextbox(
            self.pestaña_carpetas,
            height=75
        )
        self.detalles_carpetas.pack(fill="both", expand=True, padx=20, pady=20)

        # Footer
        self.crear_footer(self.pestaña_carpetas)

    def crear_contenido_pestaña_principal(self):
        """Crear el contenido de la pestaña principal"""
        # Título
        titulo = ctk.CTkLabel(
            self.pestaña_principal,
            text="Convertir Imágenes a PDF",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(pady=(20, 10))
        
        # Frame superior
        frame_superior = ctk.CTkFrame(self.pestaña_principal)
        frame_superior.pack(fill="x", padx=20, pady=10)

        # Checkbox para modo comprimido
        self.check_comprimir = ctk.CTkCheckBox(
            frame_superior,
            text="Comprimir PDFs en ZIP",
            variable=self.modo_comprimido
        )
        self.check_comprimir.pack(side="left", padx=10)

        # Botón para seleccionar carpeta
        self.btn_seleccionar = ctk.CTkButton(
            frame_superior,
            text="Seleccionar Carpeta",
            command=self.seleccionar_carpeta
        )
        self.btn_seleccionar.pack(side="right", padx=10)

        # Barra de progreso
        self.barra_progreso = ctk.CTkProgressBar(self.pestaña_principal)
        self.barra_progreso.pack(fill="x", padx=20, pady=10)
        self.barra_progreso.set(0)

        # Estado
        self.lbl_estado = ctk.CTkLabel(
            self.pestaña_principal,
            text="Esperando selección de carpeta..."
        )
        self.lbl_estado.pack(pady=5)

        # Área de detalles
        self.detalles = ctk.CTkTextbox(
            self.pestaña_principal,
            height=75
        )
        self.detalles.pack(fill="both", expand=True, padx=20, pady=20)

        # Footer
        self.crear_footer(self.pestaña_principal)

    def crear_footer(self, frame_padre):
        """Crear el pie de página con créditos"""
        creditos_interno = ctk.CTkFrame(frame_padre, fg_color="transparent")
        creditos_interno.pack(side="bottom", fill="x", pady=(10, 3))

        creditos_linea1 = ctk.CTkLabel(
            creditos_interno,
            text="Desarrollado por: Luis Fernando Moreno Montoya | 2024",
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

        corazon = ctk.CTkLabel(
            mensaje_frame,
            text="♥",
            font=ctk.CTkFont(size=13),
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

    def crear_contenido_pestaña_resize_pdf(self):
        """Crear el contenido de la pestaña de redimensionamiento de PDF"""
        # Título
        titulo = ctk.CTkLabel(
            self.pestaña_resize_pdf,
            text="Redimensionar PDF a Tamaño Carta",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(pady=(20, 10))
        
        # Descripción
        descripcion = ctk.CTkLabel(
            self.pestaña_resize_pdf,
            text="Redimensiona un PDF al tamaño carta, preservando la orientación",
            font=ctk.CTkFont(size=14)
        )
        descripcion.pack(pady=(0, 20))
        
        # Frame para opciones
        opciones_frame = ctk.CTkFrame(self.pestaña_resize_pdf)
        opciones_frame.pack(fill="x", padx=20, pady=10)
        
        # Checkbox para centrar contenido
        self.check_centrar = ctk.CTkCheckBox(
            opciones_frame,
            text="Centrar contenido en la página",
            variable=self.centrar_contenido
        )
        self.check_centrar.pack(side="left", padx=10, pady=10)
        
        # Frame para botones
        botones_frame = ctk.CTkFrame(self.pestaña_resize_pdf, fg_color="transparent")
        botones_frame.pack(fill="x", padx=20, pady=10)
        
        # Botón para seleccionar archivo PDF
        self.btn_seleccionar_pdf = ctk.CTkButton(
            botones_frame,
            text="Seleccionar PDF",
            command=self.seleccionar_pdf_para_redimensionar
        )
        self.btn_seleccionar_pdf.pack(side="left", padx=5, expand=True)
        
        # Barra de progreso
        self.barra_progreso_resize = ctk.CTkProgressBar(self.pestaña_resize_pdf)
        self.barra_progreso_resize.pack(fill="x", padx=20, pady=10)
        self.barra_progreso_resize.set(0)
        
        # Estado
        self.lbl_estado_resize = ctk.CTkLabel(
            self.pestaña_resize_pdf,
            text="Esperando selección de archivo PDF..."
        )
        self.lbl_estado_resize.pack(pady=5)
        
        # Área de detalles
        self.detalles_resize = ctk.CTkTextbox(
            self.pestaña_resize_pdf,
            height=75
        )
        self.detalles_resize.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Footer
        self.crear_footer(self.pestaña_resize_pdf)
    
    def crear_contenido_pestaña_pdf_a_png(self):
        """Crear el contenido de la pestaña de conversión de PDF a PNG"""
        # Título
        titulo = ctk.CTkLabel(
            self.pestaña_pdf_a_png,
            text="Convertir PDF a PNG",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(pady=(20, 10))
        
        # Descripción
        descripcion = ctk.CTkLabel(
            self.pestaña_pdf_a_png,
            text="Extrae imágenes de archivos PDF y las guarda como PNG",
            font=ctk.CTkFont(size=14)
        )
        descripcion.pack(pady=(0, 20))
        
        # Frame para botones
        botones_frame = ctk.CTkFrame(self.pestaña_pdf_a_png, fg_color="transparent")
        botones_frame.pack(fill="x", padx=20, pady=10)
        
        # Botón para seleccionar archivo PDF
        self.btn_seleccionar_pdf_png = ctk.CTkButton(
            botones_frame,
            text="Seleccionar PDF",
            command=self.seleccionar_pdf_para_png
        )
        self.btn_seleccionar_pdf_png.pack(side="left", padx=5, expand=True)
        
        # Botón para seleccionar carpeta con PDFs
        self.btn_seleccionar_carpeta_png = ctk.CTkButton(
            botones_frame,
            text="Seleccionar Carpeta",
            command=self.seleccionar_carpeta_para_png
        )
        self.btn_seleccionar_carpeta_png.pack(side="left", padx=5, expand=True)
        
        # Barra de progreso
        self.barra_progreso_png = ctk.CTkProgressBar(self.pestaña_pdf_a_png)
        self.barra_progreso_png.pack(fill="x", padx=20, pady=10)
        self.barra_progreso_png.set(0)
        
        # Estado
        self.lbl_estado_png = ctk.CTkLabel(
            self.pestaña_pdf_a_png,
            text="Esperando selección de archivo o carpeta..."
        )
        self.lbl_estado_png.pack(pady=5)
        
        # Área de detalles
        self.detalles_png = ctk.CTkTextbox(
            self.pestaña_pdf_a_png,
            height=75
        )
        self.detalles_png.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Footer
        self.crear_footer(self.pestaña_pdf_a_png)
    
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
