import requests
from bs4 import BeautifulSoup
import time

base_url = "https://fonts.mega8.ru/"
download_url_template = "download.php?font="
info_url_template = "index.php?font="

total_fonts = 8613

output_folder = "downloaded_fonts2/"

names_file = "font_names.txt"

with open(names_file, "a", encoding="utf-8") as name_f:
    for i in range(1, total_fonts + 1):
        for attempt in range(30):
            try:
                info_url = f"{base_url}{info_url_template}{i}"
                response = requests.get(info_url)

                if response.status_code != 200:
                    print(f"Attempt {attempt + 1}: Failed to get info for font {i}")
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string

                font_name = " ".join(title.split(" ")[1:3])

                name_f.write(f"{i}: {font_name}\n")

                download_url = f"{base_url}{download_url_template}{i}"

                headers = {
                    'Referer': 'https://fonts.mega8.ru/index.php',
                }
                response = requests.get(download_url, headers=headers)

                if response.status_code == 200:
                    with open(f"{output_folder}{i}.ttf", "wb") as f:
                        f.write(response.content)
                    print(f"Successfully downloaded {font_name} id {i}")
                    break
                else:
                    print(f"Attempt {attempt + 1}: Failed to download {font_name}")
            except Exception as e:
                print(f"Attempt {attempt + 1} failed due to an error: {e}")

        time.sleep(1)
