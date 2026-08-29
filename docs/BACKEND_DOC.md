# AETERNA AI — Backend Architecture & Engineering Documentation (v4.1.0)

Dokumen ini menjelaskan detail teknis arsitektur sistem backend, model machine learning (Stacking Regressor & Amazon Chronos), rekayasa fitur (*feature engineering*), simulasi logistik deterministik, serta panduan kontainerisasi dan *deployment* untuk **AETERNA AI (Waste Forecasting & Decision Intelligence Platform)**.

---

## 🏗️ 1. Desain Arsitektur Backend

Backend AETERNA AI dibangun menggunakan **FastAPI (Python)** dengan arsitektur asinkron berkecepatan tinggi.

```
+-----------------------------------------------------------------------------------------------+
|                                      FASTAPI BACKEND ENGINE                                   |
|                                                                                               |
|   [ /api/v1/predict ]              [ /api/v1/autopilot ]                 [ /api/v1/news ]     |
|            |                                 |                                  |             |
|            v                                 v                                  v             |
|   +---------------------------------------------------------+           +------------------+  |
|   |                  AI FORECAST LAYER                      |           | Curated News DB  |  |
|   |  - Stacking Regressor (DT + RF + GBR -> Ridge)          |           | (Static JSON)    |  |
|   |  - Amazon Chronos-T5 (Tiny) Time-Series Model           |           +------------------+  |
|   +---------------------------------------------------------+                                 |
|            |                                                                                  |
|            v                                                                                  |
|   +---------------------------------------------------------+                                 |
|   |           DETERMINISTIC LOGISTICS SIMULATION            |                                 |
|   |  - Suggested Fleet (15T Compactor @ 95% Load Factor)    |                                 |
|   |  - Crew Sizing (3 Personnel / Active Truck)             |                                 |
|   |  - Collection Time (Throughput 2.0 Ton/Hour/Truck)      |                                 |
|   +---------------------------------------------------------+                                 |
|            |                                                                                  |
|            v                                                                                  |
|   +---------------------------------------------------------+                                 |
|   |                    DATA INGESTION LAYER                 |                                 |
|   |  - Open-Meteo Weather API (Live Observed Rainfall mm)   |                                 |
|   |  - BPS Headcount Reference (44 Sub-districts)           |                                 |
|   |  - Event & Mudik Calendar Feature Extractor             |                                 |
|   +---------------------------------------------------------+                                 |
+-----------------------------------------------------------------------------------------------+
```

### Komponen Utama:
1. **Asynchronous Handling**: Memanfaatkan FastAPI dengan `run_in_threadpool` untuk menjalankan inferensi neural time-series (Chronos Transformer) tanpa memblokir thread event loop utama.
2. **Data Provenance Enforcement**: Seluruh skema response mengembalikan field provenance resmi (`data_status`, `forecast_type`, `model_version`, `training_data_type`, `disclaimer`, `weather_source`, `population_source`).
3. **Automatic OpenAPI / Swagger**: Endpoint terdokumentasi interaktif di `/docs` berbasis skema Pydantic V2.

---

## 🧠 2. Mesin Machine Learning (ML Engine)

### A. AETERNA Stacking Regressor — Model Prediksi Spasial Multi-Kecamatan
Model ensemble yang menggabungkan 3 base-learner pohon keputusan dengan 1 meta-learner linear:
* **Base Models**:
  1. `DecisionTreeRegressor(max_depth=6)`
  2. `RandomForestRegressor(n_estimators=150, max_depth=6)`
  3. `GradientBoostingRegressor(n_estimators=150, max_depth=5, lr=0.05)`
* **Meta-Learner**: `Ridge(alpha=1.0)`
* **Fitur Input**: 11 variabel spasial-temporal (`Population_Jiwa`, `Normal_Avg_Ton`, `Zone_Type_Code`, `Rainfall_mm`, `Rain_Lag_1`, `Is_Weekend`, `Hari_Dalam_Minggu`, `Bulan`, `Is_Mudik`, `Ada_Event`, `Event_Crowd_Headcount`).

> ⚠️ **Catatan Evaluasi Ilmiah**: Metrik evaluasi di bawah ini merupakan hasil pengujian pada dataset simulasi pengembangan (*Mode A: Synthetic Development Benchmark*). Evaluasi ini menunjukkan kemampuan algoritma mempelajari pola sintetis dan **bukan** bukti validasi akurasi lapangan dunia nyata.

* **Metrik Evaluasi Synthetic Benchmark (Test Set Kronologis Juli – Desember 2025)**:
  * **Mean Absolute Error (MAE)**: `11.85 Ton`
  * **Root Mean Squared Error (RMSE)**: `15.42 Ton`
  * **R-Squared ($R^2$ Score)**: `88.45%`
  * **Mean Absolute Percentage Error (MAPE)**: `6.12%`

### B. Amazon Chronos-T5 (Tiny) — Model Deret Waktu
Model Transformer deret waktu dari Amazon Research yang digunakan untuk inferensi deret waktu zero-shot berdasarkan riwayat tonase lokal.

---

## 🚚 3. Mesin Simulasi Logistik Deterministik (Non-AI Engine)

AETERNA AI memisahkan secara tegas perhitungan logistik dari model machine learning. Rekomendasi armada dihitung menggunakan formula deterministik berbasis kapasitas dan throughput pengangkutan:

1. **Suggested Fleet (15-Ton Compactor Baseline)**:
   $$	ext{Effective Capacity} = 15.0	ext{ Ton} 	imes 0.95 = 14.25	ext{ Ton/trip}$$
   $$	ext{Base Trucks} = \lceil 	ext{Forecast Volume} / 14.25	ext{ Ton} ceil$$
   $$	ext{Suggested Trucks} = \lceil 	ext{Base Trucks} 	imes 1.05	ext{ (Buffer)} ceil$$
2. **Kebutuhan Personel (Crew Sizing)**:
   $$	ext{Total Personel} = 	ext{Suggested Trucks} 	imes 3	ext{ (1 Driver + 2 Sanitarians)}$$
3. **Estimasi Waktu Pengangkutan (Throughput-Based)**:
   $$	ext{Fleet Throughput} = 	ext{Active Trucks} 	imes 2.0	ext{ Ton/jam}$$
   $$	ext{Raw Hours} = rac{	ext{Forecast Volume}}{	ext{Fleet Throughput}}$$
   $$	ext{Adjusted Hours} = rac{	ext{Raw Hours} 	imes F_{	ext{traffic}} 	imes F_{	ext{weather}} 	imes F_{	ext{event}}}{	ext{Efficiency}}$$

---

## 🌦️ 4. Rekayasa Fitur Dinamis & Integrasi Weather Open-Meteo

* **Curah Hujan Live (Open-Meteo API)**:
  Sistem memanggil Open-Meteo API secara asinkron berdasarkan koordinat (`latitude`, `longitude`) masing-masing kecamatan.
  1. `Rainfall_mm`: Curah hujan harian (mm) tanggal target.
  2. `Rain_Lag_1`: Curah hujan harian 1 hari sebelumnya untuk menangkap efek penundaan pengangkutan dan penyerapan air.
* **Fitur Demografi**: Populasi BPS DKI Jakarta per kecamatan.
* **Fitur Kalender**: Hari kerja vs akhir pekan, bulan, serta jendela mudik Lebaran.

---

## 📰 5. Sistem Berita & Artikel Referensi Terkurasi

Endpoint `/api/v1/news` menyediakan artikel referensi terkurasi mengenai tata kelola sampah DKI Jakarta.

### Integritas Sumber:
* **Curated Static Mode**: Seluruh artikel diverifikasi secara manual dengan tautan URL asli ke media resmi (Detik.com, Antara News, Kompas.com).
* **No LLM Fabrication**: Pembuatan artikel buatan oleh LLM dinonaktifkan secara permanen guna mencegah penyebaran disinformasi publik.

---

## 🐳 6. Panduan Kontainerisasi & Deployment

Aplikasi dapat dijalankan melalui Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /code
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```
