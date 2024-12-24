from PIL import Image
import os

# Crear directorio de prueba
test_dir = "test_images"
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

# Crear imágenes de prueba
def create_test_image(filename, size=(800, 600), color='white', text=None):
    img = Image.new('RGB', size, color)
    img.save(os.path.join(test_dir, filename))

# Crear diferentes tipos de imágenes
images = [
    ('test1.jpg', 'red'),
    ('test2.PNG', 'blue'),
    ('test3.jpeg', 'green'),
    ('test4.JPG', 'yellow'),
    ('test_large.png', 'purple'),
]

for filename, color in images:
    create_test_image(filename, color=color)

print("Imágenes de prueba creadas en:", test_dir)
