from flask import Flask, request, jsonify
from PIL import Image
from pix2text import Pix2Text, merge_line_texts
import pytesseract
import langid

app = Flask(__name__)


def detect_language(image_path):
    text = pytesseract.image_to_string(Image.open(image_path), lang='eng+ara')
    lang, _ = langid.classify(text)
    return lang


def ocr(image_path, language):
    if language == 'en':
        p2t = Pix2Text(analyzer_config=dict(model_name='mfd'))
        outs = p2t(image_path, resized_shape=608)  # Equal to p2t.recognize()
        result = merge_line_texts(outs, auto_line_break=True)
    elif language == 'ar':
        # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
        img = Image.open(image_path)
        result = pytesseract.image_to_string(img, lang='ara+equ')
    return result

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400

    language = detect_language(image_file)
    text = ocr(image_file, language)
    return jsonify({'text': text})


if __name__ == '__main__':
    app.run(port=5000, debug=False)
