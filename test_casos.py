from imagen_a_pdf import ImagenAPdfApp

def probar_casos():
    app = ImagenAPdfApp()
    
    # Lista de casos de prueba: (entrada, salida_esperada)
    casos = [
        # Casos básicos
        ("luis", "LUIS"),
        ("MARIA", "MARIA"),
        
        # Espacios múltiples
        ("l  uis fernan do", "LUIS FERNANDO"),
        ("maria    clara", "MARIA CLARA"),
        ("   juan   pablo  Angel ", "JUAN PABLO ANGEL"),
        
        # Nombres compuestos con espacios internos
        ("l  uis   FERNando", "LUIS FERNANDO"),
        ("Maria  Del  Carmen", "MARIA DEL CARMEN"),
        ("jose    luis   PEREZ", "JOSE LUIS PEREZ"),
        
        # Casos con números y caracteres especiales
        ("123-abc", "123ABC"),
        ("A12B34", "A12B34"),
        ("juan.perez", "JUAN PEREZ"),
        
        # IDs y nombres
        ("1 - l  uis", "1 - LUIS"),
        ("123-l  uis   FERNando", "123 - LUIS FERNANDO"),
        ("A-12 maria    clara", "A12 - MARIA CLARA"),
        
        # Casos extremos
        ("", ""),
        (" ", ""),
        ("   ", ""),
        (None, ""),
        (123, "123"),
    ]
    
    print("Iniciando pruebas de normalización de texto...")
    print("-" * 50)
    
    for entrada, esperado in casos:
        resultado = app.normalizar_texto(entrada)
        coincide = resultado == esperado
        
        print(f"\nEntrada: '{entrada}'")
        print(f"Esperado: '{esperado}'")
        print(f"Obtenido: '{resultado}'")
        print("✓" if coincide else "✗")
        
        if not coincide:
            print("⚠ ¡El resultado no coincide con lo esperado!")
    
    print("\n" + "-" * 50)
    print("Pruebas completadas.")

if __name__ == "__main__":
    probar_casos()
