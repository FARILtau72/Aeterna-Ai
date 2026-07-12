---
title: Predictive Waste Analytics
emoji: 🚛
colorFrom: green
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

# 🚛 Aeterna AI: Next-Gen Waste Intelligence Platform
**Platform Sistem Peringatan Dini & Peramalan Sampah Real-Time DKI Jakarta**

Aeterna AI (sebelumnya Eco-Twin AI) adalah platform analitik cerdas berbasis *Machine Learning* yang dirancang untuk memantau, memprediksi, dan mengoptimalkan manajemen logistik sampah DKI Jakarta secara spasial-temporal harian.

Sistem ini didesain menggunakan **Clean Architecture** (memisahkan frontend statis yang di-host di Vercel dan backend model AI di Hugging Face Spaces) dengan performa model prediksi yang sangat tinggi.

---

> [!NOTE]
> **📖 DOKUMENTASI SISTEM BACKEND**:  
> Untuk rincian mendalam mengenai arsitektur backend, model machine learning (GBR & Chronos), metrik akurasi GBR (R² 81.51%, MAPE 1.59%), formula rekayasa fitur cuaca/event, dan deployment Docker, silakan merujuk ke **[BACKEND_DOC.md](file:///c:/khusus project IT/Fine tuning ulang AI jakarta/waste-prediction-api/BACKEND_DOC.md)**.

---

## 🌟 Fitur Unggulan (Key Features)

1. **AI Autopilot Forecaster**: AI berjalan secara asinkron dan mandiri untuk memprediksi volume timbulan sampah harian di seluruh **44 Kecamatan DKI Jakarta** secara paralel berdasarkan cuaca live tingkat koordinat dan kalender event aktif hari ini.
2. **6-Kategori Komposisi Sampah**: Memprediksi rincian tonase sampah secara proporsional sesuai statistik riil Dinas Lingkungan Hidup (DLH) DKI Jakarta menjadi 6 kategori: *Sisa Makanan (~50.2%), Plastik (~22.8%), Kertas (~11.5%), Tekstil (~4.2%), Kaca (~3.2%), dan Logam/Lainnya (~8.1%)*.
3. **Integrasi Cuaca Live Open-Meteo**: API menarik data curah hujan real-time per kecamatan berdasarkan titik koordinat geografis asli untuk mengukur penambahan berat sampah basah akibat resapan air hujan (2% s.d. 5% multiplier).
4. **Kalender Event Jakarta 2026**: Mengidentifikasi jadwal acara besar Jakarta (seperti PRJ JIExpo, BTN Marathon, HUT RI di Monas, dll.) untuk menghitung lonjakan kapasitas sampah kerumunan (15% s.d. 30% multiplier).
5. **Interactive Cyber HUD UI**: Antarmuka bertema *Dark Glassmorphism* modern yang terinspirasi oleh floodzy.id dengan kursor interaktif kustom, visualisasi progress bar kategori neon glow, rincian logistik armada truk, dan efek radar sweep live di peta.

---

## 📊 Hasil Evaluasi & Akurasi Model GBR

Model inti Gradient Boosting Regressor (GBR) dilatih menggunakan **GridSearchCV** untuk mencari hyperparameter terbaik di atas dataset historis teraugmentasi 2 tahun dengan baseline rata-rata kota **8.020 Ton/hari**.

### Metrik Evaluasi Model:

| Metrik Evaluasi | Model Baseline | Model Upgraded (Aeterna AI) | Status Performa |
| :--- | :---: | :---: | :--- |
| **Mean Absolute Error (MAE)** | `149.13 Ton` | **`132.29 Ton`** | Semakin Baik (Turun ⬇️) |
| **Root Mean Squared Error (RMSE)** | `188.46 Ton` | **`165.46 Ton`** | Semakin Baik (Turun ⬇️) |
| **R-Squared ($R^2$ Score)** | `76.02%` | **`81.51%`** | Semakin Baik (Naik ⬆️) |
| **Mean Absolute Percentage Error (MAPE)** | `1.78%` | **`1.59%`** | **Sangat Akurat (< 10%) (⬇️)** |

### Hyperparameter Terbaik (GBR):
*   `n_estimators` (Pohon keputusan): **100**
*   `learning_rate`: **0.03**
*   `max_depth`: **3**
*   `subsample`: **0.9**

---

## 📂 Struktur Berkas (Clean Architecture)

```
waste-prediction-api/
├── frontend/                  (📂 Client-side statis Vercel-ready)
│   ├── index.html             (Dashboard Visual)
│   ├── style.css              (Estetika HUD Neon & Animasi)
│   ├── app.js                 (Logika Interaksi & Dynamic API routing)
│   └── vercel.json            (Konfigurasi standalone Vercel subfolder)
│
├── vercel.json                (Konfigurasi Vercel root level)
├── app.py                     (Python FastAPI Backend)
├── train.py                   (Skrip training GBR & GridSearchCV)
├── Dockerfile                 (Hugging Face Docker deployment)
├── requirements.txt           (Python library dependencies)
├── model_sampah_advanced.pkl  (Binary Model GBR)
├── latest_waste_news.json     (Database Berita Rill)
└── event_jakarta_2026.txt     (Jadwal Event Jakarta 2026)
```

---

## 📡 Dokumentasi Endpoint API Utama

Semua endpoint didukung dengan dokumentasi interaktif Swagger UI di `/docs`.

### 1. Predict Waste Volume (Forecasting)
*   **Method**: `POST`
*   **Endpoint**: `/api/v1/predict`
*   **Request Body**:
    ```json
    {
      "forecast_days": 7,
      "rainfall_mm": 0.0,
      "event_scale": 0,
      "location": "Menteng",
      "model_type": "gradient_boosting",
      "granularity": "daily"
    }
    ```
*   **Response JSON (Truncated)**:
    ```json
    {
      "status": "success",
      "confidence_score": 0.92,
      "message": "Normal conditions.",
      "data": {
        "prediction_results": [
          {
            "date": "2026-07-11",
            "total_volume_ton": 120.80,
            "organic_waste_ton": 60.64,
            "plastic_waste_ton": 27.54,
            "paper_waste_ton": 13.89,
            "metal_waste_ton": 9.78,
            "glass_waste_ton": 3.87,
            "textile_waste_ton": 5.07,
            "other_waste_ton": 0.00,
            "risk_status": "SAFE",
            "event_info": null,
            "recommended_trucks": 25
          }
        ]
      }
    }
    ```

### 2. AI Autopilot
*   **Method**: `GET`
*   **Endpoint**: `/api/v1/autopilot`
*   **Description**: Mengembalikan kalkulasi prediksi otonom hari ini untuk seluruh 44 kecamatan DKI secara paralel.

### 3. News Feed
*   **Method**: `GET`
*   **Endpoint**: `/api/v1/news`
*   **Description**: Mengembalikan 12 berita riil DKI Jakarta lengkap dengan link langsung ke artikel aslinya.

---

## 🚀 Panduan Deployment

### 1. Deploy ke Hugging Face Spaces (Backend API)
Aplikasi ini sudah dikonfigurasi untuk berjalan di Hugging Face Spaces menggunakan Docker:
1. Buat Space baru di Hugging Face dengan memilih **SDK: Docker**.
2. Hubungkan Git Anda atau unggah file di root direktori (termasuk `app.py`, `Dockerfile`, `requirements.txt`, dan `model_sampah_advanced.pkl`).
3. Port internal Docker sudah otomatis disetel ke `7860` (standar Hugging Face). Space Anda akan otomatis memuat dan menjalankan backend.

### 2. Deploy ke Vercel (Frontend Dashboard)
Frontend dirancang agar terpisah dan di-host di Vercel:
1. Hubungkan repositori GitHub Anda ke akun Vercel.
2. Buat proyek baru dan pilih repositori `Aeterna-Ai`.
3. Di bagian pengaturan Vercel, Anda dapat membiarkannya default (Vercel akan mendeteksi `vercel.json` di root) atau mengatur **Root Directory** langsung ke folder `frontend/`.
4. Vercel akan menyajikan frontend statis dan secara otomatis mem-proxy pemanggilan API `/api` langsung ke backend Hugging Face Space Anda tanpa kendala CORS.

---

## 🛠️ Pengembangan Lokal (Local Development)

### 1. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 2. Jalankan Server API Lokal
```bash
python -m uvicorn app:app --port 8001 --host 127.0.0.1
```
Akses UI lokal di: **[http://localhost:8001](http://localhost:8001)**  
Akses Swagger Docs di: **[http://localhost:8001/docs](http://localhost:8001/docs)**
