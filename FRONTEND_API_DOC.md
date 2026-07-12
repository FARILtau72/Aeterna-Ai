# Aeterna AI - Front-End API Integration & UI Development Guide (v4.0.0)

Dokumen ini ditujukan sebagai panduan bagi developer Front-End (FE) untuk mengintegrasikan antarmuka pengguna dengan backend **Aeterna AI (Waste Intelligence Platform)**, menjelaskan konfigurasi perutean, Leaflet map, interaktivitas, dan visualisasi chart.

---

## 📡 1. Konfigurasi Dynamic Routing & Vercel Compatibility

Untuk memastikan frontend dapat dipublikasikan secara terpisah di **Vercel** dan berkomunikasi secara aman dengan API backend di **Hugging Face Spaces**, perutean URL disetel secara dinamis di `frontend/app.js`:

```javascript
// Deteksi otomatis domain client untuk perutean API
const API_BASE_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "" // Menggunakan path relatif jika berjalan di lokal (localhost)
    : "https://alamdieng-waste-prediction-api.hf.space"; // Mengarah langsung ke API Hugging Face jika di-host di Vercel
```
Semua pemanggilan AJAX `fetch()` harus menggunakan template literal `${API_BASE_URL}` (contoh: `fetch(`${API_BASE_URL}/api/v1/news`)`).

---

## 🗺️ 2. Integrasi Leaflet Map & Custom Markers

Peta interaktif menggunakan **Leaflet.js** untuk memvisualisasikan timbulan sampah di 44 kecamatan:

### A. Pengelompokan Kelas Risiko Spasial
Tiap penanda (marker) kecamatan di peta memiliki kelas CSS dinamis berdasarkan tingkat bahayanya:
*   `.safe`: Warna hijau (`--green`), menyala redup.
*   `.warning`: Warna kuning (`--yellow`), berdenyut sedang.
*   `.critical`: Warna merah (`--red`), berdenyut kencang.

### B. Route Drawing & Haversine Formula
Ketika penanda kecamatan diklik, rute pengiriman logistik langsung digambar ke **TPST Bantargebang** (`[-6.3477, 106.9939]`):
```javascript
// polyline digambar putus-putus berwarna cyan bercahaya
routeLine = L.polyline([startCoords, BANTARGEBANG_COORDS], {
    color: '#00F0FF',
    weight: 3.5,
    opacity: 0.75,
    dashArray: '8, 8',
    className: 'glowing-route'
}).addTo(map);
```

---

## 🖱️ 3. Interaktivitas Cyber HUD & Custom Cursor

UI terinspirasi dari `floodzy.id` menggunakan kursor delay kustom di desktop:

### A. Animasi Kursor Lerp (Linear Interpolation)
Kursor dibagi menjadi dua bagian: titik tengah (`#cursor-dot`) dan cincin luar (`#cursor-ring`). Cincin luar bergerak mengikuti kursor dengan sedikit delay menggunakan rumus interpolasi lerp:
```javascript
// Lerp formula untuk pergerakan cincin kursor yang smooth
ringX += (mouseX - ringX) * 0.15;
ringY += (mouseY - ringY) * 0.15;
```

### B. Hover State
Saat kursor melintasi elemen interaktif (tombol, tautan berita, baris alert), kelas `.hover-state` diterapkan ke cincin luar untuk memperbesar ukurannya dan memancarkan bias cahaya cyan:
```javascript
document.querySelectorAll("a, button, select, input, .alert-row").forEach(el => {
    el.addEventListener("mouseenter", () => cursorRing.classList.add("hover-state"));
    el.addEventListener("mouseleave", () => cursorRing.classList.remove("hover-state"));
});
```

---

## 🚨 4. Aliran Navigasi Interaktif (Clickable Alerts & Autopilot)

Semua baris peringatan di tab **REGIONAL ALERTS** dan daftar **Top 5 High-Risk** di halaman Autopilot dikonfigurasi agar dapat diklik oleh pengguna untuk berpindah halaman dan menampilkan detail secara otomatis:

```javascript
row.addEventListener("click", () => {
    // 1. Pilih kecamatan target di dropdown
    selectedLocation = item.location;
    if (locationSelect) locationSelect.value = item.location;
    
    // 2. Geser dan fokuskan peta ke kecamatan target
    updateActiveMapMarker(item.location);
    panToLocation(item.location);
    fetchLiveWeather(item.location);
    
    // 3. Pindah tab navigasi ke menu "SIMULATION TOOL"
    switchPage("page-predictor");
    
    // 4. Jalankan inferensi AI secara instan setelah tab terbuka
    setTimeout(() => {
        runPrediction();
    }, 500);
});
```

---

## 📊 5. Format Data Tipe Komposisi & Truk Sampah

Timbulan sampah total dipecah menjadi 6 kategori persentase untuk divisualisasikan dalam bentuk progress bar neon di UI:

```typescript
interface WasteCompositionBreakdown {
  organic_waste_ton: number; // ~50.2% (Sisa Makanan)
  plastic_waste_ton: number; // ~22.8% (Plastik)
  paper_waste_ton: number;   // ~11.5% (Kertas)
  glass_waste_ton: number;   // ~3.2% (Kaca)
  textile_waste_ton: number; // ~4.2% (Tekstil)
  metal_waste_ton: number;   // ~8.1% (Logam/Lainnya)
}

interface LogisticsPlan {
  trucks_needed: number;            // Total timbulan / 5 Ton kapasitas truk
  manpower: number;                 // Jumlah truk * 4 crew (1 sopir + 3 petugas)
  estimated_duration_hours: number; // Jarak rute / 28 km/jam kecepatan truk
  efficiency_rate: string;          // Status efisiensi rute pengangkutan
}
```
Untuk memperbarui lebar grafik bar di HTML, hitung persentase dinamis:
$$\text{Width (\%)} = \left( \frac{\text{Kategori Ton}}{\text{Total Timbulan Ton}} \right) \times 100$$
Lalu masukkan nilainya ke CSS `style.width` masing-masing baris.
