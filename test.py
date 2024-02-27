import requests

image_path = 'test/imgs/4.png'

language = 'm'

# API endpoint URL
# url = 'http://127.0.0.1:5000/ocr'
url = 'http://64.23.164.38:5000/ocr'

files = {'image': open(image_path, 'rb')}
data = {'language': language}

response = requests.post(url, files=files, data=data, timeout=30)

print(response.json())
print(response.status_code)