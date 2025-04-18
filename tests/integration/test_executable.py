import os
import subprocess
import time
import shutil

def test_executable():
    print("Iniciando pruebas del ejecutable...")
    
    # Rutas
    exe_path = os.path.join("dist", "ImagenToPDF", "ImagenToPDF.exe")
    test_dir = "test_images"
    output_dir = "test_output"
    
    # Crear directorio de salida
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Copiar imágenes de prueba al directorio de salida
    for file in os.listdir(test_dir):
        shutil.copy2(os.path.join(test_dir, file), output_dir)
    
    # Verificar que el ejecutable existe
    if not os.path.exists(exe_path):
        print("ERROR: No se encuentra el ejecutable en:", exe_path)
        return False
    
    print("\n1. Verificación del ejecutable:")
    print(f"- Tamaño: {os.path.getsize(exe_path) / (1024*1024):.2f} MB")
    print(f"- Ruta: {os.path.abspath(exe_path)}")
    
    # Iniciar el ejecutable
    print("\n2. Iniciando el ejecutable...")
    process = subprocess.Popen([exe_path])
    
    # Dar tiempo para que la interfaz se cargue
    time.sleep(5)
    print("- Interfaz cargada correctamente")
    
    # Verificar que el proceso está corriendo
    if process.poll() is None:
        print("- Proceso ejecutándose correctamente")
    else:
        print("ERROR: El proceso no está corriendo")
        return False
    
    print("\n3. Verificando archivos de prueba:")
    for file in os.listdir(output_dir):
        print(f"- {file}: {os.path.getsize(os.path.join(output_dir, file))} bytes")
    
    # Dar tiempo para pruebas manuales
    print("\nPruebas automáticas completadas.")
    print("Por favor, realiza las siguientes pruebas manuales:")
    print("1. Selecciona la carpeta 'test_output'")
    print("2. Prueba el filtro '*.jpg'")
    print("3. Activa la opción de ZIP")
    print("4. Inicia la conversión")
    print("5. Verifica los archivos generados")
    
    input("\nPresiona Enter cuando hayas terminado las pruebas manuales...")
    
    # Terminar el proceso
    process.terminate()
    print("\nPruebas finalizadas.")

if __name__ == "__main__":
    test_executable()
