---
title: Predictive Waste Analytics
emoji: 🚛
colorFrom: green
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---







# 🌍 Eco-Twin AI: Waste Volume Prediction System
**Proyek untuk Hackathon DKI Jakarta 2026 (Case 2)**

Eco-Twin AI adalah sistem cerdas berbasis *Machine Learning* yang dirancang untuk memprediksi lonjakan volume timbulan sampah harian di area Jakarta Pusat. Sistem ini menggunakan arsitektur ganda: **Amazon Chronos-T5** (Time-Series Transformer) untuk peramalan (*forecasting*) dan integrasi Algoritma Pendukung untuk ekstraksi fitur lanjutan (Cuaca, Skala Keramaian, dan Jadwal Event).

---

## 🚀 Fitur Unggulan (Hackathon Killer Features)

1. **Integrasi Kalender Event Otomatis**: Sistem secara otomatis membaca file `event_jakarta_2025.txt` saat server dinyalakan. Jika ada *request* prediksi yang menyentuh tanggal konser besar (misal: Maroon 5 di JIS), AI akan mendeteksi dan secara akurat menambahkan estimasi volume sampah tanpa input manual tambahan.
2. **Asynchronous API Processing**: Menggunakan FastAPI dengan `run_in_threadpool`, memastikan sistem AI tidak memblokir (*blocking*) pengguna lain saat sedang mengolah model Transformer yang berat.
3. **Standar Produksi (CORS & Logging)**: Aplikasi aman dipanggil secara langsung oleh Frontend (React/Vue/HTML) dan menggunakan sistem *logging* kelas enterprise.
4. **Interactive API Docs (Swagger UI)**: Endpoint dilengkapi parameter Pydantic lengkap beserta contoh JSON terisi otomatis, sangat cocok untuk didemokan langsung ke Juri.
5. **Dekomposisi Sampah SIPSN KLHK 2025**: Memprediksi bukan hanya berat total (Ton), tapi juga membedahnya menjadi *Sisa Makanan* dan *Plastik*, serta memberikan rekomendasi jumlah armada truk yang dibutuhkan.

---

## 📂 Struktur File

- `app.py` : Berisi *Core Engine* API menggunakan FastAPI dan Amazon Chronos.
- `train.py` : Script *Advanced Feature Engineering* dan pelatihan model Gradient Boosting (Eco-Twin Pro) untuk simulasi dataset.
- `event_jakarta_2025.txt` : *Database* kalender event yang otomatis dilacak oleh AI.
- `dataset_vibe_coder_2025.csv` : Dataset historis yang dipakai oleh model.
- `.dockerfile` : Konfigurasi untuk men-*deploy* aplikasi ini (misalnya ke Hugging Face Spaces atau server Cloud).
- `requirements.txt` : Daftar dependensi *library* Python.

---

## 🛠️ Cara Menjalankan Sistem

### 1. Instalasi Kebutuhan (Library)
Pastikan Python sudah terinstal di laptop Anda. Buka Terminal/Command Prompt di dalam folder proyek ini, lalu jalankan:
```bash
pip install -r requirements.txt
pip install chronos-forecasting
```

### 2. Menjalankan Server API
Jalankan server Uvicorn dengan mode *auto-reload* agar perubahan kode langsung terbaca:
```bash
uvicorn app:app --reload --port 8001
```

### 3. Menguji via Swagger (Demonstrasi Juri)
Setelah server berjalan, buka browser dan akses:
👉 **[http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)**

Anda bisa menekan tombol **"Try it out"** di *endpoint* `/api/v1/predict` dan langsung tekan **"Execute"**.

---

## 📡 Dokumentasi Endpoint API

### 1. Status Check
Mengecek apakah server hidup dan berapa banyak jadwal event yang berhasil dimuat oleh AI.
- **URL**: `/`
- **Method**: `GET`
- **Response**:
```json
{
  "status": "Online",
  "model": "Chronos-T5 Tiny",
  "region": "Jakarta Pusat",
  "events_loaded": 15
}
```

### 2. Prediksi Volume Sampah (Forecasting)
Mendapatkan peramalan volume sampah berdasarkan data historis, cuaca, dan event.
- **URL**: `/api/v1/predict`
- **Method**: `POST`
- **Body Request**:
```json
{
  "hari_ke_depan": 7,
  "prediksi_hujan_bmkg": 25.5,
  "skala_keramaian": 0
}
```
- **Response JSON**:
```json
[
  {
    "tanggal": "2026-02-01",
    "total_volume_ton": 1520.45,
    "sisa_makanan_ton": 758.25,
    "plastik_ton": 348.94,
    "rekomendasi_truk": 153,
    "status_risiko": "CRITICAL ⚠️",
    "info_event": "Konser Maroon 5 di Jakarta International Stadium (JIS)"
  }
]
```

---

## 📝 Catatan Penting
- Jika Anda mendapatkan error `ModuleNotFoundError: No module named 'chronos'`, pastikan Anda menginstal package dengan perintah `pip install chronos-forecasting` **(BUKAN pip install chronos)**.
- Untuk deployment dengan `Dockerfile`, pastikan untuk mengubah port Uvicorn menyesuaikan provider (misal: HuggingFace Spaces menggunakan `--port 7860`).


