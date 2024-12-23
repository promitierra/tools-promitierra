import os
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox
import threading
import zipfile
from datetime import datetime
import shutil
import tempfile

class ImagenAPdfApp:
    def __init__(self):
        # Configuración de la ventana principal
        self.ventana = ctk.CTk()
        self.ventana.title("Conversor en lote de imágenes a PDF")
        self.ventana.geometry("450x800")  # Aumentamos aún más la altura
        self.ventana.resizable(False, False)  # Bloqueamos el redimensionamiento
        
        # Configurar el tema
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Variables de control
        self.procesando = False
        self.modo_comprimido = ctk.BooleanVar(value=False)
        self.directorio_salida = None
        
        # Crear el contenido de la ventana
        self.crear_widgets()
        
    def crear_widgets(self):
        # Frame principal con padding
        frame = ctk.CTkFrame(self.ventana)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        titulo = ctk.CTkLabel(frame, text="Conversor de Imágenes a PDF", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack(pady=20)
        
        # Frame para opciones con más espacio
        opciones_frame = ctk.CTkFrame(frame)
        opciones_frame.pack(fill="x", padx=20, pady=20)
        
        # Opciones de salida
        titulo_opciones = ctk.CTkLabel(opciones_frame, text="Opciones de salida:",
                                     font=ctk.CTkFont(weight="bold"))
        titulo_opciones.pack(pady=5)
        
        # Opción A: Misma carpeta
        rb_misma_carpeta = ctk.CTkRadioButton(
            opciones_frame,
            text="Crear PDFs en la misma ubicación que las imágenes",
            variable=self.modo_comprimido,
            value=False
        )
        rb_misma_carpeta.pack(pady=5, padx=20, anchor="w")
        
        # Opción B: Archivo comprimido
        rb_comprimido = ctk.CTkRadioButton(
            opciones_frame,
            text="Generar archivo ZIP con todos los PDFs",
            variable=self.modo_comprimido,
            value=True
        )
        rb_comprimido.pack(pady=5, padx=20, anchor="w")
        
        # Botones
        self.btn_seleccionar = ctk.CTkButton(frame, text="Seleccionar Carpeta", 
                                           command=self.seleccionar_carpeta)
        self.btn_seleccionar.pack(pady=10)
        
        # Barra de progreso
        self.progreso_frame = ctk.CTkFrame(frame)
        self.progreso_frame.pack(fill="x", padx=20, pady=10)
        self.barra_progreso = ctk.CTkProgressBar(self.progreso_frame)
        self.barra_progreso.pack(fill="x", padx=10, pady=5)
        self.barra_progreso.set(0)
        
        # Etiqueta de progreso
        self.progreso_label = ctk.CTkLabel(self.progreso_frame, text="0%")
        self.progreso_label.pack(pady=5)
        
        # Área de estado
        self.estado_label = ctk.CTkLabel(frame, text="Estado: Esperando selección de carpeta",
                                       font=ctk.CTkFont(size=12))
        self.estado_label.pack(pady=10)
        
        # Área de detalles con scroll
        self.detalles_text = ctk.CTkTextbox(frame, height=200)  # Aumentamos la altura del área de detalles
        self.detalles_text.pack(fill="x", padx=20, pady=(20, 30))  # Más espacio después del área de detalles
        self.detalles_text.configure(state="disabled")
        
        # Frame separado para créditos con fondo oscuro y más altura
        creditos_frame = ctk.CTkFrame(self.ventana, fg_color="#2B2B2B", height=100)
        creditos_frame.pack(side="bottom", fill="x", pady=(20, 0))  # Añadido padding superior
        creditos_frame.pack_propagate(False)  # Mantiene la altura fija
        
        # Frame interno para organizar los créditos en dos líneas
        creditos_interno = ctk.CTkFrame(creditos_frame, fg_color="transparent")
        creditos_interno.pack(expand=True)
        
        # Primera línea: Nombre y año
        creditos_linea1 = ctk.CTkLabel(
            creditos_interno, 
            text="Desarrollado por: Luis Fernando Moreno Montoya | 2024",
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC"
        )
        creditos_linea1.pack(pady=(15, 5))  # Aumentado el padding vertical
        
        # Segunda línea: Mensaje especial (dividido en partes para colorear el corazón)
        mensaje_frame = ctk.CTkFrame(creditos_interno, fg_color="transparent")
        mensaje_frame.pack(pady=(5, 15))

        # Primera parte del mensaje
        parte1 = ctk.CTkLabel(
            mensaje_frame, 
            text="Hecho con ",
            font=ctk.CTkFont(size=12),
            text_color="#99CCFF"
        )
        parte1.pack(side="left")

        # Corazón en rojo
        corazon = ctk.CTkLabel(
            mensaje_frame, 
            text="♥",
            font=ctk.CTkFont(size=12),
            text_color="#FF0000"  # Rojo
        )
        corazon.pack(side="left")

        # Resto del mensaje
        parte2 = ctk.CTkLabel(
            mensaje_frame, 
            text=" por la productividad laboral y el cuidado del tiempo",
            font=ctk.CTkFont(size=12),
            text_color="#99CCFF"
        )
        parte2.pack(side="left")
    
    def agregar_detalle(self, texto):
        """Agrega texto al área de detalles"""
        self.detalles_text.configure(state="normal")
        self.detalles_text.insert("end", texto + "\n")
        self.detalles_text.see("end")
        self.detalles_text.configure(state="disabled")
        self.ventana.update()
    
    def seleccionar_carpeta(self):
        if self.procesando:
            messagebox.showwarning("En proceso", "Por favor espera a que termine el proceso actual")
            return
            
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta con imágenes")
        if carpeta:
            # Si es modo comprimido, pedir ubicación del ZIP
            if self.modo_comprimido.get():
                fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_zip = f"PDFs_Convertidos_{fecha_actual}.zip"
                self.directorio_salida = filedialog.asksaveasfilename(
                    defaultextension=".zip",
                    initialfile=nombre_zip,
                    title="Guardar archivo ZIP como",
                    filetypes=[("Archivo ZIP", "*.zip")]
                )
                if not self.directorio_salida:
                    return
            
            # Iniciar proceso en un hilo separado
            thread = threading.Thread(target=self.procesar_carpeta, args=(carpeta,))
            thread.daemon = True
            thread.start()
    
    def procesar_carpeta(self, directorio):
        """Procesa todas las imágenes en la carpeta"""
        temp_dir = None
        try:
            self.procesando = True
            self.btn_seleccionar.configure(state="disabled")
            self.estado_label.configure(text="Estado: Buscando imágenes...")
            
            # Crear directorio temporal si es modo comprimido
            if self.modo_comprimido.get():
                temp_dir = tempfile.mkdtemp()
            
            # Encontrar todas las imágenes
            imagenes = []
            for ruta_actual, _, archivos in os.walk(directorio):
                for archivo in archivos:
                    if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                        imagenes.append(os.path.join(ruta_actual, archivo))
            
            if not imagenes:
                messagebox.showinfo("Información", "No se encontraron imágenes en la carpeta seleccionada")
                self.reset_interfaz()
                return
            
            total_imagenes = len(imagenes)
            convertidas = 0
            errores = 0
            
            self.barra_progreso.set(0)
            self.agregar_detalle(f"Encontradas {total_imagenes} imágenes para convertir")
            
            for ruta_imagen in imagenes:
                try:
                    nombre_archivo = os.path.basename(ruta_imagen)
                    self.estado_label.configure(text=f"Estado: Procesando {nombre_archivo}")
                    
                    # Determinar ruta de salida
                    if self.modo_comprimido.get():
                        # Mantener la estructura de directorios dentro del ZIP
                        ruta_relativa = os.path.relpath(ruta_imagen, directorio)
                        ruta_pdf = os.path.join(temp_dir, os.path.splitext(ruta_relativa)[0] + ".pdf")
                        # Crear directorios necesarios
                        os.makedirs(os.path.dirname(ruta_pdf), exist_ok=True)
                    else:
                        ruta_pdf = os.path.splitext(ruta_imagen)[0] + ".pdf"
                    
                    with Image.open(ruta_imagen) as img:
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        img.save(ruta_pdf, "PDF")
                    
                    convertidas += 1
                    progreso = (convertidas / total_imagenes)
                    self.barra_progreso.set(progreso)
                    self.progreso_label.configure(text=f"{int(progreso * 100)}%")
                    self.agregar_detalle(f"✓ Convertido: {nombre_archivo}")
                    
                except Exception as e:
                    errores += 1
                    self.agregar_detalle(f"✗ Error al convertir {nombre_archivo}: {str(e)}")
                
                self.ventana.update()
            
            # Si es modo comprimido, crear el ZIP
            if self.modo_comprimido.get() and temp_dir:
                self.estado_label.configure(text="Estado: Creando archivo ZIP...")
                self.agregar_detalle("Creando archivo ZIP...")
                
                with zipfile.ZipFile(self.directorio_salida, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arcname)
                
                self.agregar_detalle(f"✓ Archivo ZIP creado en: {self.directorio_salida}")
            
            # Mostrar resumen final
            mensaje = f"Proceso completado\nImágenes convertidas: {convertidas}/{total_imagenes}"
            if errores > 0:
                mensaje += f"\nErrores encontrados: {errores}"
            if self.modo_comprimido.get():
                mensaje += f"\nArchivo ZIP creado en:\n{self.directorio_salida}"
            
            messagebox.showinfo("Completado", mensaje)
            self.estado_label.configure(text="Estado: Proceso completado")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        finally:
            # Limpiar directorio temporal si existe
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            self.reset_interfaz()
    
    def reset_interfaz(self):
        """Resetea la interfaz a su estado inicial"""
        self.procesando = False
        self.btn_seleccionar.configure(state="normal")
        self.ventana.update()

    def iniciar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = ImagenAPdfApp()
    app.iniciar()
