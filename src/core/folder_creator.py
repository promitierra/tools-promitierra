"""
Módulo unificado para creación de carpetas desde plantillas Excel.
"""
from typing import Tuple, Optional, Callable, List, Dict
import os
import pandas as pd
import shutil
import re
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path

from .text_normalizer import TextNormalizer

class FolderCreator:
    """Clase para crear carpetas desde plantillas Excel con validaciones robustas."""
    
    # Caracteres no permitidos en nombres de archivo/carpeta
    CARACTERES_INVALIDOS = r'[<>:"/\\|?*]'
    
    def __init__(self):
        """Inicializar el creador de carpetas."""
        self.text_normalizer = TextNormalizer()
        self.cancelar = False
    
    def crear_plantilla(self, ruta_plantilla: str) -> Tuple[bool, str]:
        """Crear una plantilla de Excel con columnas predefinidas.
        
        Args:
            ruta_plantilla: Ruta donde se guardará la plantilla
        
        Returns:
            Tupla con (éxito, mensaje)
        """
        try:
            # Crear DataFrame con columnas estándar
            df = pd.DataFrame(columns=['ID', 'NOMBRES', 'APELLIDOS', 'CATEGORIA'])
            
            # Agregar algunos ejemplos para guiar al usuario
            ejemplos = [
                {'ID': '001', 'NOMBRES': 'Juan', 'APELLIDOS': 'Pérez', 'CATEGORIA': 'A'},
                {'ID': '002', 'NOMBRES': 'María', 'APELLIDOS': 'García', 'CATEGORIA': 'B'}
            ]
            df = pd.concat([df, pd.DataFrame(ejemplos)], ignore_index=True)
            
            # Guardar plantilla
            df.to_excel(ruta_plantilla, index=False)
            
            return True, f"Plantilla creada en {ruta_plantilla}"
        
        except Exception as e:
            return False, f"Error al crear plantilla: {str(e)}"
    
    def limpiar_nombre_carpeta(self, nombre: str) -> str:
        """Limpia un nombre para que sea válido como nombre de carpeta.
        
        Args:
            nombre: Nombre original
            
        Returns:
            Nombre limpio y válido para carpeta
        """
        # Primero normalizar acentos, etc.
        nombre_limpio = self.text_normalizer.normalize_text(nombre)
        
        # Reemplazar caracteres inválidos con guión bajo
        nombre_limpio = re.sub(self.CARACTERES_INVALIDOS, '_', nombre_limpio)
        
        # Limitar longitud para sistemas de archivos antiguos (255 caracteres máximo)
        if len(nombre_limpio) > 250:
            nombre_limpio = nombre_limpio[:250]
            
        # Eliminar espacios al inicio y final
        nombre_limpio = nombre_limpio.strip()
        
        return nombre_limpio
    
    def verificar_espacio_disponible(self, directorio: str, numero_carpetas: int) -> Tuple[bool, str]:
        """Verifica si hay suficiente espacio en disco.
        
        Args:
            directorio: Ruta del directorio
            numero_carpetas: Número de carpetas a crear
            
        Returns:
            Tupla con (hay_espacio, mensaje)
        """
        try:
            # Obtener espacio disponible en disco
            espacio_disponible = shutil.disk_usage(directorio).free
            
            # Estimar espacio necesario (4KB por carpeta mínimo)
            espacio_estimado = numero_carpetas * 4 * 1024
            
            if espacio_disponible < espacio_estimado:
                return False, f"Espacio insuficiente en disco: {espacio_disponible / (1024*1024):.2f} MB disponibles"
                
            return True, f"Espacio disponible: {espacio_disponible / (1024*1024):.2f} MB"
            
        except Exception as e:
            return False, f"Error al verificar espacio en disco: {str(e)}"
    
    def validar_plantilla(self, df: pd.DataFrame) -> Tuple[bool, str, List[str]]:
        """Valida la estructura y contenido de la plantilla.
        
        Args:
            df: DataFrame con datos de la plantilla
            
        Returns:
            Tupla con (es_valida, mensaje, advertencias)
        """
        advertencias = []
        
        # Validar columnas requeridas
        columnas_requeridas = ['ID', 'NOMBRES']
        for col in columnas_requeridas:
            if col not in df.columns:
                return False, f"Columna '{col}' no encontrada en la plantilla", advertencias
        
        # Validar que haya filas con datos
        if df.empty:
            return False, "La plantilla no contiene datos", advertencias
        
        # Verificar valores vacíos
        if df['ID'].isna().any():
            advertencias.append("Hay filas con ID vacío que serán ignoradas")
            
        if df['NOMBRES'].isna().any():
            advertencias.append("Hay filas con NOMBRES vacíos que serán ignoradas")
        
        # Validar IDs duplicados
        duplicados = df[df.duplicated(subset=['ID'], keep=False)]
        if not duplicados.empty:
            ids_duplicados = duplicados['ID'].unique()
            advertencias.append(f"Se encontraron IDs duplicados: {', '.join(ids_duplicados)}")
        
        return True, "Plantilla válida", advertencias
    
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
    
    def agrupar_por_categoria(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Agrupa los datos por categoría si existe.
        
        Args:
            df: DataFrame con datos
            
        Returns:
            Diccionario con {categoría: dataframe}
        """
        if 'CATEGORIA' in df.columns:
            # Reemplazar valores nulos en CATEGORIA con 'SIN_CATEGORIA'
            df['CATEGORIA'] = df['CATEGORIA'].fillna('SIN_CATEGORIA')
            # Agrupar por categoría
            return {categoria: grupo for categoria, grupo in df.groupby('CATEGORIA')}
        else:
            # Si no hay categoría, usar una categoría por defecto
            return {'SIN_CATEGORIA': df}
    
    def cancelar_proceso(self):
        """Cancela el proceso de creación de carpetas."""
        self.cancelar = True
        
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
        self.cancelar = False
        try:
            # Leer plantilla
            df = pd.read_excel(ruta_excel)
            
            # Validar plantilla
            es_valida, mensaje_validacion, advertencias = self.validar_plantilla(df)
            if not es_valida:
                if hasattr(callbacks, 'on_validation_error'):
                    callbacks.on_validation_error(mensaje_validacion)
                return False, mensaje_validacion
            
            # Reportar advertencias
            if advertencias and hasattr(callbacks, 'on_validation_warning'):
                for advertencia in advertencias:
                    callbacks.on_validation_warning(advertencia)
            
            # Limpiar datos
            df = df.dropna(subset=['ID', 'NOMBRES'])
            
            # Verificar espacio disponible
            hay_espacio, mensaje_espacio = self.verificar_espacio_disponible(
                directorio_salida, 
                len(df)
            )
            
            if not hay_espacio:
                if hasattr(callbacks, 'on_folder_error'):
                    callbacks.on_folder_error('', mensaje_espacio)
                return False, mensaje_espacio
            
            # Agrupar por categoría
            grupos = self.agrupar_por_categoria(df)
            
            # Crear carpetas
            carpetas_creadas = 0
            carpetas_existentes = 0
            
            # Notificar inicio
            if hasattr(callbacks, 'on_start'):
                callbacks.on_start(len(df))
            
            for categoria, grupo_df in grupos.items():
                if self.cancelar:
                    if hasattr(callbacks, 'on_cancel'):
                        callbacks.on_cancel()
                    return False, "Proceso cancelado por el usuario"
                
                # Crear directorio de categoría si es necesario
                directorio_categoria = directorio_salida
                if categoria != 'SIN_CATEGORIA':
                    directorio_categoria = os.path.join(directorio_salida, categoria)
                    os.makedirs(directorio_categoria, exist_ok=True)
                
                for idx, row in grupo_df.iterrows():
                    if self.cancelar:
                        if hasattr(callbacks, 'on_cancel'):
                            callbacks.on_cancel()
                        return False, "Proceso cancelado por el usuario"
                        
                    # Actualizar progreso
                    if hasattr(callbacks, 'on_progress'):
                        progreso = (idx + 1) / len(df)
                        callbacks.on_progress(progreso)
                        
                    # Normalizar nombre
                    nombre_base = f"{row['ID']} - {row['NOMBRES']}"
                    
                    # Agregar apellidos si existen
                    if 'APELLIDOS' in df.columns and pd.notna(row.get('APELLIDOS', '')):
                        nombre_base += f" {row['APELLIDOS']}"
                    
                    # Limpiar y normalizar nombre de carpeta
                    nombre_carpeta = self.limpiar_nombre_carpeta(nombre_base)
                    
                    # Mantener la estructura de categorías
                    ruta_carpeta = os.path.join(directorio_categoria, nombre_carpeta)
                    
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
            
            # Notificar finalización
            if hasattr(callbacks, 'on_complete'):
                callbacks.on_complete(carpetas_creadas, carpetas_existentes)
            
            return True, mensaje
        
        except Exception as e:
            # Manejar errores generales
            if hasattr(callbacks, 'on_folder_error'):
                callbacks.on_folder_error('', str(e))
            
            return False, str(e)
