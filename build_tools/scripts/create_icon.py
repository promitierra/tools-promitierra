from PIL import Image
import os

def create_icon():
    # Primero vamos a crear una imagen base limpia con el diseño que queremos
    size = (256, 256)  # Tamaño base más pequeño para mejor calidad
    icon = Image.new('RGBA', size, (0, 0, 0, 0))
    
    # Cargar la imagen original
    input_path = "DALL·E 2024-12-23 12.09.15 - A modern icon in the style of Material Design, representing image-to-PDF conversion. The design includes an image icon (a rectangle with a mountain an.webp"
    img = Image.open(input_path)
    
    # Convertir a RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Redimensionar la imagen original manteniendo la proporción
    img.thumbnail(size, Image.Resampling.LANCZOS)
    
    # Calcular la posición para centrar la imagen
    x = (size[0] - img.size[0]) // 2
    y = (size[1] - img.size[1]) // 2
    
    # Pegar la imagen centrada
    icon.paste(img, (x, y), img)
    
    # Guardar primero como PNG de alta calidad
    icon.save('temp_icon.png', 'PNG')
    
    # Ahora crear las diferentes versiones para el ICO
    sizes = [
        (256, 256),
        (128, 128),
        (64, 64),
        (48, 48),
        (32, 32),
        (16, 16)
    ]
    
    # Lista para almacenar las imágenes
    images = []
    
    # Cargar el PNG temporal que acabamos de crear
    base_img = Image.open('temp_icon.png')
    
    for size in sizes:
        # Crear una nueva imagen con fondo transparente
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        
        # Redimensionar la imagen base
        resized = base_img.resize(size, Image.Resampling.LANCZOS)
        
        # Pegar en el centro
        img.paste(resized, (0, 0), resized)
        
        images.append(img)
    
    # Eliminar el archivo ico si ya existe
    if os.path.exists('icon.ico'):
        os.remove('icon.ico')
    
    # Guardar como ICO
    images[0].save(
        'icon.ico',
        format='ICO',
        sizes=[(img.size[0], img.size[1]) for img in images]
    )
    
    # Limpiar el archivo temporal
    if os.path.exists('temp_icon.png'):
        os.remove('temp_icon.png')
    
    print("Icono creado exitosamente")

if __name__ == '__main__':
    create_icon()
