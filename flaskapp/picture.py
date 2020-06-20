import base64
import io
from PIL import Image
import numpy as np

def resize_image(image, coefficient):
    h, w = image.size
    resized_image = image.resize((int(h * coefficient), int(w * coefficient)))
    return resized_image

def convert_to_rgb(base64_string):
    with open('static/img.jpg', 'wb') as f:
        f.write(base64.b64decode(str(base64_string)))
