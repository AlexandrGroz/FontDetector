let currentImage = null;

const uploadInput = document.getElementById('imageUpload');
const dropZone = document.getElementById('dropZone');
const statusText = document.getElementById('statusText');
const predictButton = document.getElementById('predictButton');
const resultsGrid = document.getElementById('results');
const previewImage = document.getElementById('imagePreview');
const resultsCount = document.getElementById('resultsCount');

function setStatus(message, tone = 'muted') {
    statusText.textContent = message;
    statusText.className = `status ${tone}`;
}

function setLoading(isLoading) {
    predictButton.disabled = isLoading;
    predictButton.textContent = isLoading ? 'Поиск шрифтов…' : 'Определить шрифт';
    predictButton.classList.toggle('loading', isLoading);
}

function renderResults(fontData) {
    resultsGrid.innerHTML = '';
    const total = fontData?.length || 0;
    resultsCount.textContent = total ? `Top ${total}` : 'Нет результатов';

    if (!fontData || fontData.length === 0) {
        const emptyState = document.createElement('p');
        emptyState.className = 'muted';
        emptyState.textContent = 'Нет результатов. Загрузите изображение с текстом, чтобы найти похожие шрифты.';
        resultsGrid.appendChild(emptyState);
        return;
    }

    fontData.forEach((fontInfo) => {
        const card = document.createElement('article');
        card.className = 'font-card';

        const preview = document.createElement('div');
        preview.className = 'font-preview';
        preview.innerHTML = `<img src="data:image/png;base64,${fontInfo.imageBase64}" alt="Предпросмотр шрифта">`;

        const label = document.createElement('p');
        label.className = 'font-label';
        label.textContent = fontInfo.label;

        card.appendChild(preview);
        card.appendChild(label);
        resultsGrid.appendChild(card);
    });
}

async function processImage(formData) {
    setLoading(true);
    setStatus('Ищем похожие шрифты…', 'info');

    try {
        const response = await fetch('/predict/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Запрос не выполнен');
        }

        const result = await response.json();
        renderResults(result.font_data);
        setStatus('Готово! Попробуйте другое изображение для новых результатов.', 'success');
    } catch (error) {
        console.error(error);
        setStatus('Не удалось определить шрифт. Попробуйте еще раз.', 'error');
    } finally {
        setLoading(false);
    }
}

function showImagePreview(imageFile) {
    const reader = new FileReader();
    reader.onload = function (e) {
        previewImage.src = e.target.result;
        previewImage.classList.add('visible');
        currentImage = imageFile;
        setStatus('Изображение загружено. Нажмите "Определить шрифт".', 'info');
    };
    reader.readAsDataURL(imageFile);
}

function handleFileSelection(file) {
    if (!file || !file.type.startsWith('image/')) {
        setStatus('Пожалуйста, выберите файл изображения.', 'warn');
        return;
    }
    showImagePreview(file);
}

async function sendToServer() {
    if (!currentImage) {
        setStatus('Сначала загрузите изображение со шрифтом.', 'warn');
        return;
    }

    const formData = new FormData();
    formData.append('image', currentImage);
    await processImage(formData);
}

document.addEventListener('paste', function (e) {
    const clipboardData = e.clipboardData || window.clipboardData;
    if (!clipboardData) return;

    for (const item of clipboardData.items) {
        if (item.kind === 'file' && item.type.startsWith('image/')) {
            const blob = item.getAsFile();
            handleFileSelection(blob);
            break;
        }
    }
});

uploadInput.addEventListener('change', function() {
    if (this.files && this.files[0]) {
        handleFileSelection(this.files[0]);
    }
});

dropZone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropZone.classList.add('dragging');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragging');
});

dropZone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropZone.classList.remove('dragging');
    const file = event.dataTransfer.files[0];
    handleFileSelection(file);
});

dropZone.addEventListener('click', () => uploadInput.click());
predictButton.addEventListener('click', sendToServer);

renderResults([]);
