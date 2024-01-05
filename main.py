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


@app.route('/ocr', methods=['POST'])
def ocr_endpoint():
    try:
        # Get the language and image data from the request
        language = request.form.get('language')
        image_file = request.files['image']

        # Read the image data
        image_data = image_file.read()

        # Call the ocr function
        result = ocr(image_data, language)

        # Return the OCR result as JSON
        return jsonify({'result': result, 'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
