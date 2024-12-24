import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from datetime import datetime
from .pdf_converter import PDFConverter
from .folder_creator import FolderCreator
from ..utils.helpers import agregar_detalle, actualizar_progreso, generar_nombre_zip
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
        """Crear carpetas desde Excel"""
        try:
            # Seleccionar archivo Excel
            ruta_excel = filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx")],
                title="Seleccionar archivo Excel"
            )
            if not ruta_excel:
                return

            # Seleccionar carpeta destino
            directorio_destino = filedialog.askdirectory(
                title="Seleccionar carpeta destino"
            )
            if not directorio_destino:
                return

            # Callbacks para el proceso
            class Callbacks:
                def on_folder_created(self, nombre):
                    agregar_detalle(self.detalles_carpetas, f"Creada: {nombre}", "success")

                def on_folder_exists(self, nombre):
                    agregar_detalle(self.detalles_carpetas, f"Ya existe: {nombre}", "warning")

                def on_folder_error(self, nombre, error):
                    agregar_detalle(self.detalles_carpetas, f"Error en {nombre}: {error}", "error")

            # Procesar plantilla
            exito, resultado = self.folder_creator.procesar_plantilla(
                ruta_excel,
                directorio_destino,
                Callbacks()
            )

            if exito:
                carpetas_creadas, errores = resultado
                mensaje = f"Se crearon {carpetas_creadas} carpetas"
                if errores:
                    mensaje += f" con {len(errores)} errores"
                messagebox.showinfo("Completado", mensaje)
            else:
                messagebox.showerror("Error", resultado)

        except Exception as e:
            agregar_detalle(self.detalles_carpetas, f"Error: {str(e)}", "error")
            messagebox.showerror("Error", str(e))

    def seleccionar_carpeta(self):
        """Seleccionar carpeta para procesar imágenes"""
        if self.procesando:
            self.pdf_converter.cancelar_proceso()
            self.btn_seleccionar.configure(text="Seleccionar Carpeta")
            self.procesando = False
            return
            
        directorio = filedialog.askdirectory()
        if not directorio:
            return
            
        # Validar directorio
        valido, mensaje = validar_directorio(directorio)
        if not valido:
            messagebox.showerror("Error", mensaje)
            return
        
        # Configurar callbacks
        class Callbacks:
            def __init__(self):
                self.started = False
                self.files_found = 0
                self.converted = []
                self.errors = []
                
            def on_start(self):
                self.lbl_estado.configure(text="Iniciando proceso...")
                self.btn_seleccionar.configure(text="Cancelar")
                agregar_detalle(self.detalles, "Iniciando proceso...", "info")
                
            def on_no_images(self):
                self.lbl_estado.configure(text="No se encontraron imágenes")
                messagebox.showinfo("Info", "No se encontraron imágenes")
                
            def on_images_found(self, total):
                self.lbl_estado.configure(text=f"Encontradas {total} imágenes")
                agregar_detalle(self.detalles, f"Encontradas {total} imágenes", "info")
                
            def on_processing_file(self, nombre):
                self.lbl_estado.configure(text=f"Procesando: {nombre}")
                
            def on_progress(self, valor):
                actualizar_progreso(self.barra_progreso, valor)
                
            def on_file_converted(self, nombre):
                agregar_detalle(self.detalles, f"Convertido: {nombre}", "success")
                
            def on_file_error(self, nombre, error):
                agregar_detalle(self.detalles, f"Error en {nombre}: {error}", "error")
                
            def on_complete(self, convertidas, total, errores, modo_comprimido):
                mensaje = f"Proceso completado. Convertidas {convertidas} de {total} imágenes"
                if errores > 0:
                    mensaje += f" ({errores} errores)"
                self.lbl_estado.configure(text=mensaje)
                agregar_detalle(self.detalles, mensaje, "success")
                
            def on_creating_zip(self):
                self.lbl_estado.configure(text="Creando archivo ZIP...")
                agregar_detalle(self.detalles, "Creando archivo ZIP...", "info")
                
            def on_zip_created(self, ruta):
                agregar_detalle(self.detalles, f"ZIP creado en: {ruta}", "success")
                
            def on_error(self, error):
                messagebox.showerror("Error", f"Error: {error}")
                agregar_detalle(self.detalles, f"Error: {error}", "error")
                
            def on_finish(self):
                self.procesando = False
                self.btn_seleccionar.configure(text="Seleccionar Carpeta")
                
        callbacks = Callbacks()
        callbacks.__dict__.update(self.__dict__)
        
        # Iniciar procesamiento
        self.procesando = True
        if self.modo_comprimido.get():
            # Solicitar ubicación para el ZIP
            zip_path = filedialog.asksaveasfilename(
                defaultextension=".zip",
                filetypes=[("Archivo ZIP", "*.zip")],
                initialfile=f"PDFs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            )
            if not zip_path:
                self.procesando = False
                return
            self.pdf_converter.directorio_salida = zip_path
            
        # Iniciar conversión en un hilo separado
        threading.Thread(
            target=self.pdf_converter.procesar_carpeta,
            args=(directorio, self.modo_comprimido.get(), callbacks)
        ).start()

    def iniciar(self):
        """Iniciar la aplicación"""
        self.ventana.mainloop()
