from flask import Flask, request, jsonify
from PIL import Image
# from rapid_latex_ocr import LatexOCR
from texify.inference import batch_inference
from texify.model.model import load_model
from texify.model.processor import load_processor
import pytesseract
import io
import os
import matplotlib
matplotlib.use('agg')

app = Flask(__name__)

# model = LatexOCR()

# Set Tesseract command
pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
model = load_model()
processor = load_processor()

def ocr(image_data, language):
    if language == 'm':
        # res, elapse = model(image_data)
        # result = res
        img = Image.open(io.BytesIO(image_data))  # Your image name here
        result = ' '.join(batch_inference([img], model, processor))
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
        result = ''
        result += ocr(image_data, language)

        # Return the OCR result as JSON
        return jsonify({'result': result, 'status': 'success'})
    except FileNotFoundError as e:
        return jsonify({'status': 'error', 'message': f'File not found: {str(e)}'})
    except TimeoutError:
        return jsonify({'status': 'error', 'message': 'Request timed out'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=port)
