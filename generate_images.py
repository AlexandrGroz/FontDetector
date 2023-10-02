from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
import string
import numpy as np


def random_string(length=30):
    letters = string.ascii_letters + string.digits + ' ' * 10
    cyrillic_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'.upper()
    letters += cyrillic_letters
    return ''.join(random.choice(letters) for i in range(length)).strip()


def add_gaussian_noise(image, noise_level):
    np_image = np.array(image)
    noise = np.random.normal(0, noise_level, np_image.shape).astype(np.uint8)
    noisy_image = np_image + noise
    noisy_image = np.clip(noisy_image, 0, 255)
    return Image.fromarray(noisy_image, 'RGBA')


def random_contrast_color(base_color):
    r, g, b = base_color
    return 255 - r, 255 - g, 255 - b


font_dir = 'downloaded_fonts'

output_dir = 'generated_images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

random_phrases = [random_string(random.randint(5, 20)) for _ in range(300)]

for font_file in os.listdir(font_dir):
    if not font_file.endswith('.ttf') and not font_file.endswith('.otf'):
        continue
    print(font_file)
    try:
        font_path = os.path.join(font_dir, font_file)
        font = ImageFont.truetype(font_path, 60)
    except Exception as e:
        print(f"Could not load font {font_file}: {e}")
        continue
    for phrase in random_phrases:
        phrase = random_string(random.randint(5, 20))
        try:
            bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            text_color = random_contrast_color(bg_color)
            image = Image.new("RGBA", (300, 100), bg_color)
            draw = ImageDraw.Draw(image)
            text_bbox = draw.textbbox(text=phrase, font=font, xy=(0, 0))
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            while text_width > 290:
                phrase = phrase[:-1]
                text_bbox = draw.textbbox(text=phrase, font=font, xy=(0, 0))
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

            x = (image.width - text_width) // 2
            y = (image.height - text_height) // 2
            draw.text((x, y), phrase, font=font, fill=text_color)
            if random.choice([True, False]):
                image = image.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 1.5)))

            image_filename = f"{phrase}_{font_file.split('.')[0]}.png"
            image_path = os.path.join(output_dir, image_filename)
            image.save(image_path)
        except Exception as e:
            print(f"An error occurred while processing the phrase '{phrase}' with font {font_file}: {e}")
            continue
