from PIL import Image
import requests
from io import BytesIO
import os


def compress_image(image_url, output_path):
    # Download the image
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # Compress the image by 50%
    image.save(output_path, quality=50)


def process_images(input_urls, output_dir):
    output_urls = []
    for i, url in enumerate(input_urls):
        output_path = os.path.join(output_dir, f"output_{i}.jpg")
        compress_image(url, output_path)
        output_urls.append(output_path)
    return output_urls
