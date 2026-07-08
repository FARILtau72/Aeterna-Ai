# 🗑️ Panduan Integrasi API Waste Intelligence — Khusus Front-End (FE)
> **Sistem Prediksi Manajemen Sampah DKI Jakarta 2026**  
> **Target API Base URL (Lokal)**: `http://localhost:8001`  
> **Target API Base URL (Production)**: `https://huggingface.co/spaces/ALAMDIENG/waste-prediction-api`  

Dokumen ini disusun untuk memudahkan tim Front-End (FE) dalam mengintegrasikan endpoint backend dengan Dashboard UI, komponen Peta (Leaflet.js/Mapbox), Grafik (Recharts/ApexCharts/Chart.js), dan Sistem Alerts.

---

## 📑 Daftar Isi
1. [Konstanta & Data Spasial (Map & Coordinates)](#1-konstanta--data-spasial-map--coordinates)
2. [Definisi Tipe Data (TypeScript Interfaces)](#2-definisi-tipe-data-typescript-interfaces)
3. [Referensi Endpoint API](#3-referensi-endpoint-api)
   - [GET `/status` (Health Check)](#get-status-health-check)
   - [POST `/api/v1/predict` (Forecasting & Analisis)](#post-apiv1predict-forecasting--analisis)
   - [POST `/api/v1/predict/csv` (Export Data)](#post-apiv1predictcsv-export-data)
   - [GET `/api/v1/alerts` (Daftar Peringatan Hari Ini & H+2)](#get-apiv1alerts-daftar-peringatan-hari-ini--h2)
4. [Contoh Implementasi Code (Axios / Fetch)](#4-contoh-implementasi-code-axios--fetch)
5. [Panduan Mapping ke UI Dashboard](#5-panduan-mapping-ke-ui-dashboard)
6. [Penanganan Error & Validasi](#6-penanganan-error--validasi)

---

## 1. Konstanta & Data Spasial (Map & Coordinates)

Untuk memudahkan penggambaran Marker dan Garis Rute (Logistics Route) ke TPST Bantargebang di peta Leaflet.js, gunakan konstanta koordinat berikut di sisi klien.

```javascript
// Koordinat Utama Lokasi Pengamatan
export const LOCATION_COORDINATES = {
  "GBK": { latitude: -6.2183, longitude: 106.8022, radiusLabel: "2.0 km" },
  "JIS": { latitude: -6.1244, longitude: 106.8622, radiusLabel: "1.5 km" },
  "Pasar Senen": { latitude: -6.1744, longitude: 106.8444, radiusLabel: "1.2 km" },
  "Gang Sempit Tambora": { latitude: -6.1500, longitude: 106.8000, radiusLabel: "0.8 km" }
};

// Koordinat Pembuangan Akhir (Tempat Pembuangan Sampah Terpadu Bantargebang)
export const BANTARGEBANG_COORDS = { latitude: -6.3477, longitude: 106.9939 };

// Jarak & Waktu Tempuh Estimasi untuk UI Rute Logistik
export const LOGISTICS_ROUTING_PROFILES = {
  "JIS": { distance: "41.2 km", travelTime: "1.5 Jam" },
  "GBK": { distance: "38.5 km", travelTime: "1.8 Jam" },
  "Pasar Senen": { distance: "34.8 km", travelTime: "1.4 Jam" },
  "Gang Sempit Tambora": { distance: "43.5 km", travelTime: "2.1 Jam" }
};
```

> [!TIP]
> Gambar garis rute (logistik) dari koordinat lokasi terpilih langsung menuju `BANTARGEBANG_COORDS` menggunakan fitur `L.polyline` dengan style *dashed cyan glow* (`#00F0FF`) untuk memberikan kesan modern/cyberpunk.

---

## 2. Definisi Tipe Data (TypeScript Interfaces)

Jika Anda menggunakan TypeScript pada frontend (seperti React, Vue, atau Next.js), salin tipe data berikut:

```typescript
export type ModelType = 'chronos' | 'gradient_boosting';
export type Granularity = 'daily' | 'hourly';
export type RiskStatus = 'SAFE' | 'WARNING' | 'CRITICAL';
export type HourlyRiskIndicator = 'LOW' | 'MEDIUM' | 'HIGH';

export interface PredictionRequest {
  forecast_days: number;       // 1 - 30 hari
  rainfall_mm: number;         // Curah hujan manual (0 = Otomatis mengambil data live cuaca)
  event_scale: number;         // Skala keramaian buatan (0 = tidak ada, 5 = masif)
  location: 'JIS' | 'GBK' | 'Pasar Senen' | 'Gang Sempit Tambora';
  start_date?: string;         // Opsional, format YYYY-MM-DD
  granularity?: Granularity;   // Default: 'daily'
  model_type?: ModelType;      // Default: 'chronos'
}

export interface ConfidenceRange {
  lower: number;
  upper: number;
}

export interface HourlyBreakdown {
  hour: string;                // Format "00:00", "01:00", dsb.
  estimated_volume_ton: number;
  risk_indicator: HourlyRiskIndicator;
  confidence_range: ConfidenceRange;
}

export interface PredictionResult {
  date: string;                // YYYY-MM-DD
  location: string;
  total_volume_ton: number;
  organic_waste_ton: number;
  plastic_waste_ton: number;
  recommended_trucks: number;  // Truk kapasitas 5 ton
  risk_status: RiskStatus;
  event_info: string | null;   // Nama event terdekat (jika ada)
  hourly_breakdown: HourlyBreakdown[] | null; // Terisi jika granularity = 'hourly'
}

export interface LogisticsPlan {
  trucks_needed: number;
  manpower: number;            // 3 x jumlah armada truk
  estimated_duration_hours: number;
  efficiency_rate: string;     // Contoh: "85% (Optimal)"
}

export interface PredictionData {
  prediction_results: PredictionResult[];
  logistics_plan: LogisticsPlan;
}

export interface APIPredictionResponse {
  status: 'success' | 'error';
  message: string;
  confidence_score: number;    // Skala 0.0 - 1.0 (misal: 0.93)
  data: PredictionData;
}

export interface AlertItem {
  date: string;
  location: string;
  status: 'WARNING' | 'CRITICAL';
  estimated_volume_ton: number;
  message: string;
}

export interface APIAlertResponse {
  status: 'success';
  alert_count: number;
  alerts: AlertItem[];
  last_updated: string;        // ISO Timestamp
}
```

---

## 3. Referensi Endpoint API

### GET `/status` (Health Check)
Endpoint ini digunakan untuk memverifikasi apakah server menyala dan model AI sudah ter-load dengan benar di memori.

- **URL**: `/status`
- **Method**: `GET`
- **Response Contoh (200 OK)**:
  ```json
  {
    "status": "Online",
    "model_chronos": "Chronos-T5 Tiny",
    "model_gbr": "Gradient Boosting Regressor",
    "calibrated": true
  }
  ```

---

### POST `/api/v1/predict` (Forecasting & Analisis)
Endpoint utama untuk memanggil prediksi time-series model AI. AI akan menghitung dampak cuaca basah, event keramaian, status risiko per hari, rincian logistik, hingga dekomposisi sampah organik/plastik.

- **URL**: `/api/v1/predict`
- **Method**: `POST`
- **Headers**:
  - `Content-Type: application/json`
- **Request Body Contoh**:
  ```json
  {
    "forecast_days": 7,
    "rainfall_mm": 0,
    "event_scale": 0,
    "location": "JIS",
    "granularity": "hourly",
    "model_type": "gradient_boosting"
  }
  ```

- **Response Contoh (200 OK)**:
  ```json
  {
    "status": "success",
    "message": "Normal conditions.",
    "confidence_score": 0.9325,
    "data": {
      "prediction_results": [
        {
          "date": "2026-07-08",
          "location": "JIS",
          "total_volume_ton": 122.45,
          "organic_waste_ton": 61.07,
          "plastic_waste_ton": 28.1,
          "recommended_trucks": 25,
          "risk_status": "SAFE",
          "event_info": null,
          "hourly_breakdown": [
            {
              "hour": "00:00",
              "estimated_volume_ton": 2.45,
              "risk_indicator": "LOW",
              "confidence_range": {
                "lower": 2.08,
                "upper": 2.82
              }
            }
            // ... total 24 jam data
          ]
        }
      ],
      "logistics_plan": {
        "trucks_needed": 25,
        "manpower": 75,
        "estimated_duration_hours": 24.5,
        "efficiency_rate": "85% (Optimal)"
      }
    }
  }
  ```

---

### POST `/api/v1/predict/csv` (Export Data)
Endpoint ini mengembalikan data prediksi yang sama dengan di atas, tetapi langsung dikonversi menjadi file `.csv` yang siap diunduh di peramban pengguna.

- **URL**: `/api/v1/predict/csv`
- **Method**: `POST`
- **Headers**:
  - `Content-Type: application/json`
- **Response**: Mengembalikan raw bytes file stream (`text/csv`). Header response menyertakan `Content-Disposition: attachment; filename="waste_forecast_[lokasi]_[hari]d.csv"`.

---

### GET `/api/v1/alerts` (Daftar Peringatan Hari Ini & H+2)
Mengambil daftar titik lokasi yang mengalami lonjakan volume (di atas batas ambang aman) dalam 3 hari ke depan secara dinamis.

- **URL**: `/api/v1/alerts`
- **Method**: `GET`
- **Query Params**:
  - `location` (Opsional) : Untuk memfilter alert hanya untuk lokasi tertentu saja (misal: `JIS` / `GBK`).
- **Response Contoh (200 OK)**:
  ```json
  {
    "status": "success",
    "alert_count": 1,
    "alerts": [
      {
        "date": "2026-07-09",
        "location": "JIS",
        "status": "WARNING",
        "estimated_volume_ton": 168.5,
        "message": "Alert: WARNING volume expected at JIS"
      }
    ],
    "last_updated": "2026-07-08T10:15:30.123456"
  }
  ```

---

## 4. Contoh Implementasi Code (Axios / Fetch)

### Mengirim Request Prediksi & Update State (JavaScript / React)
```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001'; // Sesuaikan environment

export async function fetchWastePrediction(payload) {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/v1/predict`, payload);
    return response.data;
  } catch (error) {
    console.error("Error predicting waste volume:", error.response?.data || error.message);
    throw error;
  }
}
```

### Mengunduh CSV File (JavaScript)
```javascript
export async function downloadPredictionCSV(payload) {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/v1/predict/csv`, payload, {
      responseType: 'blob' // Wajib diisi agar file blob dibaca dengan benar
    });
    
    // Trigger download manual via browser
    const blob = new Blob([response.data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    
    // Nama file dinamis
    const fileName = `waste_forecast_${payload.location.replace(/\s+/g, '_')}_${payload.forecast_days}d.csv`;
    link.setAttribute('download', fileName);
    
    document.body.appendChild(link);
    link.click();
    
    // Bersihkan link element setelah click
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Gagal mengunduh CSV:", error);
    alert("Ekspor CSV Gagal!");
  }
}
```

---

## 5. Panduan Mapping ke UI Dashboard

### A. Total Volume & Kebutuhan Armada
1. **Total Volume Forecast**: Lakukan perulangan (`reduce`) untuk menjumlahkan `total_volume_ton` dari semua entri di `data.prediction_results`. Tampilkan nilai desimal 2 angka (`.toFixed(2)`).
2. **Kebutuhan Fleet (Truk)**: Tampilkan `data.logistics_plan.trucks_needed`. Truk dihitung secara kumulatif dengan kapasitas angkut maksimal 5 Ton per armada.
3. **Tenaga Kerja (Manpower)**: Ditampilkan dari `data.logistics_plan.manpower`. Angka ini adalah alokasi aman kru operasional (3 orang per truk).

### B. Komposisi Sampah (Organic & Plastic)
Hitung persentase dinamis untuk di-render pada UI *Progress Bar*:
```javascript
// Hitung jumlah tonase terlebih dahulu
const totalOrganic = results.reduce((acc, c) => acc + c.organic_waste_ton, 0);
const totalPlastic = results.reduce((acc, c) => acc + c.plastic_waste_ton, 0);
const totalVol = results.reduce((acc, c) => acc + c.total_volume_ton, 0);

// Hitung persentase relatif
const organicPct = totalVol > 0 ? (totalOrganic / totalVol) * 100 : 0;
const plasticPct = totalVol > 0 ? (totalPlastic / totalVol) * 100 : 0;

// Render ke UI
// Ganti properti width progress bar inline style / css variable
document.getElementById('bar-organic').style.width = `${organicPct}%`;
document.getElementById('bar-plastic').style.width = `${plasticPct}%`;
```

### C. Penentuan Status Risiko (Risk Status)
Backend mengembalikan status per hari: `'SAFE'`, `'WARNING'`, atau `'CRITICAL'`.
Untuk menentukan status risiko keseluruhan periode yang dipilih:
- Ambil status **tertinggi** yang muncul di sepanjang list hari prediksi.
- Aturan Prioritas Status: `CRITICAL` > `WARNING` > `SAFE`.
- Berikan penyesuaian style warna badge:
  - `SAFE`: Hijau terang (`#00E676`)
  - `WARNING`: Kuning neon (`#FFD600`)
  - `CRITICAL`: Merah menyala (`#FF1744`)

### D. Weather Integration (Live BMKG)
Saat user memilih lokasi baru:
1. Hubungi BMKG/Open-Meteo API di sisi FE menggunakan koordinat lokasi (lihat [Bagian 1](#1-konstanta--data-spasial-map--coordinates)).
2. Dapatkan nilai curah hujan hari ini (`precipitation_sum` / `precipitation`).
3. Tampilkan status peringatan hujan di UI:
   - Curah Hujan `> 30 mm` ➡️ Tampilkan badge **HEAVY RAIN 🟡**
   - Curah Hujan `> 50 mm` ➡️ Tampilkan badge **FLOOD DANGER 🔴**
   - Di bawah itu ➡️ Tampilkan **Normal conditions**

---

## 6. Penanganan Error & Validasi

Backend menggunakan Pydantic v2 untuk memvalidasi request body secara ketat.

### HTTP 422 Unprocessable Entity
Terjadi jika payload yang dikirimkan memiliki tipe data yang salah atau data di luar rentang validasi.
*Contoh error respon*:
```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["body", "forecast_days"],
      "msg": "Input should be less than or equal to 30",
      "input": 45
    }
  ]
}
```
**Tips FE**: Batasi input `forecast_days` menggunakan komponen slider HTML `min="1" max="30"` untuk menghindari error ini.

### HTTP 503 Service Unavailable
Terjadi jika startup server belum selesai me-load model Amazon Chronos atau file CSV belum siap di sisi backend.
**Tips FE**: Sediakan visual loader atau spinner yang menarik di dashboard untuk mencegah interaksi klik ganda saat status server menunjukkan pemuatan ulang aset AI.

---

> 💡 **Kontak Developer Backend**:  
> **Faril Putra Pratama** (SMK Taruna Bangsa)  
> Hubungi via repository GitHub di: [@FARILtau72](https://github.com/FARILtau72) jika Anda membutuhkan endpoint tambahan atau perubahan format respon!
