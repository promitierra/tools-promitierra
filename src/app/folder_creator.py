import os
import pandas as pd
from openpyxl import Workbook

class FolderCreator:
    def __init__(self):
        self.columnas_requeridas = ['ID', 'NOMBRES', 'APELLIDOS']
    
    def crear_plantilla(self, ruta_guardado):
        """Crear plantilla Excel para nombres de carpetas"""
        try:
            wb = Workbook()
            ws = wb.active
            
            # Configurar encabezados
            for i, columna in enumerate(self.columnas_requeridas, 1):
                ws.cell(row=1, column=i, value=columna)
            
            wb.save(ruta_guardado)
            return True, "Plantilla creada exitosamente"
        except Exception as e:
            return False, f"Error al crear plantilla: {str(e)}"
    
    def procesar_plantilla(self, ruta_excel, directorio_destino, callbacks):
        """Procesar plantilla Excel y crear carpetas"""
        try:
            # Leer el Excel
            df = pd.read_excel(ruta_excel)
            
            # Verificar columnas requeridas
            if not all(col in df.columns for col in self.columnas_requeridas):
                return False, "La plantilla no tiene el formato correcto"
            
            # Crear directorio destino si no existe
            if not os.path.exists(directorio_destino):
                os.makedirs(directorio_destino)
            
            # Crear carpetas
            carpetas_creadas = 0
            errores = []
            
            for _, row in df.iterrows():
                try:
                    nombre_carpeta = f"{row['ID']} - {row['NOMBRES']} {row['APELLIDOS']}"
                    # Limpiar caracteres inválidos
                    nombre_carpeta = "".join(c for c in nombre_carpeta if c not in r'<>:"/\|?*')
                    ruta_carpeta = os.path.join(directorio_destino, nombre_carpeta)
                    
                    if not os.path.exists(ruta_carpeta):
                        os.makedirs(ruta_carpeta)
                        carpetas_creadas += 1
                        callbacks.on_folder_created(nombre_carpeta)
                    else:
                        callbacks.on_folder_exists(nombre_carpeta)
                except Exception as e:
                    errores.append((nombre_carpeta, str(e)))
                    callbacks.on_folder_error(nombre_carpeta, str(e))
            
            mensaje = f"Se crearon {carpetas_creadas} carpetas"
            if errores:
                mensaje += f" con {len(errores)} errores"
            return True, mensaje
            
        except Exception as e:
            return False, f"Error al procesar plantilla: {str(e)}"
