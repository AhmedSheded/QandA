from flask import Flask, request, jsonify
from PIL import Image
from rapid_latex_ocr import LatexOCR
import pytesseract
import io

app = Flask(__name__)
model = LatexOCR()


def ocr(image_data, language):
    if language == 'm':
        res, elapse = model(image_data)
        result = res
    elif language == 'l':
        img = Image.open(io.BytesIO(image_data))
        result = pytesseract.image_to_string(img, lang='ara+eng')
    else:
        return 'bad request'
    return result


@app.route('/perform_ocr', methods=['POST'])
def perform_ocr():
    language = request.form.get('language')

    if 'image' not in request.files:
        return 'No image provided in the request'

    image = request.files['image']

    # Ensure the uploaded file is an image
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in image.filename or image.filename.split('.')[-1].lower() not in allowed_extensions:
        return 'Invalid image file'

    # Read the image data
    image_data = image.read()

    result = ocr(image_data, language)
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
