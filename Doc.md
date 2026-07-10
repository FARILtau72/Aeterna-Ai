

# 🗑️ Waste Intelligence API — Complete Documentation
> **AI-Powered Predictive Waste Management System for Jakarta Pusat (CASE 2)**  
> Version: `2.0.0` | License: `MIT` | Author: `Faril Putra Pratama - SMK Taruna Bangsa`

---

> [!IMPORTANT]
> **📖 DOKUMENTASI & PENGUJIAN SISTEM**:  
> * **Untuk Publik / Stakeholder**: Silakan merujuk ke dokumen [PUBLIC_DOC.md](file:///c:/khusus%20project%20IT/Fine%20tuning%20ulang%20AI%20jakarta/waste-prediction-api/PUBLIC_DOC.md) untuk memahami cara kerja sistem AI, arsitektur, dan panduan penggunaan bagi pengguna umum.
> * **Untuk Developer Front-End (FE)**: Silakan merujuk langsung ke dokumen [FRONTEND_API_DOC.md](file:///c:/khusus%20project%20IT/Fine%20tuning%20ulang%20AI%20jakarta/waste-prediction-api/FRONTEND_API_DOC.md) untuk spesifikasi detail endpoint API, tipe data TypeScript, contoh kode Axios/Fetch, serta petunjuk integrasi visual.
> * **Pengujian API (Postman)**: Anda dapat mengimpor file [waste_intelligence_api.postman_collection.json](file:///c:/khusus%20project%20IT/Fine%20tuning%20ulang%20AI%20jakarta/waste-prediction-api/waste_intelligence_api.postman_collection.json) langsung ke aplikasi Postman Anda untuk menguji seluruh endpoint secara instan.

---

## 📑 Table of Contents
1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Core AI & Business Logic](#3-core-ai--business-logic)
4. [API Reference](#4-api-reference)
5. [Data Dictionary](#5-data-dictionary)
6. [Deployment & Setup](#6-deployment--setup)
7. [Testing & Validation](#7-testing--validation)
8. [Business Impact & Use Cases](#8-business-impact--use-cases)
9. [Roadmap & Scalability](#9-roadmap--scalability)
10. [Author & Support](#10-author--support)

---

## 1. Project Overview

###  Problem Statement
Penumpukan sampah di Jakarta Pusat sering terjadi secara mendadak saat:
- ️ Musim hujan tinggi (sampah basah → berat volume naik)
- 🎪 Event besar (PRJ, Lebaran, Konser, HUT RI)
- 📅 Weekend & libur nasional

Penanganan saat ini masih **reaktif**: armada dikirim setelah laporan masuk atau tumpukan terlihat. Akibatnya: biaya operasional membengkak, jadwal pengangkutan tidak efisien, dan risiko kesehatan lingkungan meningkat.

### 💡 Solution
Sistem ini mengubah paradigma menjadi **prediktif** menggunakan:
- 🤖 **Amazon Chronos** (Transformer time-series) untuk forecasting baseline volume
- 🌦️ **BMKG Weather Integration** untuk penyesuaian berat sampah basah
- 📅 **Event Calendar Engine** dengan location-aware impact modeling
- 🚛 **Logistics Optimizer** untuk rekomendasi armada & manpower presisi

**Output**: Prediksi volume sampah 1–30 hari ke depan per lokasi, dekomposisi organik/plastik, status risiko, dan rencana logistik operasional.

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────┐
│                 CLIENT LAYER                     │
│  • Postman / Frontend Dashboard / Mobile App    │
│  • REST API Calls (JSON)                         │
└────────────────────────────────────────────────┘
              │ HTTPS / CORS
              ▼
┌─────────────────────────────────────────────────┐
│              API GATEWAY (FastAPI)              │
│  • Request Validation (Pydantic)                │
│  • CORS Middleware                              │
│  • Structured Logging                           │
└─────────────┬───────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    ▼                   ▼
─────────┐     ┌─────────────┐
│ PREDICT │     │  STATUS     │
│Endpoint │     │  Check      │
└────┬────┘     └─────────────┘
     │
     ▼
┌─────────────────────────────────────────────────┐
│           BUSINESS LOGIC LAYER                  │
│  1️⃣ Date Parser & Context Setup                │
│  2️⃣ Chronos Inference (Async/ThreadPool)       │
│  3️⃣ External Factor Integration                │
│     • Rain multiplier (BMKG)                    │
│     • Event engine + radius mapping             │
│     • Soft impact scaling (10–35%)              │
│  4️⃣ Post-Processing & Aggregation              │
│     • KLHK 2026 decomposition                   │
│     • Risk scoring & truck calculation          │
─────────────┬───────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    ▼                   ▼
┌─────────┐     ┌─────────────┐
│ DATA    │     │ MODEL       │
│ LAYER   │     │ LAYER       │
│ • CSV   │     │ • Chronos  │
│ • In-mem│     │   T5-Tiny   │
│ Cache   │     │ • PyTorch   │
└─────────┘     └─────────────┘
```

### 🔹 Tech Stack
| Layer | Technology |
|-------|------------|
| API Framework | FastAPI + Uvicorn |
| AI Model | Amazon Chronos-T5-Tiny (Hugging Face) |
| Data Processing | Pandas, NumPy |
| Validation | Pydantic v2 |
| Deployment | Hugging Face Spaces (CPU) |
| Logging | Python `logging` (structured) |

---

## 3. Core AI & Business Logic

### 🤖 3.1 Time-Series Forecasting (Chronos)
- **Model**: `amazon/chronos-t5-tiny` (lightweight, CPU-optimized)
- **Input**: Historical volume series (`dataset_vibe_coder_2026.csv`, 365 hari)
- **Output**: Probabilistic forecast (median quantile `0.5`) untuk `N` hari ke depan
- **Advantage**: Mampu menangkap pola musiman, tren gradual, dan fluktuasi natural tanpa fitur engineering berat

### 🎪 3.2 Event Engine & Location Matching
Event tidak serta-merta menaikkan volume di seluruh kota. Sistem menggunakan **radius-aware logic**:

```python
EVENT_RADIUS_MAP = {
    'jiexpo': ['jis', 'kemayoran', 'pademangan', 'jakarta'],
    'monas': ['pasar senen', 'gang sempit tambora', 'merdeka', 'jakarta'],
    'gbk': ['senayan', 'tanah abang', 'kuningan', 'jakarta'],
    'ancol': ['pademangan', 'kelapa gading', 'jakarta'],
    'jakarta': ['*']  # City-wide
}
```
- **Matching Rules**: Direct string match → City-wide fallback → Radius mapping
- **Impact Scaling**: `1.0 + (0.10 + min(scale * 0.05, 0.25))` → Maksimal **+35%** volume
- **Result**: Event di JIExpo hanya mempengaruhi JIS/Kemayoran, bukan GBK/Senayan

### 🌧️ 3.3 Weather Integration (BMKG Style)
Curah hujan mempengaruhi berat sampah (basah = lebih padat/berat):
- `≤20mm`: Tidak ada penyesuaian
- `>20mm`: Multiplier `1.02` hingga `1.05` (linear scaling)
- **Rationale**: Sampah organik menyerap air → tonase naik tanpa volume fisik berubah drastis

### ️ 3.4 Risk Scoring Algorithm
```python
def hitung_prioritas(nama_lokasi, volume_ton):
    akses = DATABASE_LOKASI[nama_lokasi]['aksesibilitas']  # 0.25 – 1.0
    skor = volume_ton / akses
    if skor > 1600: return 'CRITICAL ⚠️'
    if skor >= 1100: return 'WARNING 🟡'
    return 'SAFE ✅'
```
- **Accessibility Factor**: Lokasi sempit/sulit dijangkau (`0.25`) mendapat skor risiko lebih tinggi untuk volume yang sama
- **Thresholds**: Dikalibrasi untuk rentang volume realistis Jakarta Pusat (1000–2000 ton)

### 📊 3.5 Waste Decomposition (KLHK 2026)
Rasio dekomposisi dihitung dinamis dari dataset historis, fallback ke standar resmi:
- **Organik/Sisa Makanan**: `~49.87%`
- **Plastik**: `~22.95%`
- **Sisanya**: Kertas, logam, residu (tidak dihitung terpisah untuk optimasi logistik)

---

## 4. API Reference

### 1. `POST /api/v1/predict`
**Deskripsi**: Menghasilkan prediksi volume timbulan sampah harian/jam-an untuk lokasi tertentu beserta analisis risiko logistik menggunakan model Amazon Chronos atau Gradient Boosting.

#### Request Body
```json
{
  "forecast_days": 7,
  "rainfall_mm": 25.5,
  "event_scale": 0,
  "location": "JIS",
  "start_date": "2026-07-03",
  "granularity": "daily",
  "model_type": "gradient_boosting"
}
```
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `forecast_days` | `int` | ✅ | Durasi prediksi (1–30 hari) |
| `rainfall_mm` | `float` | ✅ | Curah hujan (mm). `0` = Auto (mengambil ramalan cuaca dari Open-Meteo) |
| `event_scale` | `int` | ✅ | Skala keramaian event buatan (0-5) |
| `location` | `string` | ✅ | Target lokasi: `JIS`, `GBK`, `Pasar Senen`, `Gang Sempit Tambora` |
| `start_date` | `string` | ❌ | Tanggal awal prediksi. Contoh: `2026-07-03` |
| `granularity` | `string` | ❌ | Tingkat rincian: `daily` atau `hourly` (default: `daily`) |
| `model_type` | `string` | ❌ | Algoritma: `gradient_boosting` atau `chronos` (default: `gradient_boosting`) |

#### Response Success (200)
```json
{
  "status": "success",
  "message": "Normal conditions.",
  "confidence_score": 0.9325,
  "data": {
    "prediction_results": [
      {
        "date": "2026-07-03",
        "location": "JIS",
        "total_volume_ton": 140.70,
        "organic_waste_ton": 70.17,
        "plastic_waste_ton": 32.29,
        "recommended_trucks": 29,
        "risk_status": "SAFE",
        "event_info": null,
        "hourly_breakdown": null
      }
    ],
    "logistics_plan": {
      "trucks_needed": 29,
      "manpower": 87,
      "estimated_duration_hours": 28.1,
      "efficiency_rate": "85% (Optimal)"
    }
  }
}
```

---

### 2. `POST /api/v1/predict/csv`
**Deskripsi**: Mengirimkan parameter yang sama seperti endpoint prediksi standar, tetapi menghasilkan output berkas CSV secara langsung untuk diunduh.

#### Request Body
Sama seperti `POST /api/v1/predict`.

#### Response Success (200)
Mengembalikan berkas file download (`text/csv`) dengan nama file dinamis: `waste_forecast_[Location]_[Days]d.csv`.
**Header Respon**:
`Content-Disposition: attachment; filename="waste_forecast_JIS_7d.csv"`

---

### 3. `GET /status`
**Deskripsi**: Health check status server dan ketersediaan model ML.
#### Response Success (200)
```json
{
  "status": "Online",
  "model_chronos": "Chronos-T5 Tiny",
  "model_gbr": "Gradient Boosting Regressor",
  "calibrated": true
}
```

---

## 5. Data Dictionary

### 📄 `dataset_vibe_coder_2026.csv`
| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `TANGGAL` | `YYYY-MM-DD` | Hari observasi |
| `RR` | `float` | Curah hujan (mm) |
| `Nama_Event` | `string` | Nama event (kosong jika tidak ada) |
| `Ada_Event` | `int` | Flag `1`/`0` |
| `Crowd_Scale` | `float` | Skala keramaian (0–5) |
| `Volume_Total_Ton` | `float` | Volume sampah baseline |
| `Vol_Sisa_Makanan_Ton` | `float` | Komponen organik |
| `Vol_Plastik_Ton` | `float` | Komponen plastik |
| `Hari_Ke` | `int` | Urutan hari (1–365) |
| `Is_Weekend` | `int` | `1` = Sabtu/Minggu |
| `ZONA` | `string` | Klasifikasi area: `Tourism`, `Residential`, `Commercial` |

### 📄 `event_jakarta_2026.txt`
| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `tanggal` | `YYYY-MM-DD` | Tanggal event |
| `nama_event` | `string` | Nama event |
| `lokasi` | `string` | Lokasi utama event |
| `skala_keramaian` | `int` | Skala 1–5 |

---

## 6. Deployment & Setup

###  Hugging Face Spaces (Production)
1. Create Space → Template: `Blank` → Runtime: `Python`
2. Upload files:
   ```
   📁 waste-prediction-api/
   ├── app.py
   ├── dataset_vibe_coder_2026.csv
   ├── event_jakarta_2026.txt
   ├── requirements.txt
   └── SYSTEM_ARCHITECTURE.md
   ```
3. Settings → Python 3.10, Hardware: `CPU`, Auto-rebuild: `ON`
4. Click **Factory rebuild** after each commit

### 💻 Local Development
```bash
git clone https://huggingface.co/spaces/ALAMDIENG/waste-prediction-api
cd waste-prediction-api
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```
Test:
```bash
curl -X POST http://localhost:8001/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"hari_ke_depan":7,"dari_tanggal":"06-01","nama_lokasi":"JIS"}'
```

### 📦 `requirements.txt`
```txt
fastapi>=0.104.0
uvicorn>=0.24.0
pandas>=2.1.0
numpy>=1.26.0
torch>=2.1.0
chronos-forecasting>=0.1.0
pydantic>=2.5.0
httpx>=0.25.0
```

---

## 7. Testing & Validation

### 🧪 Unit Tests (Conceptual)
```python
def test_parse_flexible_date():
    assert parse_flexible_date("06-01").date() == date(2026, 6, 1)
    assert parse_flexible_date("1 Juni 2026").date() == date(2026, 6, 1)

def test_location_matching():
    assert check_location_match("JIS", "JIExpo") == True
    assert check_location_match("GBK", "JIExpo") == False
```

###  Integration Scenarios (Postman)
| Scenario | Input | Expected |
|----------|-------|----------|
| Normal day | `dari_tanggal: "06-10", skala: 0` | `info_event: null`, volume ~1200 ton |
| Event match | `dari_tanggal: "06-01", lokasi: "JIS"` | `info_event: "PRJ..."`, +20–35% volume |
| Event no-match | `dari_tanggal: "06-01", lokasi: "GBK"` | `info_event: null`, volume normal |
| Heavy rain | `prediksi_hujan_bmkg: 50` | Multiplier +2–5% |
| Low accessibility | `lokasi: "Gang Sempit Tambora"` | Lower volume → WARNING/CRITICAL |

### 📈 Performance Targets
- **Latency**: `< 3.0s` (p95) untuk forecast 7 hari
- **Throughput**: `10–20 req/min` (HF Spaces CPU tier)
- **Accuracy**: `±8–12%` MAE vs baseline historis (valid untuk perencanaan logistik)

---

## 8. Business Impact & Use Cases

###  Operational Efficiency
| Metric | Before (Reactive) | After (Predictive) | Improvement |
|--------|-------------------|--------------------|-------------|
| Fleet dispatch | After complaint/report | H-1/H-2 scheduled | ⬇️ 15–20% idle time |
| Fuel cost | Unplanned routes | Optimized zoning | ️ 10–12% consumption |
| Manpower | Overtime-heavy | Shift-planned | ⬇️ 8–10% overtime |
| Public health | Post-spill cleanup | Pre-emptive containment | ⬆️ Risk mitigation |

###  Primary Use Cases
1. **Dinas Lingkungan Hidup**: Penjadwalan armada harian berbasis risiko zonasi
2. **Event Organizer**: Kalkulasi kebutuhan TPS & truk sampah saat izin keramaian
3. **Fasilitas Pengelola Sampah**: Alokasi shift & kapasitas gudang 3 hari ke depan
4. **Dashboard Eksekutif**: Executive summary + visual heatmap volume per kecamatan

---

## 9. Roadmap & Scalability

###  v2.1 (Next 3 Months)
- [ ] Real-time BMKG API integration (auto-fetch `prediksi_hujan_bmkg`)
- [ ] Batch prediction endpoint (`/api/v1/predict/multi`)
- [ ] Export to PDF/CSV + email webhook
- [ ] Rate limiting & API key auth

### 🏗️ v3.0 (Architecture Upgrade)
- [ ] Microservices split: `forecast-service`, `event-service`, `logistics-service`
- [ ] GPU inference optimization (Chronos-base/mini)
- [ ] Automated retraining pipeline (GitHub Actions + HF Datasets)
- [ ] Prometheus/Grafana observability + alerting

###  Long-term Vision
> *"Dari prediksi volume → optimasi rute real-time → circular economy tracking. Sistem ini menjadi tulang punggung smart city waste management yang data-driven, hemat biaya, dan berkelanjutan."*

---

## 10. Author & Support

**Developed by**:  
 **Faril Putra Pratama**  
 SMK Taruna Bangsa  
🔗 [GitHub: @FARILtau72](https://github.com/FARILtau72)  

**License**: MIT  
**Case Study**: Waste Volume Prediction System (CASE 2)  
**Last Updated**: 2026-06-01  

📩 **Issues & Contributions**:  
Gunakan GitHub Issues untuk bug report, feature request, atau dokumentasi improvement. PR welcome!

---

> 💡 **Presenter Note**:  
> *"Sistem ini bukan sekadar forecast angka. Ia adalah decision engine: Chronos memberi baseline, cuaca memberi koreksi berat, event memberi konteks spasial, dan risk scoring memberi prioritas aksi. Hasilnya? Armada tidak lagi keliling buta—mereka datang ke tempat yang tepat, di waktu yang tepat, dengan kapasitas yang tepat."*

---