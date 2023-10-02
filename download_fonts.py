import requests
import os
import time
from settings import GOOGLE_FONTS_API_KEY

API_KEY = GOOGLE_FONTS_API_KEY
FONT_LIST_URL = 'https://www.googleapis.com/webfonts/v1/webfonts'
DOWNLOAD_DIR = 'downloaded_fonts'
MAX_RETRIES = 60


def get_font_list(api_key):
    params = {
        'key': api_key,
        'sort': 'popularity'
    }
    response = requests.get(FONT_LIST_URL, params=params)
    if response.status_code != 200:
        raise ValueError("Error fetching font list from Google Fonts API.")
    return response.json().get('items', [])


def download_font_file(url, filename):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(os.path.join(DOWNLOAD_DIR, filename), 'wb') as file:
                file.write(response.content)
            print(f"Successfully downloaded {filename}")
            return
        except requests.RequestException as e:
            print(f"Error downloading {filename}: {e}. Retrying...")
            retries += 1
            time.sleep(2)
    print(f"Failed to download {filename} after {MAX_RETRIES} retries.")


if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    fonts = get_font_list(API_KEY)
    i = 0
    for font in fonts:
        if "latin-ext" not in font['subsets'] or "cyrillic-ext" not in font['subsets']:
            continue
        print(font['subsets'], i)
        url = font['files'].get('regular', None)
        if url and font['subsets']:
            file_extension = url.split('.')[-1]
            filename = f"{font['family'].replace(' ', '_')}_Regular.{file_extension}"
            download_font_file(url, filename)
        i += 1
