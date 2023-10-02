# Font-Detecitve

Реализация сервиса подобного WhatTheFont.

В отличие от DeepFont (рис. ниже), на последнем слое вместо классификации используется слой эмбеддингов, а сеть обучается с помощью triplet loss

![схема нейросети](https://github.com/robinreni96/Font_Recognition-DeepFont/raw/master/util_image/network.png)

# Датасет
Пример данных из датасета

| ![Изображение 1](https://cdn.discordapp.com/attachments/1050464028440416379/1158447339489468466/00FsK_Ysabeau_Office_Regular.png?ex=651c47a8&is=651af628&hm=175c1351e83f733d3cd6bfb3b024e3b3a3873c9bd045163b9db17dbb7aa486c4&) | ![Изображение 2](https://cdn.discordapp.com/attachments/1050464028440416379/1158447349782294559/0_59_Rubik_80s_Fade_Regular.png?ex=651c47ab&is=651af62b&hm=5c436b7c9020e81c7e1905747650abde748f4169111fdc23c2f9b436bb4d697e&) | ![Изображение 3](https://cdn.discordapp.com/attachments/1050464028440416379/1158447363489284176/0_N0_IBM_Plex_Sans_Regular.png?ex=651c47ae&is=651af62e&hm=f09196b2e5140d343b847945a3e7f7f99096e3fdf85e4ae0ed397637fbe9d1c0&) |
|--------------------------------------------|-----------------------------------------|--------------------------------------------|
| 0 бNщ0Кл_IBM_Plex_Sans_Regular.png                   | 0  5ИА9о_Rubik_80s_Fade_Regular.png                | 00FsKц_Ysabeau_Office_Regular.png                   |


# Установка
```bash
pip install -r requirements.txt
```

# Запуск сервиса
```bash
cd fast_api
uvicorn app:app --reload
```

