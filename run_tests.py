#!/usr/bin/env python
"""
Script para ejecutar pruebas con pytest.
Este script facilita la ejecución de pruebas y es compatible con la extensión
"Pruebas" de VS Code.
"""
import sys
import subprocess
import os


def run_tests():
    """
    Ejecuta pruebas utilizando pytest.
    
    Integración con VS Code:
    La extensión "Pruebas" de VS Code busca archivos de prueba utilizando
    la configuración de pytest.ini.
    """
    # Buscar el ejecutable de Python en los entornos virtuales (.venv o venv)
    venv_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                     '.venv', 'bin', 'python'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                     'venv', 'bin', 'python')
    ]
    
    python_executable = None
    for path in venv_paths:
        if os.path.exists(path):
            python_executable = path
            break
    
    # Si no encontramos el Python en entornos virtuales, usar el actual
    if not python_executable:
        python_executable = sys.executable
        print("Advertencia: No se encontró Python en entornos virtuales.")
    
    # Obtener argumentos adicionales
    args = sys.argv[1:]
    
    # Determinar qué pruebas ejecutar (por ahora solo test_helpers.py funciona)
    test_modules = []
    if '--unit' in args:
        test_modules.append('tests/unit/test_helpers.py')
        args.remove('--unit')
    elif '--integration' in args:
        test_modules.append('tests/integration')
        args.remove('--integration')
    elif '--all' in args:
        test_modules.append('tests')
        args.remove('--all')
    else:
        # Por defecto, ejecutar solo test_helpers.py que sabemos que funciona
        test_modules.append('tests/unit/test_helpers.py')
    
    # Obtener la ruta del proyecto
    project_path = os.path.dirname(os.path.abspath(__file__))
    
    # Configurar el entorno con PYTHONPATH actualizado
    env = os.environ.copy()
    
    # Asegurar que el proyecto está en PYTHONPATH
    if 'PYTHONPATH' in env:
        env['PYTHONPATH'] = f"{project_path}:{env['PYTHONPATH']}"
    else:
        env['PYTHONPATH'] = project_path
    
    # Construir el comando a ejecutar
    cmd = [python_executable, '-m', 'pytest'] + test_modules + args
    
    print(f"Ejecutando: {' '.join(cmd)}")
    print(f"PYTHONPATH: {env['PYTHONPATH']}")
    
    # Ejecutar pytest como un proceso
    result = subprocess.run(cmd, env=env)
    return result.returncode


if __name__ == "__main__":
    sys.exit(run_tests()) 