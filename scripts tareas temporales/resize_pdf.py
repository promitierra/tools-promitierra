try:
    import fitz
    from reportlab.lib.pagesizes import letter
    import sys
    import os
    # Importar el módulo compartido para el procesamiento de PDF
    from src.core.pdf_resize_algorithm import process_pdf, LETTER_WIDTH, LETTER_HEIGHT, LETTER_WIDTH_LANDSCAPE, LETTER_HEIGHT_LANDSCAPE
except ImportError:
    print("Por favor instale los paquetes requeridos: pip install pymupdf reportlab")
    import sys
    sys.exit(1)

# Función principal para redimensionar PDF
def resize_pdf(input_pdf, output_pdf, centrar=False):
    try:
        doc = fitz.open(input_pdf)
        # Utilizar el módulo compartido para procesar el PDF
        new_doc_final = process_pdf(doc, centrar)
        
        # Guardar el documento final con las páginas redimensionadas
        new_doc_final.save(output_pdf)
        print(f"PDF redimensionado exitosamente a tamaño carta (preservando orientación): {output_pdf}")
        return True
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error procesando PDF: {e}")
        sys.exit(1)  # Aseguramos que se lance SystemExit
    finally:
        # Cerrar los documentos si fueron abiertos
        if 'doc' in locals() and doc:
            doc.close()
        if 'new_doc_final' in locals() and new_doc_final:
            new_doc_final.close()

# Función para listar archivos PDF en el directorio especificado
def listar_pdfs_disponibles(directorio=None):
    # Si no se especifica un directorio, usar el directorio actual
    if directorio is None:
        directorio = os.getcwd()
    
    try:
        # Obtener la lista de archivos en el directorio especificado
        archivos = os.listdir(directorio)
        # Filtrar solo los archivos PDF
        pdfs = [archivo for archivo in archivos if archivo.lower().endswith('.pdf')]
        
        if not pdfs:
            print(f"No se encontraron archivos PDF en: {directorio}")
            print("Puede ingresar una ruta alternativa a continuación.")
        
        return pdfs, directorio
    except Exception as e:
        print(f"Error al listar archivos en {directorio}: {e}")
        return [], directorio

# Función para mostrar menú de selección
def mostrar_menu_seleccion(pdfs, directorio_actual=None):
    # Si no se especifica un directorio, usar el directorio actual
    if directorio_actual is None:
        directorio_actual = os.getcwd()
    
    print(f"\nArchivos PDF disponibles en: {directorio_actual}")
    for i, pdf in enumerate(pdfs, 1):
        print(f"{i}. {pdf}")
    
    # Agregar opciones adicionales
    print("R. Ingresar ruta alternativa a un archivo o carpeta")
    print("V. Volver al directorio principal")
    
    while True:
        try:
            seleccion_input = input("\nSeleccione el número del archivo PDF a redimensionar (0 para salir, R para ruta alternativa, V para volver): ")
            
            # Verificar si el usuario quiere volver al directorio principal
            if seleccion_input.upper() == 'V':
                # Volver al directorio principal y mostrar PDFs disponibles
                pdfs_nuevos, directorio_nuevo = listar_pdfs_disponibles()
                return mostrar_menu_seleccion(pdfs_nuevos, directorio_nuevo)
            
            # Verificar si el usuario quiere ingresar una ruta alternativa
            if seleccion_input.upper() == 'R':
                while True:
                    ruta_alternativa = input("\nIngrese la ruta completa al archivo PDF o carpeta: ").strip()
                    
                    # Eliminar comillas si el usuario las incluyó
                    if (ruta_alternativa.startswith('"') and ruta_alternativa.endswith('"')) or \
                       (ruta_alternativa.startswith("'") and ruta_alternativa.endswith("'")):
                        ruta_alternativa = ruta_alternativa[1:-1]
                    
                    # Verificar si la ruta existe
                    if os.path.exists(ruta_alternativa):
                        # Si es un directorio, listar PDFs en ese directorio
                        if os.path.isdir(ruta_alternativa):
                            print(f"\nBuscando PDFs en: {ruta_alternativa}")
                            pdfs_nuevos, directorio_nuevo = listar_pdfs_disponibles(ruta_alternativa)
                            if pdfs_nuevos:
                                return mostrar_menu_seleccion(pdfs_nuevos, directorio_nuevo)
                            else:
                                opcion = input("¿Desea intentar con otra ruta? (s/n): ").strip().lower()
                                if opcion != 's' and opcion != 'si' and opcion != 'sí':
                                    print("Operación cancelada.")
                                    sys.exit(0)
                        # Si es un archivo PDF, devolverlo directamente
                        elif ruta_alternativa.lower().endswith('.pdf'):
                            return ruta_alternativa
                        else:
                            print(f"Error: El archivo '{ruta_alternativa}' no es un PDF.")
                            opcion = input("¿Desea intentar con otra ruta? (s/n): ").strip().lower()
                            if opcion != 's' and opcion != 'si' and opcion != 'sí':
                                print("Operación cancelada.")
                                sys.exit(0)
                    else:
                        print(f"Error: La ruta '{ruta_alternativa}' no existe.")
                        opcion = input("¿Desea intentar con otra ruta? (s/n): ").strip().lower()
                        if opcion != 's' and opcion != 'si' and opcion != 'sí':
                            print("Operación cancelada.")
                            sys.exit(0)
            
            # Procesar selección numérica
            seleccion = int(seleccion_input)
            if seleccion == 0:
                print("Operación cancelada.")
                sys.exit(0)
            elif 1 <= seleccion <= len(pdfs):
                # Construir la ruta completa al archivo seleccionado
                archivo_seleccionado = pdfs[seleccion-1]
                ruta_completa = os.path.join(directorio_actual, archivo_seleccionado)
                return ruta_completa
            else:
                print(f"Por favor, ingrese un número entre 1 y {len(pdfs)}, 0 para salir, R para ruta alternativa, o V para volver.")
        except ValueError:
            if seleccion_input.upper() not in ['R', 'V']:
                print("Por favor, ingrese un número válido, 0 para salir, R para ruta alternativa, o V para volver.")

# Ejecutar el script solo cuando se llama directamente
if __name__ == "__main__":
    # Verificar si se proporcionaron argumentos de línea de comandos
    if len(sys.argv) >= 3:
        input_pdf = sys.argv[1]
        output_pdf = sys.argv[2]
        
        # Verificar si hay un tercer argumento para centrar
        centrar = False
        if len(sys.argv) > 3 and sys.argv[3].lower() in ['centrar', 'c', 'center', 'true', 's', 'si', 'sí']:
            centrar = True
        
        # Verificar si el archivo de entrada existe
        if not os.path.exists(input_pdf):
            print(f"Error: El archivo de entrada '{input_pdf}' no existe")
            sys.exit(1)
    else:
        # Mostrar archivos PDF disponibles y permitir selección
        pdfs_disponibles, directorio_actual = listar_pdfs_disponibles()
        
        # Si no hay PDFs disponibles, mostrar directamente la opción de ruta alternativa
        if not pdfs_disponibles:
            while True:
                ruta_alternativa = input("\nIngrese la ruta completa al archivo PDF o carpeta: ").strip()
                
                # Eliminar comillas si el usuario las incluyó
                if (ruta_alternativa.startswith('"') and ruta_alternativa.endswith('"')) or \
                   (ruta_alternativa.startswith("'") and ruta_alternativa.endswith("'")):
                    ruta_alternativa = ruta_alternativa[1:-1]
                
                # Verificar si la ruta existe
                if os.path.exists(ruta_alternativa):
                    # Si es un directorio, listar PDFs en ese directorio
                    if os.path.isdir(ruta_alternativa):
                        print(f"\nBuscando PDFs en: {ruta_alternativa}")
                        pdfs_nuevos, directorio_nuevo = listar_pdfs_disponibles(ruta_alternativa)
                        if pdfs_nuevos:
                            input_pdf = mostrar_menu_seleccion(pdfs_nuevos, directorio_nuevo)
                            break
                        else:
                            opcion = input("¿Desea intentar con otra ruta? (s/n): ").strip().lower()
                            if opcion != 's' and opcion != 'si' and opcion != 'sí':
                                print("Operación cancelada.")
                                sys.exit(0)
                    # Si es un archivo PDF, usarlo directamente
                    elif ruta_alternativa.lower().endswith('.pdf'):
                        input_pdf = ruta_alternativa
                        break
                    else:
                        print(f"Error: El archivo '{ruta_alternativa}' no es un PDF.")
                        opcion = input("¿Desea intentar con otra ruta? (s/n): ").strip().lower()
                        if opcion != 's' and opcion != 'si' and opcion != 'sí':
                            print("Operación cancelada.")
                            sys.exit(0)
                else:
                    print(f"Error: La ruta '{ruta_alternativa}' no existe.")
                    opcion = input("¿Desea intentar con otra ruta? (s/n): ").strip().lower()
                    if opcion != 's' and opcion != 'si' and opcion != 'sí':
                        print("Operación cancelada.")
                        sys.exit(0)
        else:
            input_pdf = mostrar_menu_seleccion(pdfs_disponibles, directorio_actual)
        
        # Solicitar nombre del archivo de salida
        nombre_base = os.path.splitext(input_pdf)[0]
        output_pdf_default = f"{nombre_base}_letter.pdf"
        output_pdf_input = input(f"\nNombre del archivo de salida [{output_pdf_default}]: ").strip()
        output_pdf = output_pdf_input if output_pdf_input else output_pdf_default
        
        # Preguntar si desea centrar el contenido
        centrar_input = input("\n¿Desea centrar el contenido en la página? (s/n) [n]: ").strip().lower()
        centrar = centrar_input == 's' or centrar_input == 'si' or centrar_input == 'sí'
        
        print(f"\nProcesando: {input_pdf} -> {output_pdf} (Centrado: {'Sí' if centrar else 'No'})")
    
    # Llamar a la función principal
    resize_pdf(input_pdf, output_pdf, centrar)