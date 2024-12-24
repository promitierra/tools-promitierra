"""
Módulo de interfaz gráfica para la aplicación.
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from datetime import datetime
from .pdf_converter import PDFConverter
from src.core.folder_creator import FolderCreator
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
        self.directorio_salida = None
        
        # Inicializar componentes
        self.pdf_converter = PDFConverter()
        self.folder_creator = FolderCreator()
        
        # Crear interfaz
        self.crear_widgets()
    
    def crear_widgets(self):
        # Preparar la estructura para agregar pestañas
        self.notebook = ctk.CTkTabview(self.ventana)
        self.notebook.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Pestañas
        self.pestaña_carpetas = self.notebook.add("Crear Carpetas")
        self.pestaña_principal = self.notebook.add("imagenes a PDFs")
        
        # Crear contenido
        self.crear_contenido_pestaña_carpetas()
        self.crear_contenido_pestaña_principal()

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

    def iniciar(self):
        """Iniciar la aplicación"""
        self.ventana.mainloop()
