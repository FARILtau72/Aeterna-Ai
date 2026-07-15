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
**Platform Sistem Peringatan Dini & Peramalan Sampah Real-Time DKI Jakarta (Case 2 - AI Open Innovation Challenge 2026)**

---

## 📖 Overview

**Aeterna AI** (sebelumnya Eco-Twin AI) adalah platform analitik cerdas berbasis *Machine Learning* yang dirancang untuk memantau, memprediksi, dan mengoptimalkan manajemen logistik sampah DKI Jakarta secara spasial-temporal harian. 

Platform ini mengubah paradigma pengelolaan sampah dari **reaktif** (menangani setelah terjadi penumpukan) menjadi **prediktif** (memprediksi surge sebelum terjadi) guna mengoptimalkan penyebaran truk pengangkut ke 44 kecamatan DKI Jakarta.

> [!NOTE]
> **📖 DOKUMENTASI SISTEM BACKEND MENDALAM**:  
> Untuk rincian mendalam mengenai arsitektur backend, model machine learning (GBR & Chronos), metrik akurasi GBR (R² 81.51%, MAPE 1.59%), formula rekayasa fitur cuaca/event, dan deployment Docker, silakan merujuk ke **[BACKEND_DOC.md](BACKEND_DOC.md)**.

---

## 🌟 Fitur Unggulan (Key Features)

1.  **AI Autopilot Forecaster**: Sistem asinkron otonom yang mengevaluasi seluruh **44 Kecamatan DKI Jakarta** secara paralel berdasarkan curah hujan tingkat koordinat (Open-Meteo) dan kalender event aktif.
2.  **6-Kategori Komposisi Sampah**: Memprediksi rincian tonase sampah secara proporsional sesuai statistik riil DLH DKI Jakarta: *Sisa Makanan (~50.2%), Plastik (~22.8%), Kertas (~11.5%), Tekstil (~4.2%), Kaca (~3.2%), dan Logam/Lainnya (~8.1%)*.
3.  **Dynamic Weather Multiplier**: Mengintegrasikan curah hujan real-time per kecamatan berdasarkan titik koordinat geografis asli untuk mengukur penambahan berat sampah basah akibat resapan air hujan (2% s.d. 5% multiplier).
4.  **Event Calendar Crowd Engine**: Mengidentifikasi jadwal acara besar Jakarta (seperti PRJ, BTN Marathon, HUT RI, dll.) untuk menghitung lonjakan kapasitas sampah kerumunan (10% s.d. 35% multiplier).
5.  **Interactive Cyber HUD UI**: Antarmuka bertema *Dark Glassmorphism* dengan kursor delay kustom (lerp), visualisasi progress bar kategori neon glow, rincian logistik armada truk (15-Ton Heavy Compactor), dan rute logistik ke TPST Bantargebang.

---

## 🏗️ Arsitektur Sistem (Clean Architecture)

Sistem ini didesain menggunakan arsitektur modular multi-platform yang terpisah (*decoupled*):

```
                                  +-----------------------------------+
                                  |         NEXT.JS FRONTEND          |
                                  |   (Hosted on Vercel Global CDN)   |
                                  +-----------------------------------+
                                                    |
                                                    | HTTPS Requests
                                                    v
                                  +-----------------------------------+
                                  |          LARAVEL BACKEND          |
                                  |     (API Controller & Gateway)    |
                                  +-----------------------------------+
                                                    |
                                                    | REST Proxy API
                                                    v
+---------------------------------------------------------------------------------------------------+
|                                  PYTHON ML MICROSERVICE CONTAINER                                 |
|                               (Docker - Hosted on Hugging Face Spaces)                            |
|                                                                                                   |
|  [ FastAPI ] --> [ GBR Model (GridSearchCV) ] & [ Amazon Chronos-T5 ] --> [ Open-Meteo API Sync ] |
+---------------------------------------------------------------------------------------------------+
```

### Penjelasan Lapisan (Layers):
*   **Front-End Layer (Next.js)**: Menyajikan antarmuka pengguna interaktif. Memanfaatkan *Next.js Dynamic Imports* dengan SSR dinonaktifkan khusus untuk modul **Leaflet.js** agar peta interaktif dapat dirender secara asinkron di client-side tanpa memicu error server-node.
*   **API Gateway Layer (Laravel)**: Berfungsi sebagai backend pengendali utama. Menangani middleware CORS, validasi skema request, manajemen kalender event, parsing berita, dan mengamankan pemanggilan proxy ke microservice AI.
*   **ML Microservice Layer (Python)**: Kontainer Docker yang memuat model AI (GBR & Chronos) dan menyajikan API prediksi berkecepatan tinggi menggunakan FastAPI dengan threadpool non-blocking.

---

## 📊 Hasil Evaluasi & Akurasi Model GBR

Model GBR dilatih dengan **GridSearchCV** di atas dataset historis teraugmentasi 2 tahun dengan baseline rata-rata kota **8.020 Ton/hari**.

| Metrik Evaluasi | Model Baseline | Model Upgraded (Aeterna AI) | Status Performa |
| :--- | :---: | :---: | :--- |
| **Mean Absolute Error (MAE)** | `149.13 Ton` | **`132.29 Ton`** | Lebih Baik (Turun ⬇️) |
| **Root Mean Squared Error (RMSE)** | `188.46 Ton` | **`165.46 Ton`** | Lebih Baik (Turun ⬇️) |
| **R-Squared ($R^2$ Score)** | `76.02%` | **`81.51%`** | Lebih Baik (Naik ⬆️) |
| **Mean Absolute Percentage Error (MAPE)** | `1.78%` | **`1.59%`** | **Sangat Akurat (< 10%) (⬇️)** |

---

## 🌦️ Model Rekayasa Fitur Matematika

### A. Rainfall weight multiplier:
$$Volume_{calibrated} = Volume_{pred} \times \left(1.0 + \frac{Precipitation_{mm}}{1000} \right)$$

### B. Event Crowd Multiplier:
*   Skala 1 s.d. 2 (Lokal): **+10% s.d. +15%** volume sampah.
*   Skala 3 s.d. 4 (Regional): **+20% s.d. +25%** volume sampah.
*   Skala 5 (Nasional / Hari Raya): **+30% s.d. +35%** volume sampah.

---

## 📡 Referensi Endpoint API Utama

Semua endpoint didukung dengan dokumentasi interaktif Swagger UI di `/docs`.

### 1. Predict Waste Volume (Forecasting)
*   **Method**: `POST`
*   **Endpoint**: `/api/v1/predict`
*   **Request Payload**:
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
*   **Response Payload**:
    ```json
    {
      "status": "success",
      "confidence_score": 0.9325,
      "message": "Normal conditions.",
      "data": {
        "prediction_results": [
          {
            "date": "2026-07-15",
            "location": "Menteng",
            "total_volume_ton": 120.8,
            "organic_waste_ton": 60.64,
            "plastic_waste_ton": 27.54,
            "paper_waste_ton": 13.89,
            "recommended_trucks": 8,
            "risk_status": "SAFE"
          }
        ],
        "logistics_plan": {
          "trucks_needed": 8,
          "manpower": 24,
          "estimated_duration_hours": 8.1,
          "efficiency_rate": "85% (Optimal)"
        }
      }
    }
    ```

### 2. Autopilot Live DKI (Today)
*   **Method**: `GET`
*   **Endpoint**: `/api/v1/autopilot`
*   **Description**: Mengembalikan kalkulasi prediksi otonom hari ini untuk seluruh 44 kecamatan DKI secara paralel lengkap dengan data koordinat (latitude, longitude) untuk plotting peta instan.

### 3. News Feed API
*   **Method**: `GET`
*   **Endpoint**: `/api/v1/news`
*   **Description**: Mengembalikan 10 berita persampahan DKI Jakarta terbaru yang diperbarui dinamis menggunakan Conduit AI API (dengan generator fallback lokal).

---

## 🛠️ Panduan Instalasi & Pengembangan Lokal

### 1. Prasyarat & Backend Setup (Python ML)
Masuk ke root folder proyek:
```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan server FastAPI lokal
python -m uvicorn app:app --port 8001 --host 127.0.0.1
```
*   Akses UI di: `http://localhost:8001`
*   Akses Swagger di: `http://localhost:8001/docs`

### 2. Setup Backend Controller (Laravel)
Jika menggunakan controller Laravel untuk mengamankan route API:
```bash
# Clone atau masuk ke direktori Laravel Anda
composer install
cp .env.example .env
php artisan key:generate
```
Di dalam berkas `.env` Laravel, arahkan URL microservice AI Anda:
```env
AETERNA_ML_SERVICE_URL=http://localhost:8001
```

### 3. Setup Frontend Dashboard (Next.js)
```bash
# Masuk ke folder Next.js
npm install
npm run dev
```
*   Pastikan Leaflet di-import dinamis:
    ```javascript
    import dynamic from 'next/dynamic';
    const MapComponent = dynamic(() => import('../components/Map'), { ssr: false });
    ```

---

## 👥 Kontributor Tim Pengembang (Aeterna Team)

*   **FARIL PUTRA PRATAMA** (AI Engineer) — *SMK Taruna Bangsa*
*   **ARGA KURNIAWAN** (Front End Developer)
*   **BAGAS TRESNA MUSTIDA SAKLI** (System Architecture)
