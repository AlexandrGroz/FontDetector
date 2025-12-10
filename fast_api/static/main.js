let currentImage = null;

async function processImage(formData) {
    const response = await fetch('/predict/', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    console.log(result);
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = "";

    result.font_data.forEach((fontInfo) => {
        const fontDiv = document.createElement('div');
        fontDiv.innerHTML = `<img src="data:image/png;base64,${fontInfo.imageBase64}">
                         <p>${fontInfo.label}</p>`;
        resultsDiv.appendChild(fontDiv);
    });
}

async function showImagePreview(imageFile) {
    const reader = new FileReader();
    reader.onload = function (e) {
        const imagePreview = document.getElementById('imagePreview');
        imagePreview.src = e.target.result;
        currentImage = imageFile;
    }
    reader.readAsDataURL(imageFile);
}

async function predictFont() {
    const imageUpload = document.getElementById('imageUpload').files[0];
    showImagePreview(imageUpload);
}

async function sendToServer() {
    if (currentImage) {
        const formData = new FormData();
        formData.append('image', currentImage);
        await processImage(formData);
    }
}

document.addEventListener('paste', async function (e) {
    const clipboardData = e.clipboardData || window.clipboardData;
    if (!clipboardData) {
        return;
    }

    const items = clipboardData.items;

    for (const item of items) {
        if (item.kind === 'file' && item.type.startsWith('image/')) {
            const blob = item.getAsFile();
            showImagePreview(blob);
            break;
        }
    }
});

document.getElementById('imageUpload').addEventListener('change', function() {
  if (this.files && this.files[0]) {
    showImagePreview(this.files[0]);
  }
});
