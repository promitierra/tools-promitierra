"""
Script para generar un icono por defecto para la aplicación.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def crear_icono_default():
    """Crea un icono por defecto con las letras 'PT' en un diseño moderno."""
    # Crear una imagen cuadrada
    size = (256, 256)
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Dibujar un círculo de fondo
    margin = 10
    circle_bbox = (margin, margin, size[0] - margin, size[1] - margin)
    draw.ellipse(circle_bbox, fill='#2B5797')
    
    # Agregar texto
    try:
        # Intentar usar una fuente del sistema
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        # Si no está disponible, usar la fuente por defecto
        font = ImageFont.load_default()
    
    text = "PT"
    # Obtener el tamaño del texto
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Centrar el texto
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Dibujar el texto
    draw.text((x, y), text, font=font, fill='white')
    
    # Guardar en diferentes tamaños
    sizes = [16, 32, 48, 64, 128, 256]
    ico_path = Path('build_tools/assets/icon.ico')
    
    # Crear las imágenes en diferentes tamaños
    images = []
    for s in sizes:
        img_copy = image.copy()
        img_copy.thumbnail((s, s), Image.Resampling.LANCZOS)
        images.append(img_copy)
    
    # Guardar como .ico
    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    
    print(f"Icono creado en: {ico_path}")

if __name__ == '__main__':
    crear_icono_default() 