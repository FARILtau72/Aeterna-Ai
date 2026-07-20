# Aeterna AI - Backend Architecture & ML Engine Documentation (v4.0.0)

Dokumen ini menjelaskan detail teknis arsitektur sistem backend, model machine learning (Gradient Boosting & Amazon Chronos), rekayasa fitur (*feature engineering*), serta panduan kontainerisasi dan *deployment* untuk **Aeterna AI (Waste Intelligence Platform)**.

---

## 🏗️ 1. Desain Arsitektur Backend

Backend Aeterna AI dibangun menggunakan **FastAPI (Python)**, sebuah kerangka kerja web asinkron dengan performa tinggi yang setara dengan Node.js dan Go.

```
+-----------------------------------------------------------------+
|                        FASTAPI BACKEND                          |
|                                                                 |
|  [ /api/v1/predict ]      [ /api/v1/autopilot ]   [ /api/v1/news ]
|          |                         |                     |      |
|          v                         v                     |      |
|  +---------------+        +------------------+           |      |
|  |  Chronos T5   |        |  GBR Model       |           |      |
|  |  Transformer  |        |  (GridSearchCV)  |           |      |
|  +---------------+        +------------------+           |      |
|          |                         |                     |      |
|          +------------+------------+                     |      |
|                       |                                  |      |
|                       v                                  v      |
|            +-----------------------+           +-------------+  |
|            | Feature Engineering   |           | News DB     |  |
|            | - Weather (OpenMeteo) |           | (JSON)      |  |
|            | - Event Multipliers   |           +-------------+  |
|            | - Spatial Calibration |                            |
|            +-----------------------+                            |
+-----------------------------------------------------------------+
```

### Komponen Utama:
1.  **Asynchronous Handling**: Memanfaatkan FastAPI dengan `run_in_threadpool` untuk menjalankan inferensi deep learning (Chronos Transformer) tanpa memblokir thread event loop utama.
2.  **CORS Security Middleware**: Dikonfigurasi secara wildcard (`*`) untuk mengizinkan aplikasi client-side (seperti dashboard Vercel) melakukan kueri asinkron lintas asal (*cross-origin*).
3.  **Automatic Swagger Docs**: Endpoint mendefinisikan tipe data masukan menggunakan model **Pydantic** yang secara otomatis membuat spesifikasi OpenAPI dan dokumentasi interaktif di `/docs`.

---

## 🧠 2. Mesin Machine Learning (ML Engine)

Aeterna AI mengadopsi arsitektur model hibrida:

### A. Gradient Boosting Regressor (GBR) - Model Prediksi Harian
Model regresi teroptimasi yang memprediksi volume timbulan sampah harian tingkat kecamatan berdasarkan fitur-fitur spasial dan kontekstual.
*   **Hyperparameter Terbaik (GridSearchCV)**:
    *   `n_estimators` (Jumlah pohon keputusan): **100**
    *   `learning_rate` (Laju pembelajaran): **0.03**
    *   `max_depth` (Kedalaman pohon maksimal): **3**
    *   `subsample` (Rasio sampel acak per pohon): **0.9**
*   **Metrik Evaluasi Model**:
    *   **Mean Absolute Error (MAE)**: `132.29 Ton` (Rata-rata kesalahan tebakan sekitar 132 ton).
    *   **Root Mean Squared Error (RMSE)**: `165.46 Ton` (Tebakan stabil tanpa kesalahan ekstrem).
    *   **R-Squared ($R^2$ Score)**: `81.51%` (81.5% pola data berhasil dijelaskan oleh fitur).
    *   **Mean Absolute Percentage Error (MAPE)**: **`1.59%`** (Tingkat persentase kesalahan di bawah 2%, masuk kategori *Highly Accurate Forecasting*).

### B. Amazon Chronos-T5 (Tiny) - Model Deret Waktu (Time-Series)
Model Transformer terlatih dari Amazon yang digunakan untuk memprediksi tren masa depan 7 s.d. 30 hari ke depan pada kueri simulasi. Chronos membaca barisan data historis dan melakukan peramalan probabilistik (diambil kuantil median `0.5`).

---

## 🌦️ 3. Rekayasa Fitur Dinamis (Feature Engineering)

AI mengalibrasi prediksi mentah berdasarkan faktor riil eksternal:

### A. Multiplier Curah Hujan (Rainfall Multiplier)
Sampah terbuka di Tempat Penampungan Sementara (TPS) menyerap air hujan, yang meningkatkan berat massa jenis sampah basah.
*   Sistem memanggil **Open-Meteo API** secara dinamis menggunakan titik koordinat presisi dari kecamatan target.
*   **Multiplier Formula**:
    $$\text{Volume}_{\text{calibrated}} = \text{Volume}_{\text{pred}} \times \left(1.0 + \frac{\text{Precipitation (mm)}}{1000} \right)$$
    *Curah hujan lebat (misal 50 mm) akan menambah berat jenis timbulan sekitar 5%.*

### B. Multiplier Skala Keramaian & Event (Event Multiplier)
Jadwal acara besar Jakarta (`event_jakarta_2026.txt`) dipindai secara berkala berdasarkan tanggal kueri.
*   Jika ada event aktif, sistem mendeteksi nama acara dan skala keramaian (1 s.d. 5).
*   **Skala Multiplier**:
    *   Skala 1 s.d. 2 (Keramaian lokal): **+10% s.d. +15%** volume sampah.
    *   Skala 3 s.d. 4 (Keramaian regional, misal BTN Marathon): **+20% s.d. +25%** volume sampah.
    *   Skala 5 (Keramaian masif, misal Idul Fitri): **+30% s.d. +35%** volume sampah.

---

## ⏰ 4. Timezone-Aware Engine (WIB / Asia/Jakarta)

Agar hasil prediksi antara server lokal pengembang dan server Hugging Face (yang biasanya berlokasi di Amerika Serikat) sinkron 100%, backend Aeterna AI dilengkapi dengan pengunci zona waktu WIB (UTC+7):

```python
from datetime import datetime, timezone, timedelta

def get_jakarta_now() -> datetime:
    # Memaksa system time menggunakan Waktu Indonesia Barat (WIB)
    return datetime.now(timezone(timedelta(hours=7)))
```
Semua query default, pencocokan kalender event, serta umpan berita menggunakan `get_jakarta_now()` untuk mencegah pergeseran penanggalan akibat perbedaan lokasi server fisik.

---

## 🐳 5. Panduan Kontainerisasi & Deployment (Hugging Face Spaces)

Aplikasi dideploy ke **Hugging Face Spaces** menggunakan **Docker**.

### Berkas Dockerfile:
```dockerfile
FROM python:3.11-slim

# System setup
WORKDIR /code
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port (Hugging Face standard port)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Langkah Deployment ke Hugging Face:
1.  Buat Space baru di Hugging Face, pilih SDK **Docker** (Blank template).
2.  Tambahkan remote git Hugging Face ke repositori lokal Anda:
    ```bash
    git remote add huggingface https://huggingface.co/spaces/USERNAME/SPACE_NAME
    ```
3.  Dorong perubahan langsung ke Space:
    ```bash
    git push huggingface main
    ```
4.  Hugging Face akan mendeteksi `Dockerfile`, membangun *image*, dan menyalakan API pada port `7860` secara otomatis.

---

## 📰 6. Dokumentasi API Berita Dinamis (Dynamic News API)

Endpoint ini menyediakan umpan berita terbaru mengenai tata kelola sampah di DKI Jakarta yang dihasilkan secara dinamis melalui integrasi LLM (Conduit API) dan terproteksi oleh sistem penyimpanan cadangan (*caching*) lokal.

### A. Spesifikasi Endpoint
*   **Path**: `/api/v1/news`
*   **Method**: `GET`
*   **Response Model**: `List[NewsItem]`
*   **Deskripsi**: Mengambil minimal 10 artikel berita persampahan terhangat yang dirilis paling lama 1 minggu dari tanggal kueri. 

### B. Mekanisme Keandalan (Reliability Mechanism)
Untuk menjamin tingkat kegagalan layanan 0% (*zero downtime*), sistem diimplementasikan menggunakan arsitektur bercabang (*fallback structure*):

```
                       [ GET /api/v1/news ]
                                |
                                v
                   +-------------------------+
                   |  Panggil Conduit LLM    |
                   |  (GPT-4o-Mini API)      |
                   +-------------------------+
                                |
                   +------------+------------+
                   |                         |
            (Status 200)               (Timeout/Error/402)
                   |                         |
                   v                         v
       +-----------------------+   +-----------------------+
       | - Ambil Data Baru     |   | - Baca Backup Cache   |
       | - Tulis ke JSON Cache |   |   (latest_waste_news) |
       | - Kembalikan Response |   | - Kembalikan Response |
       +-----------------------+   +-----------------------+
```

1.  **AI Crawl Mode**: Backend akan memanggil API LLM (Conduit) secara asinkron dengan batas waktu (*timeout*) 8.0 detik. AI diarahkan untuk membuat artikel berita riil/valid dengan rentang tanggal maksimum 7 hari ke belakang dari tanggal hari ini.
2.  **JSON Database Backup**: Jika API eksternal mengalami kendala jaringan, melebihi kuota (Error 402/Free Plan Limit), atau mati, sistem secara otomatis mengalihkan permintaan untuk membaca data statis valid yang tersimpan di berkas `latest_waste_news.json` tanpa mengganggu kelancaran dashboard frontend.

### C. Skema Respons (JSON Schema)
Setiap objek berita dalam array memiliki struktur data sebagai berikut:

| Nama Field | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `title` | `string` | Judul berita persampahan DKI Jakarta |
| `source` | `string` | Nama penerbit berita resmi (misal: Kompas.com, Antara News) |
| `url` | `string` | Tautan/URL artikel asli berita |
| `date_fetched` | `string` | Tanggal penulisan/pengambilan berita (Format: `YYYY-MM-DD`) |
| `summary` | `string` | Ringkasan isi berita dan tindak lanjut penanganan sampah |

#### Contoh JSON Output:
```json
[
  {
    "title": "DLH DKI Jakarta Wajibkan Pemilahan Sampah Rumah Tangga Mulai 1 Agustus 2026",
    "source": "Kompas.com",
    "url": "https://megapolitan.kompas.com/read/2026/07/12/dlh-dki-wajibkan-pemilahan-sampah-rumah-tangga",
    "date_fetched": "2026-07-12",
    "summary": "Dinas Lingkungan Hidup DKI Jakarta resmi mensosialisasikan Instruksi Gubernur No. 5 Tahun 2026 tentang kewajiban pilah sampah dari rumah guna mengurangi pasokan sampah ke TPST Bantargebang per 1 Agustus 2026."
  }
]
```
