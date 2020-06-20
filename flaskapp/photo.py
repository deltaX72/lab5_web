import base64
import io
from PIL import Image, ImageEnhance
import numpy as np

def resize_image(image, coefficient):
    h, w = image.size
    resized_image = image.resize((int(h * coefficient), int(w * coefficient)))
    return resized_image

def convert_to_rgb(base64_string):
    data = base64.b64decode(str(base64_string))
    filename = f'static/result.jpg' 
    with open(filename, 'wb') as f:
        f.write(data)
