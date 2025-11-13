import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import base64
from io import BytesIO
import cv2
import torch.nn as nn
from PIL import Image as PILImage, ImageDraw, ImageFont
import pickle
import torch
from torchvision import transforms
import numpy as np
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def generate_font_image(text, font_path, image_size=(900, 100)):
    image = PILImage.new('L', image_size, color='black')
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(font_path, 40)
    except IOError:
        return None

    text_bbox = draw.textbbox(text=text, font=font, xy=(0, 0))
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)

    draw.text(position, text, fill='white', font=font)
    return image


class BaseNet(nn.Module):
    def __init__(self):
        super(BaseNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, 3), nn.ReLU(),
            nn.Conv2d(32, 32, 3), nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, 3), nn.ReLU(),
            nn.Conv2d(64, 64, 3), nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, 3), nn.ReLU(),
            nn.Conv2d(128, 128, 3), nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((2, 2)),
            nn.Flatten(),
            nn.Linear(512, 1024), nn.ReLU(),
            nn.Linear(1024, 512), nn.ReLU(),
            nn.Linear(512, 256)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
model_path = os.path.join(parent_directory, 'model.pth')

base_net = BaseNet()
base_net.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
base_net.eval()

embeddings_path = os.path.join(parent_directory, 'test_average_embeddings.pkl')
with open(embeddings_path, 'rb') as f:
    test_average_embeddings = pickle.load(f)


def euclidean_distance(a, b):
    return torch.norm(a - b, p=2)


def predict_top_fonts(embedding, average_embeddings, top_n=3):
    distances = []

    embedding = torch.tensor(embedding) if type(embedding) is not torch.Tensor else embedding

    for label, avg_emb in average_embeddings.items():
        avg_emb = torch.tensor(avg_emb) if type(avg_emb) is not torch.Tensor else avg_emb
        distance = euclidean_distance(embedding, avg_emb)
        distances.append((label, distance.item()))

    distances.sort(key=lambda x: x[1])
    return distances[:top_n]


def predict_font_from_image(image):
    image = cv2.cvtColor(image.astype('uint8'), cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if cv2.countNonZero(image) > (image.shape[0] * image.shape[1] // 2):
        image = cv2.bitwise_not(image)

    image = Image.fromarray(image, 'L')
    transform = transforms.Compose([
        transforms.Resize((100, 300)),
        transforms.ToTensor()
    ])
    image = transform(image)

    image = image.unsqueeze(0)

    embedding = base_net(image).detach().cpu().numpy()

    top5_fonts = predict_top_fonts(embedding, test_average_embeddings, top_n=3)

    font_data = []
    for font_name, font_distance in top5_fonts:
        font_file = font_name.replace(" ", "_") + "_regular.otf"
        font_path = f"{parent_directory}/downloaded_fonts/{font_file}"
        print(font_path)
        font_image = generate_font_image("АБВГД абвгд 12345", font_path)
        if font_image:
            font_data.append(font_image)
            font_data.append(f"{font_name} (Дистанция: {font_distance:.2f})")

    return tuple(font_data)


@app.get("/")
def read_root():
    return FileResponse("index.html")


@app.post("/predict/")
async def predict(image: UploadFile = File(...)):
    image_contents = await image.read()
    pil_image = Image.open(BytesIO(image_contents)).convert("RGB")

    font_data = predict_font_from_image(np.array(pil_image))
    results = []
    for image, label in zip(font_data[::2], font_data[1::2]):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode()
        results.append({"imageBase64": image_base64, "label": label})
    return JSONResponse(content={"font_data": results})
