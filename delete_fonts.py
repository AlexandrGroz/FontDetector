from fontTools.ttLib import TTFont
import os

font_dir = 'downloaded_fonts'


def check_cyrillic_support(font_path):
    font = TTFont(font_path)
    for table in font['cmap'].tables:
        for code in range(0x0410, 0x044F):
            if table.isUnicode() and table.cmap.get(code):
                return True
    return False


def check_latin_support(font_path):
    font = TTFont(font_path)
    for table in font['cmap'].tables:
        for code in range(0x0041, 0x007A):
            if table.isUnicode() and table.cmap.get(code):
                return True
    return False


for font_file in os.listdir(font_dir):
    if not font_file.endswith('.ttf') and not font_file.endswith('.otf'):
        continue

    full_font_path = f"{font_dir}/{font_file}"

    if not check_cyrillic_support(full_font_path) or not check_latin_support(full_font_path):
        print(f"Deleting {font_file}")
        os.remove(full_font_path)
