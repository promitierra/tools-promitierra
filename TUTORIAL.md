# Tutorial de Uso - Herramientas ProMITIERRA v0.2.2

## Introducción

Esta herramienta ofrece dos funcionalidades principales:

1. Creación automática de carpetas desde plantilla Excel
2. Conversión de imágenes a PDF manteniendo la estructura de carpetas

## Requisitos

- Windows 10 o superior
- No se requiere instalación de Python ni otras dependencias

## 1. Creación Automática de Carpetas

1. **Obtener la Plantilla Excel**

   - Al abrir la aplicación, ve a la pestaña "Crear Carpetas"
   - Haz clic en el botón "Descargar Plantilla"
   - Se creará un archivo Excel con el formato requerido
   - La plantilla contiene las columnas:
     - ID: Identificador único
     - NOMBRES: Nombre de la persona o entidad
     - APELLIDOS: (Opcional) Apellidos

2. **Llenar la Plantilla**

   - Abre la plantilla descargada
   - Llena las columnas con la información requerida
   - No modifiques los nombres de las columnas
   - Guarda el archivo Excel

3. **Usar la Herramienta**

   - En la pestaña "Crear Carpetas":
     - Haz clic en "Seleccionar Plantilla" y elige tu archivo Excel
     - Selecciona la carpeta donde se crearán los directorios
     - Haz clic en "Crear Carpetas"

4. **Resultados**

   - Se crearán carpetas con los nombres normalizados
   - Los nombres se formarán usando ID, nombres y apellidos
   - Se manejarán automáticamente caracteres especiales

## 2. Conversión de Imágenes a PDFs

1. **Iniciar la Aplicación**

   - En la misma aplicación `Herramientas ProMITIERRA.exe`
   - Ve a la pestaña "Convertir Imágenes a PDF"
2. **Convertir Imágenes a PDF**

   - Haz clic en el botón "Seleccionar Carpeta"
   - Navega y selecciona la carpeta que contiene tus imágenes
   - La herramienta procesará todas las subcarpetas automáticamente
3. **Opciones de Conversión**

   - **Modo Simple**: Los PDFs se crearán en las mismas carpetas que las imágenes originales
   - **Modo ZIP**: Activa la casilla "Generar archivo comprimido" para crear un ZIP con todos los PDFs
4. **Durante la Conversión**

   - Verás una barra de progreso
   - Los detalles de la conversión aparecerán en la ventana de texto
   - Espera a que el proceso termine
5. **Resultados**

   - **Modo Simple**: Encontrarás los PDFs junto a las imágenes originales
   - **Modo ZIP**: Encontrarás un archivo ZIP en la carpeta principal con fecha y hora

## Ejemplos

### Creación de Carpetas

```
Plantilla Excel:
ID    | NOMBRES      | APELLIDOS
------|-------------|------------
001   | Juan Carlos | Pérez López
002   | María       | González

Resultado:
└── Carpeta Destino
    ├── 001_JUAN_CARLOS_PEREZ_LOPEZ
    └── 002_MARIA_GONZALEZ
```

### Conversión Simple

```
Carpeta Original:
  └── Fotos
      ├── 2023
      │   ├── Enero
      │   │   └── foto1.jpg
      │   └── Febrero
      │       └── foto2.png
      └── 2024
          └── foto3.jpg

Resultado:
  └── Fotos
      ├── 2023
      │   ├── Enero
      │   │   ├── foto1.jpg
      │   │   └── foto1.pdf
      │   └── Febrero
      │       ├── foto2.png
      │       └── foto2.pdf
      └── 2024
          ├── foto3.jpg
          └── foto3.pdf
```

### Modo ZIP

```
Carpeta Original: [igual que arriba]

Resultado:
  └── Fotos
      ├── [estructura original]
      └── PDFs_20241224_130000.zip
          └── [PDFs con la misma estructura de carpetas]
```

## Solución de Problemas

1. **La aplicación no inicia**

   - Verifica que estés usando Windows 10 o superior
   - Intenta ejecutar como administrador
2. **Errores durante la conversión**

   - Los errores se mostrarán en la ventana de detalles
   - El proceso continuará con las demás imágenes
3. **Archivos no convertidos**

   - Verifica que sean formatos soportados (PNG, JPG, JPEG, BMP, TIFF, WEBP, GIF)
   - Asegúrate de que los archivos no estén dañados
4. **Problemas con la plantilla Excel**

   - Verifica que las columnas tengan los nombres correctos
   - Asegúrate de que no haya filas vacías
   - Comprueba que los IDs sean únicos

## Formatos Soportados

- PNG
- JPG/JPEG
- BMP
- TIFF
- WEBP
- GIF

## Notas Importantes

- La aplicación mantiene tus archivos originales intactos
- Los PDFs se crean con calidad optimizada
- Las imágenes grandes se redimensionan automáticamente para mejor rendimiento
- El proceso es paralelo para mayor velocidad
- Los nombres de carpetas se normalizan automáticamente (mayúsculas, sin acentos)
