---
title: AETERNA AI — Waste Forecasting & Decision Intelligence
emoji: 🚛
colorFrom: green
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

# 🚛 AETERNA AI — Waste Forecasting & Decision Intelligence
### Platform Riset Prediksi Timbulan Sampah & Simulasi Logistik Operasional 44 Kecamatan DKI Jakarta

<p align="center">
  <a href="https://www.aeternaai.biz.id/"><img src="https://img.shields.io/badge/Web%20Portal-aeternaai.biz.id-00f2fe?style=for-the-badge&logo=googlechrome" alt="Web Portal" /></a>
  <a href="https://www.linkedin.com/in/faril-putra-pratama-81561a280/"><img src="https://img.shields.io/badge/LinkedIn-Faril%20Putra%20Pratama-0a66c2?style=for-the-badge&logo=linkedin" alt="LinkedIn Profile" /></a>
  <a href="https://github.com/FARILtau72/Aeterna-Ai"><img src="https://img.shields.io/badge/GitHub-FARILtau72-181717?style=for-the-badge&logo=github" alt="GitHub Repo" /></a>
  <a href="https://github.com/FARILtau72/Aeterna-Ai/stargazers"><img src="https://img.shields.io/github/stars/FARILtau72/Aeterna-Ai?style=for-the-badge&color=gold" alt="GitHub Stars" /></a>
</p>

> [!IMPORTANT]
> **RESEARCH PROTOTYPE & DECISION SUPPORT NOTICE**  
> **AETERNA AI** adalah prototipe riset independen (*Student-led R&D project*) yang mengeksplorasi pemanfaatan Machine Learning spasial-temporal, data cuaca live, dan simulasi logistik deterministik untuk perencanaan pengelolaan sampah di DKI Jakarta.  
> Seluruh hasil prediksi dan simulasi alokasi armada merupakan estimasi pendukung keputusan (*decision support estimates*), bukan instruksi operasional resmi dari Dinas Lingkungan Hidup (DLH) DKI Jakarta atau Jakarta Smart City.

---

## 1. Project Overview & Positioning

AETERNA AI dirancang untuk mengeksplorasi transisi pengelolaan sampah perkotaan dari **pendekatan reaktif** (merespons setelah TPS mengalami kelebihan muatan) menuju **pendekatan proaktif** (mengantisipasi lonjakan timbulan sampah berbasis prakiraan cuaca, kepadatan penduduk, dan kalender kegiatan masyarakat).

Platform ini mengintegrasikan:
- **Spatial Machine Learning**: Memproyeksikan volume timbulan sampah (Ton) untuk 44 kecamatan di DKI Jakarta.
- **Live Environmental Intelligence**: Mengintegrasikan data curah hujan live dari Open-Meteo API.
- **Deterministic Operations Simulation**: Menghitung estimasi kebutuhan armada truk 15T compactor dan alokasi personel secara transparan.
- **5-Tier Data Provenance System**: Membedakan secara eksplisit data observasi, turunan, estimasi, prediksi AI, dan output simulasi.

---

## 2. Problem Statement

DKI Jakarta menghasilkan sekitar **7.500 – 9.000+ Ton sampah setiap hari** yang diangkut menuju TPST Bantargebang. Pengelolaan logistik persampahan menghadapi tantangan dinamis:
1. **Fluktuasi Cuaca**: Hujan deras meningkatkan bobot sampah basah dan memperlambat laju pengangkutan di jalan raya.
2. **Disparitas Spasial**: Tingkat timbulan sampah sangat bervariasi antara zona permukiman padat (misal: Cengkareng, Cakung) dan pusat komersial (misal: Tanah Abang, Menteng).
3. **Keterbatasan Fasilitas TPA**: TPST Bantargebang memerlukan perencanaan distribusi armada yang terukur untuk meminimalkan antrean truk dan kemacetan jalur transit.

---

## 3. Solution Architecture (Decoupled Engine)

AETERNA AI memisahkan secara tegas antara **Komponen Prediksi (Machine Learning)** dan **Komponen Simulasi Operasional (Deterministic Rules Engine)**:

```
+---------------------------------------------------------------------------------------------------+
|                                  AETERNA AI SYSTEM ARCHITECTURE                                   |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
                   +-------------------------------------------------------------+
                   |                 EXTERNAL & REFERENCE DATA                   |
                   |  - Open-Meteo API (Live Rainfall mm)          [OBSERVED]    |
                   |  - BPS DKI Jakarta (Resident Headcount)       [REFERENCE]   |
                   |  - Event & Transit Calendar                   [DERIVED]     |
                   +-------------------------------------------------------------+
                                                  |
                                                  v
                   +-------------------------------------------------------------+
                   |               PROVENANCE & FEATURE PIPELINE                 |
                   |  - Temporal Encoding (Day-of-week, Month, Weekend)          |
                   |  - Precipitation Lag & Mudik Window Indicators              |
                   |  - Spatial Normal Baseline Calibration                      |
                   +-------------------------------------------------------------+
                                                  |
                                                  v
                   +-------------------------------------------------------------+
                   |                 AI FORECAST ENGINE (LAYER 1)                |
                   |  - Stacking Regressor (DT + RF + GBR -> Ridge Meta-Learner) |
                   |  - Amazon Chronos-T5 (Tiny) Time-Series Neural Model        |
                   |                                                             |
                   |  OUTPUT: Forecast Volume (Tons) & 6-Material Composition    |
                   +-------------------------------------------------------------+
                                                  |
                                                  v
                   +-------------------------------------------------------------+
                   |            OPERATIONAL SIMULATION ENGINE (LAYER 2)          |
                   |             (Deterministic Mathematics / Non-AI)            |
                   |                                                             |
                   |  - Suggested Fleet = ceil(Volume / 14.25T) * 1.05 Buffer    |
                   |  - Crew Sizing = Active Trucks * 3 Personnel                |
                   |  - Collection Time = Volume / (Active Trucks * 2.0 Ton/Hr)  |
                   +-------------------------------------------------------------+
                                                  |
                                                  v
                   +-------------------------------------------------------------+
                   |             DECISION SUPPORT DASHBOARD (HUD UI)             |
                   |  (Leaflet Spatial Map, Provenance Badges, Analytics Panel)  |
                   +-------------------------------------------------------------+
```

---

## 4. Data Sources & 5-Tier Data Provenance System

Untuk menjaga integritas ilmiah dan akuntabilitas publik, setiap variabel data dalam AETERNA AI diklasifikasikan ke dalam 5 kategori formal:

| Kategori | Definisi | Contoh dalam Sistem |
| :--- | :--- | :--- |
| **`OBSERVED`** | Data yang diperoleh langsung dari pengukuran sensor atau API eksternal resmi | Curah Hujan Harian (Open-Meteo API) |
| **`DERIVED`** | Data yang dihitung secara matematis dari dataset terverifikasi | Fitur Lag Cuaca, Indikator Hari Kerja/Libur |
| **`ESTIMATED`** | Nilai baseline yang diestimasi karena sensor lapangan langsung belum tersedia | Baseline Timbulan Normal per Kecamatan |
| **`FORECAST`** | Nilai masa depan yang diproyeksikan oleh model Machine Learning | Estimasi Tonase Sampah Harian per Kecamatan |
| **`SIMULATION`** | Output skenario berbasis formula deterministik dan asumsi parameter | Kebutuhan Armada Truk 15T & Jumlah Kru |

### Katalog Sumber Data:
* **Open-Meteo API**: Live API curah hujan harian presisi koordinat latitude/longitude masing-masing kecamatan. (*Status: Active Live*).
* **BPS DKI Jakarta**: Data populasi jumlah jiwa per kecamatan. (*Status: Reference Data / Adapter Ready*).
* **SIPSN KLHK & DLH DKI Jakarta**: Data acuan tonase kota agregat. (*Status: Mode B Adapter Ready*).

---

## 5. Forecasting Machine Learning Engine

Model utama peramalan adalah **Stacking Regressor Ensemble**:
* **Base Estimators**:
  1. `DecisionTreeRegressor(max_depth=6)`
  2. `RandomForestRegressor(n_estimators=150, max_depth=6)`
  3. `GradientBoostingRegressor(n_estimators=150, max_depth=5, learning_rate=0.05)`
* **Meta-Learner**: `Ridge(alpha=1.0)`
* **Cross-Validation**: 3-fold temporal stacking cross-validation.
* **Fitur Input (11 Fitur)**: `Population_Jiwa`, `Normal_Avg_Ton`, `Zone_Type_Code`, `Rainfall_mm`, `Rain_Lag_1`, `Is_Weekend`, `Hari_Dalam_Minggu`, `Bulan`, `Is_Mudik`, `Ada_Event`, `Event_Crowd_Headcount`.

---

## 6. Deterministic Operational Simulation

Rekomendasi armada dan operasional dihitung secara deterministik (**bukan black-box AI**):
1. **Suggested Fleet**: Dihitung dari kapasitas muat efektif truk compactor 15 Ton dengan load factor 95% ($14.25	ext{ Ton/trip}$) ditambah buffer operasional 5%.
2. **Kebutuhan Personel**: Rasio standar 1 pengemudi + 2 petugas kebersihan per unit truk ($3	ext{ kru/truk}$).
3. **Estimasi Waktu Pengangkutan**: Berbasis throughput angkut ($2.0	ext{ Ton/jam/truk}$) yang disesuaikan dengan faktor koreksi cuaca dan kemacetan lalu lintas.

---

## 7. Model Evaluation (Development Benchmark)

> ⚠️ **Catatan Evaluasi**: Evaluasi berikut dilakukan di atas dataset simulasi pengembangan (*Mode A: Synthetic Development Dataset*) untuk pengujian fungsionalitas pipeline. Hasil ini **bukan** bukti akurasi operasional lapangan dunia nyata.

| Metrik Evaluasi | AETERNA Stacking Regressor | Baseline (Historical Mean) | Baseline (Rolling Mean 7D) |
| :--- | :---: | :---: | :---: |
| **MAE** | **`11.85 Ton`** | 48.20 Ton | 22.40 Ton |
| **RMSE** | **`15.42 Ton`** | 62.15 Ton | 29.80 Ton |
| **R² Score** | **`88.45%`** | 0.00% | 56.30% |
| **MAPE** | **`6.12%`** | 24.80% | 11.20% |

---

## 8. Status Validasi Ilmiah

* **Mode A — Development Benchmark**: **TERSEDIA & AKTIF** (Pengujian pipeline end-to-end pada dataset simulasi).
* **Mode B — Real-World Field Validation**: **BELUM TERSEDIA** (Memerlukan data pencatatan timbulan sampah harian aktual tingkat 44 kecamatan dari DLH DKI Jakarta).

---

## 9. Referensi REST API

Dokumentasi OpenAPI interaktif tersedia di `/docs`.

### 1. Endpoint Prediksi & Simulasi
* **POST** `/api/v1/predict`
  ```json
  {
    "location": "Menteng",
    "forecast_days": 7,
    "rainfall_mm": 0.0,
    "jumlah_jiwa": 88000,
    "model_type": "gradient_boosting",
    "granularity": "daily"
  }
  ```
* **Response**: Mengembalikan objek `prediction_results` (Forecast) dan `logistics_plan` (Simulation) lengkap dengan metadata data provenance.

### 2. Endpoint Autopilot & Monitoring
* **GET** `/api/v1/autopilot`: Ringkasan prakiraan 44 kecamatan hari ini.
* **GET** `/api/v1/alerts`: Wilayah dengan estimasi mendekati ambang batas kapasitas.
* **GET** `/api/v1/news`: Artikel referensi terkurasi seputar kebijakan persampahan Jakarta.
* **GET** `/status`: Status kesehatan servis dan arsitektur model aktif.

---

## 10. Panduan Instalasi & Menjalankan Lokal

```bash
# 1. Clone repository
git clone https://github.com/FARILtau72/Aeterna-Ai.git
cd Aeterna-Ai

# 2. Buat virtual environment & install dependensi
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

# 3. Jalankan unit test
python -m pytest tests/ -v

# 4. Jalankan aplikasi FastAPI
python -m uvicorn app:app --port 8001 --host 127.0.0.1
```
Buka browser pada `http://localhost:8001`.

---

## 11. Limitasi Sistem

1. **Ketiadaan Data Lapangan Harian Kecamatan**: DLH DKI Jakarta saat ini belum menyediakan data observasi timbulan sampah harian tingkat kecamatan melalui API publik.
2. **Asumsi Armada Bersifat Prototipe**: Kapasitas 15 Ton dan rasio kru merupakan asumsi pemodelan yang dapat disesuaikan dengan SOP dinas terkait.
3. **Prakiraan Cuaca**: Akurasi prakiraan curah hujan Open-Meteo menurun pada horizon di atas 7 hari.

---

## 12. Pengembang & Kontak

* **Lead Developer**: **Faril Putra Pratama** ([@FARILtau72](https://github.com/FARILtau72))
* **Web Portal**: [https://www.aeternaai.biz.id/](https://www.aeternaai.biz.id/)
* **LinkedIn**: [Faril Putra Pratama](https://www.linkedin.com/in/faril-putra-pratama-81561a280/)
* **Email**: `farilpratamap@gmail.com`

---

## 13. Lisensi

Proyek riset ini dirilis di bawah lisensi terbuka [MIT License](LICENSE).
