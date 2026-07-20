---
title: Predictive Waste Analytics
emoji: 🚛
colorFrom: green
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

# 🚛 Aeterna AI: Next-Gen Waste Intelligence Platform DKI Jakarta

<p align="center">
  <a href="https://www.aeternaai.biz.id/"><img src="https://img.shields.io/badge/Official%20Portal-aeternaai.biz.id-00f2fe?style=for-the-badge&logo=googlechrome" alt="Official Website" /></a>
  <a href="https://www.linkedin.com/in/faril-putra-pratama-81561a280/"><img src="https://img.shields.io/badge/LinkedIn-Faril%20Putra%20Pratama-0a66c2?style=for-the-badge&logo=linkedin" alt="LinkedIn Profile" /></a>
  <a href="https://github.com/FARILtau72/Aeterna-Ai"><img src="https://img.shields.io/badge/GitHub-FARILtau72-181717?style=for-the-badge&logo=github" alt="GitHub Badge" /></a>
  <a href="https://github.com/FARILtau72/Aeterna-Ai/stargazers"><img src="https://img.shields.io/github/stars/FARILtau72/Aeterna-Ai?style=for-the-badge&color=gold" alt="GitHub Stars" /></a>
  <a href="https://scikit-learn.org/"><img src="https://img.shields.io/badge/GBR%20Accuracy-R%C2%B2%2098.28%25-brightgreen?style=for-the-badge&logo=scikitlearn" alt="Scikit-Learn" /></a>
</p>

> ⭐ **If you find Aeterna AI useful, please give this repository a Star on GitHub! Your support helps boost open-source smart city innovation!**

---

### 👨‍💻 Lead Developer: Faril Putra Pratama
* **Official Website Portal**: [https://www.aeternaai.biz.id/](https://www.aeternaai.biz.id/)
* **LinkedIn Profile**: [https://www.linkedin.com/in/faril-putra-pratama-81561a280/](https://www.linkedin.com/in/faril-putra-pratama-81561a280/)
* **GitHub Repository**: [https://github.com/FARILtau72/Aeterna-Ai](https://github.com/FARILtau72/Aeterna-Ai)
* **Live HF Deployment**: [https://huggingface.co/spaces/ALAMDIENG/waste-prediction-api](https://huggingface.co/spaces/ALAMDIENG/waste-prediction-api)

**Platform Sistem Peringatan Dini & Peramalan Sampah Real-Time 44 Kecamatan DKI Jakarta berbasis BPS Jumlah Jiwa, Open-Meteo, & AI Chronos T5.**

---

## 📖 Overview

**Aeterna AI** adalah platform analitik kecerdasan buatan (*Waste Intelligence System*) yang dirancang dan dikembangkan oleh **Faril Putra Pratama (@FARILtau72)**. Platform ini dirancang untuk memantau, memprediksi, dan mengoptimalkan manajemen logistik armada truk sampah DKI Jakarta secara spasial-temporal harian untuk seluruh **44 Kecamatan**.

Platform ini mengubah paradigma pengelolaan sampah dari **reaktif** (menangani setelah terjadi penumpukan) menjadi **prediktif** (memprediksi surge sebelum terjadi) guna mengoptimalkan penyebaran armada truk pengangkut ke 44 kecamatan DKI Jakarta.

> [!NOTE]
> **📖 DOKUMENTASI SISTEM BACKEND MENDALAM**:  
> Untuk rincian mendalam mengenai arsitektur backend, model machine learning (GBR R²=98.28% & Chronos T5), metrik akurasi, formula rekayasa fitur cuaca/event, dan deployment Docker, silakan merujuk ke **[BACKEND_DOC.md](BACKEND_DOC.md)**.

---

## 🌟 Fitur Unggulan (Key Features)

1. **BPS Jumlah Jiwa Headcount Scaling Engine**: Mengintegrasikan data populasi resmi BPS DKI Jakarta 2023/2024 untuk seluruh 44 Kecamatan (Cengkareng 592rb, Cakung 559rb, Menteng 88rb, dll.) untuk mengukur lonjakan tonase sampah secara fisik.
2. **AI Autopilot Forecaster**: Sistem otonom yang mengevaluasi seluruh **44 Kecamatan DKI Jakarta** secara paralel berdasarkan curah hujan koordinat presisi (Open-Meteo) dan kalender event aktif 2026.
3. **6-Kategori Komposisi Sampah**: Memprediksi rincian tonase sampah secara proporsional sesuai statistik riil DLH DKI Jakarta: *Sisa Makanan (~50.2%), Plastik (~22.8%), Kertas (~11.5%), Tekstil (~4.2%), Kaca (~3.2%), dan Logam/Lainnya (~8.1%)*.
4. **Armada Truk Compactor (8-Ton Divisor)**: Menghitung alokasi armada truk sampah secara presisi berdasarkan standar armada DLH DKI Jakarta (8 Ton per truk).
5. **Interactive Cyber HUD UI**: Antarmuka bertema *Dark Glassmorphism* dengan kursor delay kustom, visualisasi progress bar kategori neon glow, rincian logistik armada truk, dan rute logistik ke TPST Bantargebang.

---

## 🏗️ Arsitektur Sistem (Single-Container Full-Stack Architecture)

Sistem ini didesain menggunakan arsitektur full-stack terpadu berbasis **Python FastAPI & Vanilla JavaScript** yang ringan, cepat, dan hemat memori:

```
+---------------------------------------------------------------------------------------------------+
|                                 AETERNA AI PLATFORM CONTAINER                                     |
|                             (Hosted on Hugging Face Spaces & Docker)                              |
|                                                                                                   |
|   +---------------------------------------+     +---------------------------------------------+   |
|   |         CYBER HUD DASHBOARD UI        |     |             FASTAPI BACKEND ENGINE          |   |
|   | (HTML5, Vanilla CSS3, Leaflet.js Map) | <-> |    (Async REST Endpoints & Web Controller)   |   |
|   +---------------------------------------+     +---------------------------------------------+   |
|                                                                |                                  |
|                                         +----------------------+----------------------+           |
|                                         |                                             |           |
|                                         v                                             v           |
|                         +-------------------------------+             +-------------------------------+
|                         |    AMAZON CHRONOS-T5 (TINY)   |             |   GRADIENT BOOSTING REGRESSOR |
|                         | (Time-Series Neural Network)  |             |     (GBR R²=98.28%, MAPE=1.72%) |
|                         +-------------------------------+             +-------------------------------+
|                                         |                                             |           |
|                                         +----------------------+----------------------+           |
|                                                                |                                  |
|                                                                v                                  |
|                                             +-------------------------------------+               |
|                                             |         EXTERNAL DATA SYNC          |               |
|                                             |  - BPS Jakarta 2024 (Jumlah Jiwa)   |               |
|                                             |  - Open-Meteo Realtime Rainfall API |               |
|                                             +-------------------------------------+               |
+---------------------------------------------------------------------------------------------------+
```

### Component Stack:
* **Frontend Layer**: HTML5, Vanilla CSS3 (*Dark Glassmorphism Theme*), Vanilla JavaScript ES6+, dan **Leaflet.js** untuk visualisasi peta spasial 44 Kecamatan DKI Jakarta.
* **Backend Layer**: **Python 3.9+** & **FastAPI** dengan Uvicorn ASGI Server untuk eksekusi peramalan REST API berkecepatan tinggi.
* **AI & Machine Learning Engine**: **Amazon Chronos-T5 (Tiny)** (PyTorch) & **Gradient Boosting Regressor** (Scikit-Learn, fine-tuned dengan GridSearchCV).
* **Data Providers**: Data Populasi **BPS DKI Jakarta 2023/2024** (Jumlah Jiwa), **Open-Meteo Weather API** (Curah Hujan Real-Time), dan **Dinas Lingkungan Hidup DKI Jakarta**.

---

## 📊 Hasil Evaluasi & Akurasi Model GBR

Model Gradient Boosting Regressor (GBR) dilatih dengan **GridSearchCV** di atas dataset teraugmentasi DLH Jakarta dengan rata-rata timbulan **8.020 Ton/hari**.

| Metrik Evaluasi | Model Baseline | Model Upgraded (Aeterna AI) | Status Performa |
| :--- | :---: | :---: | :--- |
| **Mean Absolute Error (MAE)** | `149.13 Ton` | **`14.20 Ton`** | Sangat Presisi (Turun ⬇️) |
| **Root Mean Squared Error (RMSE)** | `188.46 Ton` | **`18.50 Ton`** | Sangat Presisi (Turun ⬇️) |
| **R-Squared ($R^2$ Score)** | `76.02%` | **`98.28%`** | Performa Puncak (Naik ⬆️) |
| **Mean Absolute Percentage Error (MAPE)** | `1.78%` | **`1.72%`** | **Sangat Akurat (< 2%) (⬇️)** |

---

## 📡 Referensi Endpoint API Utama

Semua endpoint didukung dengan dokumentasi interaktif Swagger UI di `/docs`.

### 1. Predict Waste Volume (Forecasting)
* **Method**: `POST`
* **Endpoint**: `/api/v1/predict`
* **Request Payload**:
    ```json
    {
      "forecast_days": 7,
      "rainfall_mm": 0.0,
      "jumlah_jiwa": 120000,
      "location": "Menteng",
      "model_type": "gradient_boosting",
      "granularity": "daily"
    }
    ```

### 2. Autopilot Live DKI (Today)
* **Method**: `GET`
* **Endpoint**: `/api/v1/autopilot`
* **Description**: Mengembalikan kalkulasi prediksi otonom hari ini untuk seluruh 44 kecamatan DKI Jakarta secara paralel lengkap dengan data koordinat lokasi.

### 3. SEO & GEO Endpoints
* `GET /robots.txt`: Izin crawler AI (GPTBot, ClaudeBot, PerplexityBot).
* `GET /sitemap.xml`: XML Sitemap untuk indeks Googlebot.
* `GET /llms.txt` & `/llms-full.txt`: Spesifikasi RAG citation untuk AI LLM.

---

## 🛠️ Panduan Instalasi & Pengembangan Lokal

```bash
# Clone repository
git clone https://github.com/FARILtau72/Aeterna-Ai.git
cd Aeterna-Ai

# Install dependencies
pip install -r requirements.txt

# Jalankan server FastAPI lokal
python -m uvicorn app:app --port 8001 --host 127.0.0.1
```
* Akses UI di: `http://localhost:8001`
* Akses Swagger UI di: `http://localhost:8001/docs`

---

## 👤 Developer & Legal License

Developed & Engineered with ⚡ by **[Faril Putra Pratama (@FARILtau72)](https://github.com/FARILtau72)**.  
Distributed under the **MIT License**.


*   **FARIL PUTRA PRATAMA** (Lead Full-Stack AI Engineer) — *SMK Taruna Bangsa*
    *   *Portofolio Kontribusi*: Merancang dan melatih model GBR (MAPE 1.59%), mengintegrasikan API Open-Meteo, merancang arsitektur backend, dan membangun antarmuka visual Cyber HUD interaktif.
