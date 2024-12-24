from PIL import Image, ImageDraw
import os

def create_icon():
    # Crear una imagen base con fondo transparente
    size = (256, 256)
    icon = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Colores
    azul = (33, 150, 243)  # Material Blue
    blanco = (255, 255, 255)
    
    # Dibujar un círculo azul como fondo
    padding = 20
    circle_bbox = (padding, padding, size[0]-padding, size[1]-padding)
    draw.ellipse(circle_bbox, fill=azul)
    
    # Dibujar el símbolo de imagen (un rectángulo con una montaña)
    margin = 60
    img_box = (margin, margin, size[0]-margin, size[1]-margin)
    draw.rectangle(img_box, fill=blanco)
    
    # Dibujar la "montaña" dentro del rectángulo
    peak_height = margin + (size[1]-2*margin) * 0.3
    mountain_points = [
        (margin, size[1]-margin),  # Esquina inferior izquierda
        (margin + (size[0]-2*margin) * 0.4, peak_height),  # Primer pico
        (margin + (size[0]-2*margin) * 0.7, peak_height + 30),  # Segundo pico
        (size[0]-margin, size[1]-margin)  # Esquina inferior derecha
    ]
    draw.polygon(mountain_points, fill=azul)
    
    # Dibujar el símbolo PDF en la esquina inferior derecha
    pdf_size = 80
    pdf_margin = 40
    pdf_box = (
        size[0] - pdf_size - pdf_margin,
        size[1] - pdf_size - pdf_margin,
        size[0] - pdf_margin,
        size[1] - pdf_margin
    )
    draw.rectangle(pdf_box, fill=azul)
    
    # Texto "PDF" en blanco
    pdf_text_margin = 45
    draw.text(
        (size[0] - pdf_size - pdf_margin + 15, size[1] - pdf_size - pdf_margin + 20),
        "PDF",
        fill=blanco,
        font=None
    )
    
    # Guardar en diferentes tamaños
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []
    
    for s in sizes:
        resized = icon.resize(s, Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Eliminar icono existente si existe
    if os.path.exists('icon.ico'):
        os.remove('icon.ico')
    
    # Guardar como ICO
    icon.save('icon.ico', format='ICO', sizes=sizes)
    print("Icono creado exitosamente")

if __name__ == '__main__':
    create_icon()
