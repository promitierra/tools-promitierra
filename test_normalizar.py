from imagen_a_pdf import ImagenAPdfApp

def main():
    app = ImagenAPdfApp()
    
    # Ejecutar pruebas unitarias
    if app.test_normalizar_texto():
        print("✓ Todas las pruebas pasaron correctamente")
    else:
        print("✗ Algunas pruebas fallaron")
    
    # Pruebas adicionales específicas
    casos_prueba = [
        ("1", "l  uis   FERNando", "LUIS FERNANDO"),
        ("02 5656", "maria    clara", "MARIA CLARA"),
        ("123  456", "Juan   Carlos  PEREZ", "JUAN CARLOS PEREZ"),
    ]
    
    print("\nPruebas de nombres de carpetas:")
    for id_value, nombre, apellido in casos_prueba:
        id_norm = ''.join(str(id_value).strip().split())
        nombre_norm = app.normalizar_texto(nombre)
        apellido_norm = app.normalizar_texto(apellido)
        nombre_carpeta = f"{id_norm} - {nombre_norm} {apellido_norm}"
        print(f"Entrada: ID='{id_value}', Nombre='{nombre}', Apellido='{apellido}'")
        print(f"Salida: '{nombre_carpeta}'")
        print()

if __name__ == "__main__":
    main()
