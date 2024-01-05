import requests

# Replace with the actual file path to your image
image_path = 'test/imgs/4.png'

# Replace with the desired language ('m' or 'l')
language = 'm'

# API endpoint URL
# url = 'http://127.0.0.1:5001/ocr'
url = ' https://pyocr-b3169decc152.herokuapp.com/ocr'

# Prepare the payload
files = {'image': open(image_path, 'rb')}
data = {'language': language}

# Send the POST request
response = requests.post(url, files=files, data=data, timeout=30)

# Print the response
print(response.json())
