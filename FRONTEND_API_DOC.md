# Aeterna AI - Front-End API Integration Guide (v4.0.0)

Dokumen ini ditujukan bagi tim Front-End untuk mengintegrasikan antarmuka pengguna dengan backend **Aeterna AI (Waste Intelligence Platform)**.

---

## 📡 Konfigurasi Global
*   **Base URL (Local)**: `http://localhost:8001`
*   **Content-Type**: `application/json`
*   **CORS**: Diaktifkan secara wildcard (`*`) untuk semua origin, method, dan header.

---

## 🗺️ Konstanta Wilayah (44 Kecamatan DKI Jakarta)
Untuk memetakan wilayah pada leaflet/map atau drop-down pilihan di FE, gunakan konstanta koordinat dan baseline berikut:

```typescript
export interface RegionMetadata {
  latitude: number;
  longitude: number;
  normal_avg: number;
  warning_threshold: number;
  critical_threshold: number;
  city: 'Jakarta Pusat' | 'Jakarta Utara' | 'Jakarta Barat' | 'Jakarta Selatan' | 'Jakarta Timur' | 'Kepulauan Seribu';
}

export const KECAMATAN_DATABASE: Record<string, RegionMetadata> = {
  // JAKARTA PUSAT
  "Menteng": { latitude: -6.1950, longitude: 106.8322, normal_avg: 120.0, warning_threshold: 160.0, critical_threshold: 180.0, city: "Jakarta Pusat" },
  "Senen": { latitude: -6.1822, longitude: 106.8452, normal_avg: 180.0, warning_threshold: 220.0, critical_threshold: 240.0, city: "Jakarta Pusat" },
  "Cempaka Putih": { latitude: -6.1802, longitude: 106.8686, normal_avg: 90.0, warning_threshold: 120.0, critical_threshold: 140.0, city: "Jakarta Pusat" },
  "Johar Baru": { latitude: -6.1866, longitude: 106.8572, normal_avg: 70.0, warning_threshold: 95.0, critical_threshold: 110.0, city: "Jakarta Pusat" },
  "Kemayoran": { latitude: -6.1628, longitude: 106.8438, normal_avg: 180.0, warning_threshold: 220.0, critical_threshold: 240.0, city: "Jakarta Pusat" },
  "Sawah Besar": { latitude: -6.1554, longitude: 106.8322, normal_avg: 110.0, warning_threshold: 145.0, critical_threshold: 165.0, city: "Jakarta Pusat" },
  "Tanah Abang": { latitude: -6.2104, longitude: 106.8122, normal_avg: 250.0, warning_threshold: 320.0, critical_threshold: 350.0, city: "Jakarta Pusat" },
  "Gambir": { latitude: -6.1764, longitude: 106.8190, normal_avg: 150.0, warning_threshold: 195.0, critical_threshold: 215.0, city: "Jakarta Pusat" },

  // JAKARTA UTARA
  "Penjaringan": { latitude: -6.1264, longitude: 106.7822, normal_avg: 280.0, warning_threshold: 350.0, critical_threshold: 380.0, city: "Jakarta Utara" },
  "Tanjung Priok": { latitude: -6.1322, longitude: 106.8722, normal_avg: 260.0, warning_threshold: 320.0, critical_threshold: 350.0, city: "Jakarta Utara" },
  "Koja": { latitude: -6.1214, longitude: 106.9133, normal_avg: 190.0, warning_threshold: 240.0, critical_threshold: 270.0, city: "Jakarta Utara" },
  "Cilincing": { latitude: -6.1288, longitude: 106.9452, normal_avg: 290.0, warning_threshold: 370.0, critical_threshold: 400.0, city: "Jakarta Utara" },
  "Pademangan": { latitude: -6.1328, longitude: 106.8422, normal_avg: 140.0, warning_threshold: 180.0, critical_threshold: 200.0, city: "Jakarta Utara" },
  "Kelapa Gading": { latitude: -6.1552, longitude: 106.9022, normal_avg: 190.0, warning_threshold: 240.0, critical_threshold: 270.0, city: "Jakarta Utara" },

  // JAKARTA BARAT
  "Cengkareng": { latitude: -6.1528, longitude: 106.7322, normal_avg: 340.0, warning_threshold: 420.0, critical_threshold: 460.0, city: "Jakarta Barat" },
  "Grogol Petamburan": { latitude: -6.1622, longitude: 106.7882, normal_avg: 220.0, warning_threshold: 280.0, critical_threshold: 310.0, city: "Jakarta Barat" },
  "Kalideres": { latitude: -6.1428, longitude: 106.7022, normal_avg: 260.0, warning_threshold: 330.0, critical_threshold: 360.0, city: "Jakarta Barat" },
  "Kebon Jeruk": { latitude: -6.1922, longitude: 106.7722, normal_avg: 210.0, warning_threshold: 260.0, critical_threshold: 290.0, city: "Jakarta Barat" },
  "Kembangan": { latitude: -6.1828, longitude: 106.7382, normal_avg: 180.0, warning_threshold: 230.0, critical_threshold: 250.0, city: "Jakarta Barat" },
  "Palmerah": { latitude: -6.2028, longitude: 106.7882, normal_avg: 160.0, warning_threshold: 200.0, critical_threshold: 220.0, city: "Jakarta Barat" },
  "Taman Sari": { latitude: -6.1454, longitude: 106.8182, normal_avg: 100.0, warning_threshold: 130.0, critical_threshold: 150.0, city: "Jakarta Barat" },
  "Tambora": { latitude: -6.1500, longitude: 106.8000, normal_avg: 80.0, warning_threshold: 110.0, critical_threshold: 125.0, city: "Jakarta Barat" },

  // JAKARTA SELATAN
  "Cilandak": { latitude: -6.2928, longitude: 106.7922, normal_avg: 180.0, warning_threshold: 230.0, critical_threshold: 250.0, city: "Jakarta Selatan" },
  "Jagakarsa": { latitude: -6.3328, longitude: 106.8222, normal_avg: 220.0, warning_threshold: 280.0, critical_threshold: 310.0, city: "Jakarta Selatan" },
  "Kebayoran Baru": { latitude: -6.2422, longitude: 106.7982, normal_avg: 210.0, warning_threshold: 260.0, critical_threshold: 290.0, city: "Jakarta Selatan" },
  "Kebayoran Lama": { latitude: -6.2488, longitude: 106.7722, normal_avg: 230.0, warning_threshold: 290.0, critical_threshold: 320.0, city: "Jakarta Selatan" },
  "Mampang Prapatan": { latitude: -6.2522, longitude: 106.8182, normal_avg: 120.0, warning_threshold: 150.0, critical_threshold: 170.0, city: "Jakarta Selatan" },
  "Pancoran": { latitude: -6.2622, longitude: 106.8382, normal_avg: 130.0, warning_threshold: 160.0, critical_threshold: 180.0, city: "Jakarta Selatan" },
  "Pasar Minggu": { latitude: -6.2828, longitude: 106.8438, normal_avg: 240.0, warning_threshold: 300.0, critical_threshold: 330.0, city: "Jakarta Selatan" },
  "Pesanggrahan": { latitude: -6.2588, longitude: 106.7588, normal_avg: 160.0, warning_threshold: 200.0, critical_threshold: 220.0, city: "Jakarta Selatan" },
  "Setiabudi": { latitude: -6.2228, longitude: 106.8282, normal_avg: 190.0, warning_threshold: 240.0, critical_threshold: 270.0, city: "Jakarta Selatan" },
  "Tebet": { latitude: -6.2288, longitude: 106.8482, normal_avg: 170.0, warning_threshold: 210.0, critical_threshold: 230.0, city: "Jakarta Selatan" },

  // JAKARTA TIMUR
  "Cakung": { latitude: -6.1828, longitude: 106.9482, normal_avg: 350.0, warning_threshold: 430.0, critical_threshold: 470.0, city: "Jakarta Timur" },
  "Cipayung": { latitude: -6.3128, longitude: 106.9022, normal_avg: 140.0, warning_threshold: 180.0, critical_threshold: 200.0, city: "Jakarta Timur" },
  "Ciracas": { latitude: -6.3228, longitude: 106.8782, normal_avg: 190.0, warning_threshold: 240.0, critical_threshold: 270.0, city: "Jakarta Timur" },
  "Duren Sawit": { latitude: -6.2228, longitude: 106.9282, normal_avg: 300.0, warning_threshold: 370.0, critical_threshold: 410.0, city: "Jakarta Timur" },
  "Jatinegara": { latitude: -6.2222, longitude: 106.8682, normal_avg: 240.0, warning_threshold: 300.0, critical_threshold: 330.0, city: "Jakarta Timur" },
  "Kramat Jati": { latitude: -6.2722, longitude: 106.8682, normal_avg: 220.0, warning_threshold: 270.0, critical_threshold: 300.0, city: "Jakarta Timur" },
  "Makasar": { latitude: -6.2622, longitude: 106.8782, normal_avg: 160.0, warning_threshold: 200.0, critical_threshold: 220.0, city: "Jakarta Timur" },
  "Matraman": { latitude: -6.2022, longitude: 106.8582, normal_avg: 130.0, warning_threshold: 160.0, critical_threshold: 180.0, city: "Jakarta Timur" },
  "Pasar Rebo": { latitude: -6.3122, longitude: 106.8522, normal_avg: 150.0, warning_threshold: 190.0, critical_threshold: 210.0, city: "Jakarta Timur" },
  "Pulo Gadung": { latitude: -6.1922, longitude: 106.8922, normal_avg: 220.0, warning_threshold: 270.0, critical_threshold: 300.0, city: "Jakarta Timur" },

  // KEPULAUAN SERIBU
  "Kepulauan Seribu Utara": { latitude: -5.5722, longitude: 106.5522, normal_avg: 11.0, warning_threshold: 15.0, critical_threshold: 18.0, city: "Kepulauan Seribu" },
  "Kepulauan Seribu Selatan": { latitude: -5.7722, longitude: 106.6522, normal_avg: 9.0, warning_threshold: 12.0, critical_threshold: 15.0, city: "Kepulauan Seribu" }
};
```

---

## 🔌 Referensi API Endpoint

### 1. Mengambil Berita Ter-crawled Harian
Endpoint ini menyajikan database berita seputar persampahan DKI Jakarta yang diperbarui berkala setiap 1 jam.

*   **URL**: `/api/v1/news`
*   **Method**: `GET`
*   **Headers**: `Accept: application/json`
*   **Response Schema (`200 OK`)**:
    ```json
    [
      {
        "title": "DKI Uji Coba Penarikan Retribusi Sampah Pelayanan Kebersihan Harian",
        "source": "Antara News",
        "url": "https://www.antaranews.com/tag/sampah-jakarta",
        "date_fetched": "2026-07-10",
        "summary": "Pemprov DKI Jakarta merencanakan uji coba penarikan retribusi pelayanan kebersihan/sampah berdasarkan golongan daya listrik..."
      }
    ]
    ```

---

### 2. Prediksi AI Otonom (Autopilot Mode)
Mengambil prediksi otonom untuk ke-44 kecamatan sekaligus untuk hari ini. Berguna untuk dashboard autopilot utama.

*   **URL**: `/api/v1/autopilot`
*   **Method**: `GET`
*   **Response Schema (`200 OK`)**:
    ```json
    {
      "status": "success",
      "date": "2026-07-10",
      "total_volume_ton": 8105.42,
      "total_trucks": 1640,
      "top_kecamatan": [
        {
          "location": "Cakung",
          "volume_ton": 355.20,
          "trucks": 72,
          "status": "SAFE",
          "city": "Jakarta Timur"
        }
      ],
      "rainy_regions": 0,
      "event_today": null
    }
    ```

---

### 3. Simulasi Prediksi Wilayah (Predictor Tool)
Melakukan peramalan timbulan sampah untuk kecamatan tertentu dengan parameter simulasi cuaca/event keramaian.

*   **URL**: `/api/v1/predict`
*   **Method**: `POST`
*   **Request Body**:
    ```typescript
    interface PredictionRequest {
      forecast_days: number;       // Ambang batas: 1 - 30 hari
      rainfall_mm: number;         // Curah hujan override (0.0 = Auto Open-Meteo)
      event_scale: number;         // 0 (none) sampai 5 (massive crowd)
      location: string;            // Salah satu nama dari 44 kecamatan
      granularity: 'daily' | 'hourly';
      model_type: 'chronos' | 'gradient_boosting';
    }
    ```
*   **Contoh Request Payload**:
    ```json
    {
      "forecast_days": 7,
      "rainfall_mm": 0.0,
      "event_scale": 0,
      "location": "Menteng",
      "granularity": "daily",
      "model_type": "gradient_boosting"
    }
    ```
*   **Response Schema (`200 OK`)**:
    ```json
    {
      "status": "success",
      "message": "Normal conditions.",
      "confidence_score": 0.9828,
      "data": {
        "prediction_results": [
          {
            "date": "2026-07-10",
            "location": "Menteng",
            "total_volume_ton": 120.54,
            "organic_waste_ton": 60.11,
            "plastic_waste_ton": 27.66,
            "paper_waste_ton": 13.86,
            "glass_waste_ton": 3.86,
            "metal_waste_ton": 2.53,
            "textile_waste_ton": 5.06,
            "other_waste_ton": 7.46,
            "recommended_trucks": 25,
            "risk_status": "SAFE",
            "event_info": null,
            "hourly_breakdown": null
          }
        ],
        "logistics_plan": {
          "trucks_needed": 25,
          "manpower": 75,
          "estimated_duration_hours": 24.1,
          "efficiency_rate": "85% (Optimal)"
        }
      }
    }
    ```

---

### 4. Unduh Berkas CSV Prediksi
Mengunduh berkas tabel data hasil simulasi prediksi.

*   **URL**: `/api/v1/predict/csv`
*   **Method**: `POST`
*   **Request Body**: Sama dengan request `/api/v1/predict`
*   **Response**: Binary Blob (`text/csv` stream file).

---

### 5. Mengambil Peringatan Operasional Dinamis (Alerts)
Mendapatkan peringatan kritis wilayah yang volumenya melebihi ambang batas warning/critical.

*   **URL**: `/api/v1/alerts`
*   **Method**: `GET`
*   **Query Parameters**: `location` (opsional, untuk menyaring satu kecamatan)
*   **Response Schema (`200 OK`)**:
    ```json
    {
      "status": "success",
      "alert_count": 2,
      "alerts": [
        {
          "date": "2026-07-10",
          "location": "Cakung",
          "status": "WARNING",
          "estimated_volume_ton": 435.0,
          "message": "Alert: WARNING volume expected at Cakung"
        }
      ],
      "last_updated": "2026-07-10T20:52:00.123456"
    }
    ```

---

## ⚡ Contoh Integrasi Frontend (Axios / JavaScript)

Berikut adalah contoh cara menarik data prediksi Autopilot dan memuatnya ke komponen halaman FE Anda:

```javascript
import axios from 'axios';

const BACKEND_URL = 'http://localhost:8001';

// 1. Memuat Umpan Berita AI
export async function getWasteNews() {
  try {
    const res = await axios.get(`${BACKEND_URL}/api/v1/news`);
    return res.data; // Mengembalikan array berita
  } catch (error) {
    console.error("Gagal menarik berita sampah:", error);
    return [];
  }
}

// 2. Memuat Data Autopilot Otonom DKI
export async function getAutopilotData() {
  try {
    const res = await axios.get(`${BACKEND_URL}/api/v1/autopilot`);
    return res.data;
  } catch (error) {
    console.error("Gagal memuat autopilot data:", error);
    return null;
  }
}

// 3. Menjalankan Prediksi Manual (Simulation)
export async function postSimulationPrediction(kecamatan, hari = 7, model = 'gradient_boosting') {
  const payload = {
    forecast_days: hari,
    rainfall_mm: 0.0, // Auto
    event_scale: 0,
    location: kecamatan,
    granularity: hari <= 7 ? 'hourly' : 'daily',
    model_type: model
  };

  try {
    const res = await axios.post(`${BACKEND_URL}/api/v1/predict`, payload);
    return res.data;
  } catch (error) {
    console.error("Gagal melakukan prediksi simulasi:", error);
    throw error;
  }
}
```
