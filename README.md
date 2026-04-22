# 🧠 Acne Detection Project

Project ini adalah sistem **deteksi jerawat (acne detection)** menggunakan model Deep Learning (CNN) dengan format `.keras`.

---

## 🚀 Fitur
- Deteksi jerawat dari gambar
- Model deep learning (CNN)
- Support inference lokal
- Model disimpan menggunakan **Git LFS**

---

## 📦 Tech Stack
- Python 3.x
- TensorFlow / Keras
- OpenCV
- NumPy

---

## ⚠️ Penting (WAJIB DIBACA)
Project ini menggunakan **Git LFS** karena ukuran model besar (>100MB).

👉 Jadi sebelum clone, **HARUS install Git LFS dulu**

---

## 🛠️ Cara Setup Project

### 1. Install Git LFS
Download dan install dari:
https://git-lfs.com/

Lalu jalankan:

git lfs install

---

### 2. Clone Repository

git clone https://github.com/bssd874/Acne_Detection_Project.git
cd Acne_Detection_Project

---

### 3. Install Dependencies

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt

---

### 4. Download Model (WAJIB)

git lfs pull

---

## ▶️ Cara Menjalankan Project

python main.py

atau

python inference.py

---

## 📁 Struktur Folder

Acne_Detection_Project/
│
├── backend/
│   ├── model/
│   │   ├── acne_model_best_1.keras
│   │   ├── acne_model_best_2.keras
│   ├── utils/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── requirements.txt
└── README.md

---

## 🧪 Contoh Load Model

from tensorflow.keras.models import load_model

model = load_model("backend/model/acne_model_best_1.keras")

---

## ❌ Error yang Sering Terjadi

Model tidak bisa dibuka:
OSError: Unable to open file

Solusi:
git lfs pull

---

Module tidak ditemukan:
ModuleNotFoundError

Solusi:
pip install -r requirements.txt

---

## 📌 Catatan
- Jangan upload model tanpa Git LFS
- Jangan commit folder venv
- Gunakan .gitignore yang sudah disediakan

---

## 👨‍💻 Author
Boni Steven
