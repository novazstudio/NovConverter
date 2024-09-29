from flask import Flask, request, render_template, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/convert', methods=['POST'])
def convert():
    # Obtener las imágenes y otros parámetros
    images = request.files.getlist('image')
    output_format = request.form.get('format')
    quality = int(request.form.get('quality', 80))
    width = request.form.get('width')
    height = request.form.get('height')
    filter_type = request.form.get('filter')

    # Procesar la primera imagen solamente
    image_file = images[0]  # Para simplificar, puedes manejar múltiples imágenes más adelante
    img = Image.open(image_file)

    # Aplicar el filtro si se ha seleccionado uno
    if filter_type == 'grayscale':
        img = img.convert('L')  # Convertir a escala de grises
    elif filter_type == 'sepia':
        img = img.convert('RGB')  # Asegurarse de que la imagen esté en modo RGB
        pixels = img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                r, g, b = pixels[i, j]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                # Asegurarse de que los valores están en el rango correcto
                pixels[i, j] = (min(tr, 255), min(tg, 255), min(tb, 255))
    elif filter_type == 'invert':
        img = img.convert('RGB')  # Asegurarse de que la imagen esté en modo RGB
        img = Image.eval(img, lambda x: 255 - x)  # Invertir colores

    # Redimensionar si se especifica
    if width and height:
        img = img.resize((int(width), int(height)), Image.LANCZOS)

    # Guardar la imagen en memoria en el formato deseado
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=output_format, quality=quality)
    img_byte_arr.seek(0)

    # Cambiar el nombre del archivo para que tenga la extensión correcta
    filename = f"converted_image.{output_format}"

    # Devolver la imagen convertida para descargar
    return send_file(img_byte_arr, mimetype=f'image/{output_format}', as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)