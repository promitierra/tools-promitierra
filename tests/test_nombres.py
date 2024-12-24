from imagen_a_pdf import ImagenAPdfApp

def probar_casos():
    app = ImagenAPdfApp()
    
    # Lista de casos de prueba: (entrada, salida_esperada)
    casos = [
        # Casos de ID - NOMBRES APELLIDOS
        ("123 - Luis Fernando", "123 - LUIS FERNANDO"),
        ("A12 - Maria Clara", "A12 - MARIA CLARA"),
        ("001-Juan Pablo Angel", "001 - JUAN PABLO ANGEL"),
        
        # Casos con espacios múltiples
        ("123  -  Luis   Fernando", "123 - LUIS FERNANDO"),
        ("A12-   Maria    Clara   ", "A12 - MARIA CLARA"),
        ("001  -Juan   Pablo  Angel", "001 - JUAN PABLO ANGEL"),
        
        # Casos con mezcla de mayúsculas/minúsculas
        ("123-luis FERNando", "123 - LUIS FERNANDO"),
        ("A12-MARIA clara", "A12 - MARIA CLARA"),
        ("001-Juan pablo ANGEL", "001 - JUAN PABLO ANGEL"),
        
        # Casos especiales
        ("123ABC - Luis", "123ABC - LUIS"),
        ("A-12 - Maria Clara", "A12 - MARIA CLARA"),
        ("001.1 - Juan Pablo", "0011 - JUAN PABLO"),
        
        # Casos sin guion
        ("Luis Fernando", "- LUIS FERNANDO"),
        ("Maria Clara", "- MARIA CLARA"),
        ("Juan Pablo Angel", "- JUAN PABLO ANGEL"),
        
        # Casos extremos
        ("", " - "),
        (" ", " - "),
        ("   ", " - "),
        (None, " -"),
        ("123 -", "123 - "),
        ("- Luis", " - LUIS"),
    ]
    
    print("Iniciando pruebas de normalización de texto...")
    print("-" * 50)
    
    errores = 0
    for entrada, esperado in casos:
        resultado = app.normalizar_texto(entrada)
        coincide = resultado == esperado
        
        print(f"\nEntrada: '{entrada}'")
        print(f"Esperado: '{esperado}'")
        print(f"Obtenido: '{resultado}'")
        print("[OK]" if coincide else "[ERROR]")
        
        if not coincide:
            print("! El resultado no coincide con lo esperado!")
            errores += 1
    
    print("\n" + "-" * 50)
    print(f"Pruebas completadas. {errores} errores encontrados.")

if __name__ == "__main__":
    probar_casos()
