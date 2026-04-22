// API URL
const API_URL = 'http://localhost:5000';

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const uncertain = document.getElementById('uncertain');
const result = document.getElementById('result');
const resetBtn = document.getElementById('resetBtn');

// Event Listeners
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', handleDragOver);
dropZone.addEventListener('dragleave', handleDragLeave);
dropZone.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
resetBtn.addEventListener('click', resetApp);

function handleDragOver(e) {
    e.preventDefault();
    dropZone.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    dropZone.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        processImage(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        processImage(files[0]);
    }
}

function processImage(file) {
    // Validasi file
    if (!file.type.startsWith('image/')) {
        showError('File harus berupa gambar (JPG, PNG, JPEG)');
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
        showError('Ukuran file maksimal 5MB');
        return;
    }
    
    // UI state
    hideAllSections();
    loading.classList.remove('hidden');
    
    // Kirim ke API
    const formData = new FormData();
    formData.append('image', file);
    
    fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loading.classList.add('hidden');
        
        if (data.status === 'error') {
            showError(data.message, data.tip);
        } else if (data.status === 'uncertain') {
            showUncertain(data);
        } else if (data.status === 'success') {
            showResult(data, file);
        }
    })
    .catch(err => {
        loading.classList.add('hidden');
        showError('Gagal terhubung ke server. Pastikan backend berjalan di http://localhost:5000');
        console.error(err);
    });
}

function showError(message, tip = '') {
    hideAllSections();
    error.classList.remove('hidden');
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorTip').textContent = tip || '';
    resetBtn.classList.remove('hidden');
}

function showUncertain(data) {
    hideAllSections();
    uncertain.classList.remove('hidden');
    document.getElementById('uncertainMessage').textContent = 
        `${data.message} (Confidence: ${(data.confidence * 100).toFixed(2)}%)`;
    
    // Show probabilities
    const probsDiv = document.getElementById('uncertainProbs');
    probsDiv.innerHTML = '<h4>Probabilitas:</h4>';
    
    for (const [cls, prob] of Object.entries(data.all_probabilities)) {
        const percent = (prob * 100).toFixed(2);
        probsDiv.innerHTML += `<p>${cls}: ${percent}%</p>`;
    }
    
    resetBtn.classList.remove('hidden');
}

function showResult(data, file) {
    hideAllSections();
    result.classList.remove('hidden');
    resetBtn.classList.remove('hidden');
    
    // Header
    document.getElementById('className').textContent = data.class_name;
    document.getElementById('confidenceValue').textContent = 
        `${(data.confidence * 100).toFixed(2)}%`;
    
    // Gambar
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('resultImage').src = e.target.result;
    };
    reader.readAsDataURL(file);
    
    // Deskripsi
    document.getElementById('description').textContent = data.description;
    
    // Causes
    const causesList = document.getElementById('causes');
    causesList.innerHTML = data.causes.map(c => `<li>${c}</li>`).join('');
    
    // Solutions
    const solutionsList = document.getElementById('solutions');
    solutionsList.innerHTML = data.solutions.map(s => `<li>${s}</li>`).join('');
    
    // Ingredients
    document.getElementById('ingredients').textContent = data.ingredients.join(', ');
    
    // Products
    const productsDiv = document.getElementById('products');
    productsDiv.innerHTML = data.products.map(p => `
        <div class="product-item">
            <h4>${p.name}</h4>
            <p class="price">${p.price}</p>
            <a href="${p.link}" target="_blank">🔗 Beli di Tokopedia</a>
        </div>
    `).join('');
    
    // Warning
    if (data.warning) {
        document.getElementById('warning').classList.remove('hidden');
        document.getElementById('warningText').textContent = data.warning;
    } else {
        document.getElementById('warning').classList.add('hidden');
    }
    
    // Probabilities bar chart
    const probsDiv = document.getElementById('probabilities');
    probsDiv.innerHTML = '';
    
    const sortedProbs = Object.entries(data.all_probabilities)
        .sort((a, b) => b[1] - a[1]);
    
    for (const [cls, prob] of sortedProbs) {
        const percent = (prob * 100).toFixed(2);
        probsDiv.innerHTML += `
            <div class="prob-bar">
                <div class="prob-label">
                    <span>${cls}</span>
                    <span>${percent}%</span>
                </div>
                <div class="prob-track">
                    <div class="prob-fill" style="width: ${percent}%">
                        ${percent > 20 ? percent + '%' : ''}
                    </div>
                </div>
            </div>
        `;
    }
}

function hideAllSections() {
    loading.classList.add('hidden');
    error.classList.add('hidden');
    uncertain.classList.add('hidden');
    result.classList.add('hidden');
    resetBtn.classList.add('hidden');
}

function resetApp() {
    hideAllSections();
    fileInput.value = '';
    dropZone.classList.remove('hidden');
}

// Cek health saat load
fetch(`${API_URL}/health`)
    .then(r => r.json())
    .then(data => {
        console.log('API Status:', data);
    })
    .catch(err => {
        console.error('API tidak tersedia:', err);
    });