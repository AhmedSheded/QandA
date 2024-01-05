import requests

api_url = 'https://pyocr-b3169decc152.herokuapp.com//perform_ocr'
image_path = 'test/imgs/4.png'
language = 'm'
data = {'language': language}

with open(image_path, 'rb') as file:
    files = {'image': (image_path, file, 'image/png')}
    response = requests.post(api_url, data=data, files=files)

# Print the response
print(response.status_code)
print(response.json())
