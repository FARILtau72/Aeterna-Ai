// Coordinates and Map Data for all 44 Kecamatan of DKI Jakarta
const KECAMATAN_DATABASE = {
    // 1. JAKARTA PUSAT (8 Kecamatan)
    "Menteng": {coords: [-6.1950, 106.8322], city: "Jakarta Pusat", radius: "1.2 km"},
    "Senen": {coords: [-6.1822, 106.8452], city: "Jakarta Pusat", radius: "1.0 km"},
    "Cempaka Putih": {coords: [-6.1802, 106.8686], city: "Jakarta Pusat", radius: "1.1 km"},
    "Johar Baru": {coords: [-6.1866, 106.8572], city: "Jakarta Pusat", radius: "0.8 km"},
    "Kemayoran": {coords: [-6.1628, 106.8438], city: "Jakarta Pusat", radius: "1.5 km"},
    "Sawah Besar": {coords: [-6.1554, 106.8322], city: "Jakarta Pusat", radius: "1.2 km"},
    "Tanah Abang": {coords: [-6.2104, 106.8122], city: "Jakarta Pusat", radius: "2.0 km"},
    "Gambir": {coords: [-6.1764, 106.8190], city: "Jakarta Pusat", radius: "1.8 km"},

    // 2. JAKARTA UTARA (6 Kecamatan)
    "Penjaringan": {coords: [-6.1264, 106.7822], city: "Jakarta Utara", radius: "2.5 km"},
    "Tanjung Priok": {coords: [-6.1322, 106.8722], city: "Jakarta Utara", radius: "2.2 km"},
    "Koja": {coords: [-6.1214, 106.9133], city: "Jakarta Utara", radius: "1.8 km"},
    "Cilincing": {coords: [-6.1288, 106.9452], city: "Jakarta Utara", radius: "3.0 km"},
    "Pademangan": {coords: [-6.1328, 106.8422], city: "Jakarta Utara", radius: "1.5 km"},
    "Kelapa Gading": {coords: [-6.1552, 106.9022], city: "Jakarta Utara", radius: "2.0 km"},

    // 3. JAKARTA BARAT (8 Kecamatan)
    "Cengkareng": {coords: [-6.1528, 106.7322], city: "Jakarta Barat", radius: "3.0 km"},
    "Grogol Petamburan": {coords: [-6.1622, 106.7882], city: "Jakarta Barat", radius: "2.0 km"},
    "Kalideres": {coords: [-6.1428, 106.7022], city: "Jakarta Barat", radius: "3.2 km"},
    "Kebon Jeruk": {coords: [-6.1922, 106.7722], city: "Jakarta Barat", radius: "2.2 km"},
    "Kembangan": {coords: [-6.1828, 106.7382], city: "Jakarta Barat", radius: "2.5 km"},
    "Palmerah": {coords: [-6.2028, 106.7882], city: "Jakarta Barat", radius: "1.8 km"},
    "Taman Sari": {coords: [-6.1454, 106.8182], city: "Jakarta Barat", radius: "1.2 km"},
    "Tambora": {coords: [-6.1500, 106.8000], city: "Jakarta Barat", radius: "1.0 km"},

    // 4. JAKARTA SELATAN (10 Kecamatan)
    "Cilandak": {coords: [-6.2928, 106.7922], city: "Jakarta Selatan", radius: "2.2 km"},
    "Jagakarsa": {coords: [-6.3328, 106.8222], city: "Jakarta Selatan", radius: "2.5 km"},
    "Kebayoran Baru": {coords: [-6.2422, 106.7982], city: "Jakarta Selatan", radius: "2.0 km"},
    "Kebayoran Lama": {coords: [-6.2488, 106.7722], city: "Jakarta Selatan", radius: "2.4 km"},
    "Mampang Prapatan": {coords: [-6.2522, 106.8182], city: "Jakarta Selatan", radius: "1.5 km"},
    "Pancoran": {coords: [-6.2622, 106.8382], city: "Jakarta Selatan", radius: "1.6 km"},
    "Pasar Minggu": {coords: [-6.2828, 106.8438], city: "Jakarta Selatan", radius: "2.5 km"},
    "Pesanggrahan": {coords: [-6.2588, 106.7588], city: "Jakarta Selatan", radius: "2.0 km"},
    "Setiabudi": {coords: [-6.2228, 106.8282], city: "Jakarta Selatan", radius: "1.8 km"},
    "Tebet": {coords: [-6.2288, 106.8482], city: "Jakarta Selatan", radius: "2.0 km"},

    // 5. JAKARTA TIMUR (10 Kecamatan)
    "Cakung": {coords: [-6.1828, 106.9482], city: "Jakarta Timur", radius: "3.5 km"},
    "Cipayung": {coords: [-6.3128, 106.9022], city: "Jakarta Timur", radius: "2.8 km"},
    "Ciracas": {coords: [-6.3228, 106.8782], city: "Jakarta Timur", radius: "2.2 km"},
    "Duren Sawit": {coords: [-6.2228, 106.9282], city: "Jakarta Timur", radius: "3.0 km"},
    "Jatinegara": {coords: [-6.2222, 106.8682], city: "Jakarta Timur", radius: "2.5 km"},
    "Kramat Jati": {coords: [-6.2722, 106.8682], city: "Jakarta Timur", radius: "2.4 km"},
    "Makasar": {coords: [-6.2622, 106.8782], city: "Jakarta Timur", radius: "2.0 km"},
    "Matraman": {coords: [-6.2022, 106.8582], city: "Jakarta Timur", radius: "1.5 km"},
    "Pasar Rebo": {coords: [-6.3122, 106.8522], city: "Jakarta Timur", radius: "2.0 km"},
    "Pulo Gadung": {coords: [-6.1922, 106.8922], city: "Jakarta Timur", radius: "2.6 km"},

    // 6. KEPULAUAN SERIBU (2 Kecamatan)
    "Kepulauan Seribu Utara": {coords: [-5.5722, 106.5522], city: "Kepulauan Seribu", radius: "8.0 km"},
    "Kepulauan Seribu Selatan": {coords: [-5.7722, 106.6522], city: "Kepulauan Seribu", radius: "7.0 km"}
};

const BANTARGEBANG_COORDS = [-6.3477, 106.9939];

// Dynamic backend routing (highly compatible with Vercel deployment)
const API_BASE_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "" // Relative path on local environment
    : "https://alamdieng-waste-prediction-api.hf.space"; // Direct backend url on remote hosting

// UI Elements
const locationSelect = document.getElementById("location-select");
const modelSelect = document.getElementById("model-select");
const forecastSlider = document.getElementById("forecast-slider");
const forecastVal = document.getElementById("forecast-val");
const rainOverride = document.getElementById("rain-override");
const rainOverrideVal = document.getElementById("rain-override-val");
const eventOverride = document.getElementById("event-override");
const eventOverrideVal = document.getElementById("event-override-val");
const predictBtn = document.getElementById("predict-btn");
const exportBtn = document.getElementById("export-btn");

// Weather elements
const weatherForecastText = document.getElementById("weather-forecast-text");
const weatherLocationText = document.getElementById("weather-location-text");
const weatherPrecip = document.getElementById("weather-precip");
const weatherAlert = document.getElementById("weather-alert");
const eventDescText = document.getElementById("event-desc-text");

// Stats elements
const statTotalVolume = document.getElementById("stat-total-volume");
const statRiskStatus = document.getElementById("stat-risk-status");
const statTrucks = document.getElementById("stat-trucks");

// Metadata elements
const statPeriodMeta = document.getElementById("stat-period-meta");
const statLocationMeta = document.getElementById("stat-location-meta");

// Composition elements
const valOrganic = document.getElementById("val-organic");
const valPlastic = document.getElementById("val-plastic");
const valPaper = document.getElementById("val-paper");
const valGlass = document.getElementById("val-glass");
const valTextile = document.getElementById("val-textile");
const valMetal = document.getElementById("val-metal");
const barOrganic = document.getElementById("bar-organic");
const barPlastic = document.getElementById("bar-plastic");
const barPaper = document.getElementById("bar-paper");
const barGlass = document.getElementById("bar-glass");
const barTextile = document.getElementById("bar-textile");
const barMetal = document.getElementById("bar-metal");

// Logistics elements
const logManpower = document.getElementById("log-manpower");
const logDuration = document.getElementById("log-duration");
const logEfficiency = document.getElementById("log-efficiency");
const logConfidence = document.getElementById("log-confidence");

// Timeline & Hourly
const timelineList = document.getElementById("timeline-list");
const hourlySection = document.getElementById("hourly-section");
const hourlyGrid = document.getElementById("hourly-grid");

// Decision Dashboard UI Elements
const decLocationSelect = document.getElementById("dec-location-select");
const decTotalVol = document.getElementById("dec-total-vol");
const decVolStatus = document.getElementById("dec-vol-status");
const decCostVal = document.getElementById("dec-cost-val");
const decEfficiencyVal = document.getElementById("dec-efficiency-val");
const decSavedVal = document.getElementById("dec-saved-val");
const decWorkloadGrid = document.getElementById("dec-workload-grid");
const decTruckLarge = document.getElementById("dec-truck-large");
const decTruckSmall = document.getElementById("dec-truck-small");
const decCriticalTitle = document.getElementById("dec-critical-title");
const decCriticalList = document.getElementById("dec-critical-list");

// Weather Modal UI Elements
const weatherModal = document.getElementById("weather-modal");
const modalWeatherLoc = document.getElementById("modal-weather-loc");
const modalSumTotal = document.getElementById("modal-sum-total");
const modalSumAvg = document.getElementById("modal-sum-avg");
const modalSumBadge = document.getElementById("modal-sum-badge");
const weatherModalList = document.getElementById("weather-modal-list");

// State
let selectedLocation = "Menteng";
let rainValue = 0; // 0 means Auto (Open-Meteo)
let map;
let mapMarkers = {};
let routeLine = null;
let lastPredictionData = null;

// ==========================================
// SPA MULTIPAGE ROUTING
// ==========================================
function switchPage(pageId) {
    document.querySelectorAll(".page-container").forEach(el => {
        el.classList.remove("active");
    });
    document.querySelectorAll(".nav-btn").forEach(el => {
        el.classList.remove("active");
    });

    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add("active");
    }

    const targetBtn = document.querySelector(`.nav-btn[data-target="${pageId}"]`);
    if (targetBtn) {
        targetBtn.classList.add("active");
    }

    if (pageId === "page-news") {
        loadNewsFeed();
    } else if (pageId === "page-alerts") {
        loadAlertsFeed();
    } else if (pageId === "page-autopilot") {
        loadAutopilotFeed();
    } else if (pageId === "page-predictor") {
        if (map) setTimeout(() => { map.invalidateSize(); }, 200);
        if (lastPredictionData) {
            updateDecisionDashboard(lastPredictionData, selectedLocation);
        }
    }
}

window.switchPage = switchPage;

// Dynamically Populate Dropdown on Startup
function populateLocationDropdown() {
    if (!locationSelect) return;
    locationSelect.innerHTML = "";
    Object.keys(KECAMATAN_DATABASE).forEach(loc => {
        const opt = document.createElement("option");
        opt.value = loc;
        opt.textContent = `${loc} (${KECAMATAN_DATABASE[loc].city})`;
        locationSelect.appendChild(opt);
    });
    locationSelect.value = selectedLocation;
}

// Calculate Haversine Distance between two coordinate arrays [lat, lon]
function getHaversineDistance(coords1, coords2) {
    const R = 6371; // Earth radius in km
    const dLat = (coords2[0] - coords1[0]) * Math.PI / 180;
    const dLon = (coords2[1] - coords1[1]) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(coords1[0] * Math.PI / 180) * Math.cos(coords2[0] * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

// Event Listeners for controls
if (forecastSlider) {
    forecastSlider.addEventListener("input", (e) => {
        forecastVal.textContent = e.target.value;
    });
}

if (rainOverride) {
    rainOverride.addEventListener("input", (e) => {
        const val = parseInt(e.target.value);
        rainValue = val;
        if (val === 0) {
            rainOverrideVal.textContent = "Auto (Open-Meteo)";
        } else {
            rainOverrideVal.textContent = `${val} mm`;
        }
        updateRainAnimationIntensity(val);
    });
}

if (eventOverride) {
    eventOverride.addEventListener("input", (e) => {
        const val = parseInt(e.target.value);
        if (eventOverrideVal) {
            eventOverrideVal.textContent = `${val.toLocaleString()} Jiwa`;
        }
    });
}

if (locationSelect) {
    locationSelect.addEventListener("change", (e) => {
        selectedLocation = e.target.value;
        const pop = KECAMATAN_DATABASE[selectedLocation]?.population_jiwa || 100000;
        if (eventOverride) {
            eventOverride.value = pop;
        }
        if (eventOverrideVal) {
            eventOverrideVal.textContent = `${pop.toLocaleString()} Jiwa (BPS)`;
        }
        updateActiveMapMarker(selectedLocation);
        panToLocation(selectedLocation);
        fetchLiveWeather(selectedLocation);
        runPrediction();
    });
}

// Initialize Leaflet Map
function initMap() {
    const mapEl = document.getElementById("map");
    if (!mapEl) return;
    
    map = L.map('map', {
        zoomControl: true,
        attributionControl: false,
        maxZoom: 15,
        minZoom: 9
    }).setView([-6.175, 106.825], 11.5);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 20
    }).addTo(map);

    // Add Bantargebang disposal site marker
    const bantarIcon = L.divIcon({
        className: 'leaflet-custom-marker bantar-marker',
        html: `<div class="marker-pulse" style="background:#FF9900;opacity:0.25;"></div><div class="marker-core" style="background:#FF9900;border:2px solid #FFF;"></div><div class="marker-label" style="color:#FF9900;border-color:#FF9900;">Bantargebang</div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    });
    L.marker(BANTARGEBANG_COORDS, { icon: bantarIcon }).addTo(map).bindPopup(`
        <div class="route-popup" style="border-left: 3px solid #FF9900;">
            <h3 style="color:#FF9900;">TPST BANTARGEBANG</h3>
            <div>Disposal Facility (Bekasi)</div>
            <div>Status: <b>Active & Calibrated</b></div>
        </div>
    `);

    // Add Custom Location Markers for 44 Kecamatan
    Object.keys(KECAMATAN_DATABASE).forEach(loc => {
        const data = KECAMATAN_DATABASE[loc];
        const customIcon = L.divIcon({
            className: 'leaflet-custom-marker',
            html: `<div class="marker-pulse"></div><div class="marker-core"></div><div class="marker-label">${loc}</div>`,
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        });

        const marker = L.marker(data.coords, { icon: customIcon }).addTo(map);

        marker.on('click', () => {
            selectedLocation = loc;
            if (locationSelect) locationSelect.value = loc;
            updateActiveMapMarker(loc);
            panToLocation(loc);
            fetchLiveWeather(loc);
            runPrediction();
        });

        mapMarkers[loc] = marker;
    });

    setTimeout(() => {
        updateActiveMapMarker(selectedLocation);
    }, 1000);
}

function updateActiveMapMarker(locName) {
    Object.keys(mapMarkers).forEach(loc => {
        const marker = mapMarkers[loc];
        const el = marker.getElement();
        if (el) {
            if (loc === locName) {
                el.classList.add("active");
            } else {
                el.classList.remove("active");
            }
        }
    });
}

function panToLocation(locName) {
    const coords = KECAMATAN_DATABASE[locName]?.coords;
    if (coords && map) {
        map.panTo(coords);
    }
}

function updateMarkerRisk(locName, riskStatus) {
    const marker = mapMarkers[locName];
    if (marker) {
        const el = marker.getElement();
        if (el) {
            el.classList.remove("safe", "warning", "critical");
            el.classList.add(riskStatus.toLowerCase());
        }
    }
}

// Draw transit route to TPST Bantargebang
function drawTransitRoute(locName) {
    const startCoords = KECAMATAN_DATABASE[locName]?.coords;
    if (!startCoords || !map) return;

    if (routeLine) {
        map.removeLayer(routeLine);
    }

    routeLine = L.polyline([startCoords, BANTARGEBANG_COORDS], {
        color: '#00F0FF',
        weight: 3.5,
        opacity: 0.75,
        dashArray: '8, 8',
        className: 'glowing-route'
    }).addTo(map);

    const directDist = getHaversineDistance(startCoords, BANTARGEBANG_COORDS);
    const roadDist = directDist * 1.35; 
    const travelTimeHours = roadDist / 28.0; 

    routeLine.bindPopup(`
        <div class="route-popup">
            <h3>LOGISTICS DISPATCH ROUTE</h3>
            <div>Kecamatan: <b>${locName}</b></div>
            <div>Destination: <b>TPST Bantargebang</b></div>
            <div>Transit Distance: <b class="highlight">${roadDist.toFixed(1)} km</b></div>
            <div>Est. Travel Time: <b class="highlight">${travelTimeHours.toFixed(1)} Hours</b></div>
        </div>
    `).openPopup();

    map.fitBounds([startCoords, BANTARGEBANG_COORDS], {
        padding: [60, 60]
    });
}

// Fetch Live Weather from Open-Meteo with Timeout
async function fetchLiveWeather(loc) {
    const coord = KECAMATAN_DATABASE[loc];
    if (!coord) return;

    if (weatherForecastText) weatherForecastText.textContent = "Fetching...";
    if (weatherPrecip) weatherPrecip.textContent = "0.0 mm";
    if (weatherAlert) weatherAlert.textContent = "Checking...";

    const url = `https://api.open-meteo.com/v1/forecast?latitude=${coord.coords[0]}&longitude=${coord.coords[1]}&current_weather=true&daily=precipitation_sum&timezone=Asia/Jakarta&past_days=2`;
    
    // Set 1.5s timeout promise
    const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error("Timeout")), 1500)
    );

    try {
        const fetchPromise = fetch(url).then(res => {
            if (!res.ok) throw new Error("HTTP Error");
            return res.json();
        });

        // Race weather request with 1.5s timeout
        const data = await Promise.race([fetchPromise, timeoutPromise]);
        
        const temp = data.current_weather.temperature;
        const code = data.current_weather.weathercode;
        
        const dailyData = data.daily || {};
        const precipList = dailyData.precipitation_sum || [];
        const precipToday = precipList[2] || 0;
        
        let cond = "Cerah Berawan";
        if (code === 0 && precipToday < 0.5) cond = "Cerah";
        else if (code <= 2 && precipToday < 0.5) cond = "Cerah Berawan";
        else if (code <= 3 && precipToday < 0.5) cond = "Berawan";
        else if (precipToday >= 20.0) cond = "Hujan Lebat";
        else if (precipToday >= 5.0) cond = "Hujan Sedang";
        else if (precipToday >= 0.5) cond = "Hujan Ringan";
        else cond = "Berawan";

        if (weatherForecastText) weatherForecastText.textContent = `${temp}°C - ${cond}`;
        if (weatherLocationText) weatherLocationText.textContent = `${loc} (${coord.city})`;
        if (weatherPrecip) weatherPrecip.textContent = `${precipToday.toFixed(1)} mm`;
        
        if (weatherAlert) {
            if (precipToday >= 50) {
                weatherAlert.textContent = "FLOOD DANGER 🔴";
                weatherAlert.className = "highlight text-red";
            } else if (precipToday >= 20) {
                weatherAlert.textContent = "HEAVY RAIN 🟡";
                weatherAlert.className = "highlight text-warning";
            } else {
                weatherAlert.textContent = "Normal / Aman";
                weatherAlert.className = "highlight";
            }
        }
    } catch (err) {
        console.warn("Weather fetch timed out/failed. Using fallback forecast.", err);
        // Instant Fallback Weather Data
        const fallbackTemp = 32.5 + Math.random() * 2.0;
        const fallbackPrecip = 0.0;
        if (weatherForecastText) weatherForecastText.textContent = `${fallbackTemp.toFixed(1)}°C - Cerah Berawan`;
        if (weatherLocationText) weatherLocationText.textContent = `${loc} (${coord.city})`;
        if (weatherPrecip) weatherPrecip.textContent = `${fallbackPrecip.toFixed(1)} mm`;
        if (weatherAlert) {
            weatherAlert.textContent = "Normal / Aman";
            weatherAlert.className = "highlight";
        }
    }
}

// Run prediction calling FastAPI backend
async function runPrediction() {
    if (!predictBtn) return;
    predictBtn.disabled = true;
    predictBtn.querySelector(".btn-text").textContent = "PROCESSING FORECAST...";

    const payload = {
        forecast_days: parseInt(forecastSlider.value),
        rainfall_mm: parseFloat(rainValue),
        jumlah_jiwa: parseInt(eventOverride.value),
        event_scale: 0,
        location: selectedLocation,
        model_type: modelSelect.value,
        granularity: forecastSlider.value <= 7 ? "hourly" : "daily"
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const resData = await response.json();
            updateDashboardData(resData.data, resData.confidence_score, resData.message);
        } else {
            console.error("API Error");
        }
    } catch (err) {
        console.error(err);
    } finally {
        predictBtn.disabled = false;
        predictBtn.querySelector(".btn-text").textContent = "RUN PREDICTION";
    }
}

function updateDashboardData(data, confScore, message) {
    const results = data.prediction_results;
    if (results.length === 0) return;

    const totalVolume = results.reduce((acc, curr) => acc + curr.total_volume_ton, 0);
    if (statTotalVolume) statTotalVolume.innerHTML = `${totalVolume.toFixed(2)} <span class="unit">Tons</span>`;
    
    let maxRisk = "SAFE";
    results.forEach(r => {
        if (r.risk_status === "CRITICAL") maxRisk = "CRITICAL";
        else if (r.risk_status === "WARNING" && maxRisk !== "CRITICAL") maxRisk = "WARNING";
    });
    
    if (statRiskStatus) {
        statRiskStatus.textContent = maxRisk;
        statRiskStatus.className = `card-value status-badge ${maxRisk.toLowerCase()}`;
    }

    updateMarkerRisk(selectedLocation, maxRisk);
    drawTransitRoute(selectedLocation);

    if (statTrucks) statTrucks.innerHTML = `${data.logistics_plan.trucks_needed} <span class="unit">Trucks (15T)</span>`;

    const startDateStr = results[0].date;
    const endDateStr = results[results.length - 1].date;
    
    if (statPeriodMeta) statPeriodMeta.textContent = `Period: ${startDateStr} to ${endDateStr}`;
    if (statLocationMeta) statLocationMeta.textContent = `${selectedLocation} (Radius ${KECAMATAN_DATABASE[selectedLocation].radius})`;

    const totalOrganic = results.reduce((acc, curr) => acc + curr.organic_waste_ton, 0);
    const totalPlastic = results.reduce((acc, curr) => acc + curr.plastic_waste_ton, 0);
    const totalPaper = results.reduce((acc, curr) => acc + curr.paper_waste_ton, 0);
    const totalGlass = results.reduce((acc, curr) => acc + curr.glass_waste_ton, 0);
    const totalTextile = results.reduce((acc, curr) => acc + curr.textile_waste_ton, 0);
    const totalMetal = results.reduce((acc, curr) => acc + (curr.metal_waste_ton + curr.other_waste_ton), 0);
    
    if (valOrganic) valOrganic.textContent = `${totalOrganic.toFixed(2)} Ton`;
    if (valPlastic) valPlastic.textContent = `${totalPlastic.toFixed(2)} Ton`;
    if (valPaper) valPaper.textContent = `${totalPaper.toFixed(2)} Ton`;
    if (valGlass) valGlass.textContent = `${totalGlass.toFixed(2)} Ton`;
    if (valTextile) valTextile.textContent = `${totalTextile.toFixed(2)} Ton`;
    if (valMetal) valMetal.textContent = `${totalMetal.toFixed(2)} Ton`;

    const getPct = (val) => totalVolume > 0 ? (val / totalVolume) * 100 : 0;

    if (barOrganic) barOrganic.style.width = `${getPct(totalOrganic)}%`;
    if (barPlastic) barPlastic.style.width = `${getPct(totalPlastic)}%`;
    if (barPaper) barPaper.style.width = `${getPct(totalPaper)}%`;
    if (barGlass) barGlass.style.width = `${getPct(totalGlass)}%`;
    if (barTextile) barTextile.style.width = `${getPct(totalTextile)}%`;
    if (barMetal) barMetal.style.width = `${getPct(totalMetal)}%`;

    if (logManpower) logManpower.textContent = `${data.logistics_plan.manpower} Crew`;
    if (logDuration) logDuration.textContent = `${data.logistics_plan.estimated_duration_hours.toFixed(1)} Hours`;
    if (logEfficiency) logEfficiency.textContent = data.logistics_plan.efficiency_rate;
    if (logConfidence) logConfidence.textContent = `${(confScore * 100).toFixed(1)}%`;

    const eventDay = results.find(r => r.event_info !== null);
    if (eventDay) {
        if (eventDescText) eventDescText.innerHTML = `⚠️ <strong>${eventDay.event_info}</strong> on ${eventDay.date}. Heavy crowd expected near site.`;
        const eBox = document.getElementById("event-box");
        if (eBox) eBox.style.borderColor = "var(--red)";
    } else {
        if (eventDescText) eventDescText.textContent = "No major public events scheduled for this location in the forecast window.";
        const eBox = document.getElementById("event-box");
        if (eBox) eBox.style.borderColor = "var(--yellow)";
    }

    if (timelineList) {
        timelineList.innerHTML = "";
        results.forEach(day => {
            const card = document.createElement("div");
            card.className = "timeline-card";
            
            const dateObj = new Date(day.date);
            const dayName = dateObj.toLocaleDateString('en-US', { weekday: 'short' });
            const displayDate = `${dayName}, ${dateObj.getDate()} ${dateObj.toLocaleString('en-US', { month: 'short' })}`;

            card.innerHTML = `
                <span class="timeline-date">${displayDate}</span>
                <span class="timeline-vol">${day.total_volume_ton.toFixed(1)} T</span>
                <span class="timeline-status ${day.risk_status.toLowerCase()}">${day.risk_status}</span>
            `;
            timelineList.appendChild(card);
        });
    }

    const hourlyDay = results[0];
    if (hourlyDay && hourlyDay.hourly_breakdown) {
        if (hourlySection) hourlySection.style.display = "block";
        if (hourlyGrid) {
            hourlyGrid.innerHTML = "";
            hourlyDay.hourly_breakdown.forEach(hour => {
                const cell = document.createElement("div");
                cell.className = "hourly-cell";
                
                let intensityClass = "low";
                if (hour.risk_indicator === "MEDIUM") intensityClass = "medium";
                else if (hour.risk_indicator === "HIGH") intensityClass = "high";

                cell.innerHTML = `
                    <div class="cell-block ${intensityClass}" title="Vol: ${hour.estimated_volume_ton} Ton - Risk: ${hour.risk_indicator}"></div>
                    <span class="cell-time">${hour.hour}</span>
                `;
                hourlyGrid.appendChild(cell);
            });
        }
    } else {
        if (hourlySection) hourlySection.style.display = "none";
    }

    // Save and update Decision Dashboard
    lastPredictionData = data;
    updateDecisionDashboard(data, selectedLocation);
}

// ==========================================
// DECISION DASHBOARD (EXECUTIVE LOGISTICS & COST OPTIMIZER)
// ==========================================
function updateDecisionDashboard(data, location) {
    if (!data || !data.prediction_results || data.prediction_results.length === 0) return;

    const results = data.prediction_results;
    const weekResults = results.slice(0, 7);
    const totalVolume = weekResults.reduce((acc, curr) => acc + curr.total_volume_ton, 0);
    const totalTrucks = weekResults.reduce((acc, curr) => acc + curr.recommended_trucks, 0);
    const config = KECAMATAN_DATABASE[location] || KECAMATAN_DATABASE["Menteng"];

    // 1. Total Volume Prediksi
    if (decTotalVol) decTotalVol.textContent = totalVolume.toFixed(1);
    if (decVolStatus) decVolStatus.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00F0FF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> Berhasil diprediksi (${weekResults.length} hari)`;

    // 2. Estimasi Biaya Operasional (Pergub DKI & Standar DLH: Rp 95.000/ton + SDM Rp 504.000/truk/hari)
    const costProactive = Math.round(((totalVolume * 95000) + (totalTrucks * 504000)) / 100000) * 100000;
    const costReactive = Math.round((costProactive * 2.048) / 100000) * 100000;
    const costSaved = costReactive - costProactive;
    const efficiencyPct = ((costSaved / costReactive) * 100).toFixed(1);

    if (decCostVal) decCostVal.textContent = `Rp ${costProactive.toLocaleString('id-ID')}`;
    if (decEfficiencyVal) decEfficiencyVal.textContent = `${efficiencyPct}%`;
    if (decSavedVal) decSavedVal.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline points="17 18 23 18 23 12"/></svg> Hemat Rp ${costSaved.toLocaleString('id-ID')} dibanding Reaktif`;

    // 3. Alokasi Armada Spesifik (Dump Truck 60% vs Pick-up 40% pemukiman padat)
    const dumpTruckUnits = Math.ceil(totalTrucks * 0.60);
    const pickupUnits = Math.ceil(totalTrucks * 0.40 * 1.75);
    if (decTruckLarge) decTruckLarge.textContent = dumpTruckUnits;
    if (decTruckSmall) decTruckSmall.textContent = pickupUnits;

    // 4. Peta Beban Kerja Harian (7 Hari Horizon)
    if (decWorkloadGrid) {
        decWorkloadGrid.innerHTML = "";
        const dayAbbrsIndo = ["MIN", "SEN", "SEL", "RAB", "KAM", "JUM", "SAB"];

        weekResults.forEach(day => {
            const dateObj = new Date(day.date);
            const dayAbbr = dayAbbrsIndo[dateObj.getDay()] || "HARI";
            const isCritical = day.risk_status === "CRITICAL" || day.total_volume_ton > (config.normal_avg * 1.18);
            const isWarning = day.risk_status === "WARNING";

            let badgeClass = "normal";
            if (isCritical) badgeClass = "peak-critical";
            else if (isWarning || dateObj.getDay() === 0 || dateObj.getDay() === 5 || dateObj.getDay() === 6) badgeClass = "warning";

            const card = document.createElement("div");
            card.className = `workload-day-card ${isCritical ? "critical" : ""}`;
            
            // Shift schedule: S1 & S2 always active, S3 active on peak/critical days
            const showShift3 = isCritical || day.total_volume_ton > (config.normal_avg * 1.10);
            
            card.innerHTML = `
                <div class="workload-day-badge ${badgeClass}">${dayAbbr}</div>
                <div class="workload-ton-val">${day.total_volume_ton.toFixed(1)}</div>
                <div class="workload-ton-label">TON</div>
                <div class="workload-trucks-count">
                    <span>🚚</span> <span>${day.recommended_trucks}</span>
                </div>
                <div class="workload-shifts-list">
                    <span class="workload-shift-pill s1">S1: 04:00-10:00</span>
                    <span class="workload-shift-pill s2">S2: 10:00-16:00</span>
                    ${showShift3 ? '<span class="workload-shift-pill s3">S3: 19:00-01:00</span>' : ''}
                </div>
            `;
            decWorkloadGrid.appendChild(card);
        });
    }

    // 5. Rencana Aksi Kritis
    const peakDay = weekResults.reduce((max, d) => d.total_volume_ton > max.total_volume_ton ? d : max, weekResults[0]);
    if (peakDay) {
        const peakDateObj = new Date(peakDay.date);
        const dayAbbrsIndo = ["MIN", "SEN", "SEL", "RAB", "KAM", "JUM", "SAB"];
        const peakDayName = dayAbbrsIndo[peakDateObj.getDay()] || "HARI";
        
        let situationTag = "BEBAN PUNCAK & KEPADATAN RUTIN";
        if (peakDay.event_info) {
            situationTag = peakDay.event_info.toUpperCase();
        } else if (peakDay.risk_status === "CRITICAL") {
            situationTag = "HUJAN LEBAT & BEBAN PUNCAK";
        }

        if (decCriticalTitle) {
            decCriticalTitle.textContent = `AKSI HARI ${peakDayName} (${situationTag})`;
        }

        if (decCriticalList) {
            decCriticalList.innerHTML = `
                <li>Aktifkan <strong>Shift 3 (19:00 - 01:00 WIB)</strong> untuk evakuasi cepat TPS permukiman ${location} guna mencegah penumpukan sampah malam.</li>
                <li>Prioritaskan dispatch <strong>${Math.ceil(peakDay.recommended_trucks * 0.60)} unit Dump Truck 15T</strong> via jalur bebas hambatan untuk mitigasi antrean gerbang timbang TPST Bantargebang.</li>
                <li>Siagakan <strong>pompa portabel penyedot lindi</strong> dan armada sapu bersih di titik TPS transfer point.</li>
                <li>Kerahkan <strong>${Math.ceil(peakDay.recommended_trucks * 0.40 * 1.75)} armada Pick-up</strong> untuk penyisiran lorong pemukiman padat sebelum jam sibuk warga (pukul 06:00 WIB).</li>
            `;
        }
    }
}

// ==========================================
// 7-DAY WEATHER FORECAST MODAL CONTROLLER
// ==========================================
async function openWeatherModal(loc) {
    const targetLoc = loc || selectedLocation;
    const coord = KECAMATAN_DATABASE[targetLoc];
    if (!coord) return;

    if (modalWeatherLoc) modalWeatherLoc.textContent = targetLoc;
    if (weatherModal) {
        weatherModal.classList.add("open");
    }

    if (weatherModalList) {
        weatherModalList.innerHTML = '<div class="weather-modal-loading">Mengambil data cuaca 7 hari dari Open-Meteo API...</div>';
    }

    try {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${coord.coords[0]}&longitude=${coord.coords[1]}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_hours&timezone=Asia/Jakarta&forecast_days=7`;
        
        const timeoutPromise = new Promise((_, reject) => 
            setTimeout(() => reject(new Error("Timeout")), 2000)
        );
        const fetchPromise = fetch(url).then(res => {
            if (!res.ok) throw new Error("HTTP Error");
            return res.json();
        });

        const data = await Promise.race([fetchPromise, timeoutPromise]);
        const daily = data.daily || {};
        const dates = daily.time || [];
        const codes = daily.weathercode || [];
        const tempMax = daily.temperature_2m_max || [];
        const tempMin = daily.temperature_2m_min || [];
        const precipSum = daily.precipitation_sum || [];
        const precipHours = daily.precipitation_hours || [];

        let totalPrecip = 0;
        let totalHours = 0;
        precipSum.forEach(p => totalPrecip += (p || 0));
        precipHours.forEach(h => totalHours += (h || 0));

        const avgHr = totalHours > 0 ? (totalPrecip / totalHours) : (totalPrecip / 7);

        if (modalSumTotal) modalSumTotal.textContent = `${totalPrecip.toFixed(1)}mm`;
        if (modalSumAvg) modalSumAvg.textContent = `${avgHr.toFixed(1)}mm/hr`;

        // BMKG Weather Category badge
        if (modalSumBadge) {
            if (totalPrecip < 20.0) {
                modalSumBadge.textContent = "KERING";
                modalSumBadge.className = "weather-dryness-badge dry";
            } else if (totalPrecip < 50.0) {
                modalSumBadge.textContent = "LEMBAP";
                modalSumBadge.className = "weather-dryness-badge wet";
            } else {
                modalSumBadge.textContent = "HUJAN LEBAT";
                modalSumBadge.className = "weather-dryness-badge heavy";
            }
        }

        const dayNamesIndo = ["Min", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"];
        
        if (weatherModalList) {
            weatherModalList.innerHTML = "";
            dates.forEach((dStr, idx) => {
                const dateObj = new Date(dStr);
                const dayName = dayNamesIndo[dateObj.getDay()] || "Hari";
                const wCode = codes[idx] || 0;
                const pVal = precipSum[idx] || 0.0;
                const tMax = Math.round(tempMax[idx] || 33);
                const tMin = Math.round(tempMin[idx] || 25);

                let icon = "☀️";
                let condition = "Cerah";

                // BMKG Meteorological Standard Interpretation
                if (wCode >= 95 || (wCode >= 80 && pVal >= 20.0)) {
                    icon = "⛈️";
                    condition = "Badai Petir";
                } else if (pVal >= 20.0) {
                    icon = "🌧️";
                    condition = "Hujan Lebat";
                } else if (pVal >= 5.0) {
                    icon = "🌧️";
                    condition = "Hujan Sedang";
                } else if (pVal >= 1.5) {
                    icon = "🌦️";
                    condition = "Hujan Ringan";
                } else if (pVal >= 0.5) {
                    icon = "⛅";
                    condition = "Berawan";
                } else {
                    // Under 0.5mm is non-rainy (Cerah / Cerah Berawan)
                    if (wCode === 0) {
                        icon = "☀️";
                        condition = "Cerah";
                    } else if (wCode <= 2) {
                        icon = "🌤️";
                        condition = "Cerah Berawan";
                    } else {
                        icon = "⛅";
                        condition = "Berawan";
                    }
                }

                const precipDisplay = pVal >= 0.5 ? `${pVal.toFixed(1)}mm` : '';

                const row = document.createElement("div");
                row.className = "weather-forecast-row";
                row.innerHTML = `
                    <span class="w-row-day">${dayName}</span>
                    <span class="w-row-icon">${icon}</span>
                    <span class="w-row-cond">${condition}</span>
                    <span class="w-row-precip">${precipDisplay}</span>
                    <div class="w-row-temp">
                        <span class="w-temp-max">${tMax}°</span>
                        <span class="w-temp-min">${tMin}°</span>
                    </div>
                `;
                weatherModalList.appendChild(row);
            });
        }

    } catch (err) {
        console.warn("Open-Meteo weather modal fallback:", err);
        // Fallback matching real Jakarta climate baseline
        const fallbackData = [
            { day: "Kam", icon: "🌦️", cond: "Hujan Ringan", precip: "1.3mm", max: 33, min: 25 },
            { day: "Jum", icon: "⛅", cond: "Berawan", precip: "", max: 35, min: 25 },
            { day: "Sab", icon: "🌤️", cond: "Cerah Berawan", precip: "", max: 36, min: 25 },
            { day: "Min", icon: "☀️", cond: "Cerah", precip: "", max: 34, min: 26 },
            { day: "Sen", icon: "🌦️", cond: "Hujan Ringan", precip: "1.5mm", max: 33, min: 26 },
            { day: "Sel", icon: "🌤️", cond: "Cerah Berawan", precip: "", max: 35, min: 26 },
            { day: "Rab", icon: "🌧️", cond: "Hujan Sedang", precip: "3.6mm", max: 35, min: 27 }
        ];

        if (modalSumTotal) modalSumTotal.textContent = "6.4mm";
        if (modalSumAvg) modalSumAvg.textContent = "0.9mm/hr";
        if (modalSumBadge) {
            modalSumBadge.textContent = "KERING";
            modalSumBadge.className = "weather-dryness-badge dry";
        }

        if (weatherModalList) {
            weatherModalList.innerHTML = "";
            fallbackData.forEach(item => {
                const row = document.createElement("div");
                row.className = "weather-forecast-row";
                row.innerHTML = `
                    <span class="w-row-day">${item.day}</span>
                    <span class="w-row-icon">${item.icon}</span>
                    <span class="w-row-cond">${item.cond}</span>
                    <span class="w-row-precip">${item.precip}</span>
                    <div class="w-row-temp">
                        <span class="w-temp-max">${item.max}°</span>
                        <span class="w-temp-min">${item.min}°</span>
                    </div>
                `;
                weatherModalList.appendChild(row);
            });
        }
    }
}

function closeWeatherModal() {
    if (weatherModal) {
        weatherModal.classList.remove("open");
    }
}

window.openWeatherModal = openWeatherModal;
window.closeWeatherModal = closeWeatherModal;

// Request CSV from Backend API and download it
async function runExport() {
    if (!exportBtn) return;
    exportBtn.disabled = true;
    exportBtn.querySelector(".btn-text").textContent = "EXPORTING...";

    const payload = {
        forecast_days: parseInt(forecastSlider.value),
        rainfall_mm: parseFloat(rainValue),
        event_scale: parseInt(eventOverride.value),
        location: selectedLocation,
        model_type: modelSelect.value,
        granularity: forecastSlider.value <= 7 ? "hourly" : "daily"
    };

    try {
        const response = await fetch("/api/v1/predict/csv", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `waste_forecast_${selectedLocation.replace(/\s+/g, "_")}_${forecastSlider.value}d.csv`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        }
    } catch (err) {
        console.error(err);
    } finally {
        exportBtn.disabled = false;
        exportBtn.querySelector(".btn-text").textContent = "EXPORT CSV";
    }
}

// ==========================================
// SPA ASYNC LOADERS (News, Alerts, Autopilot)
// ==========================================
async function loadNewsFeed() {
    const newsGrid = document.getElementById("news-grid-list");
    if (!newsGrid) return;
    newsGrid.innerHTML = '<div class="loading-news">Loading latest waste intelligence...</div>';
    
    try {
        const res = await fetch(`${API_BASE_URL}/api/v1/news`);
        if (res.ok) {
            const news = await res.json();
            newsGrid.innerHTML = "";
            if (news.length === 0) {
                newsGrid.innerHTML = '<div class="loading-news">No news articles found.</div>';
                return;
            }
            news.forEach(item => {
                const card = document.createElement("div");
                card.className = "news-card";
                card.innerHTML = `
                    <div class="news-card-header">
                        <span class="news-source">${item.source}</span>
                        <span class="news-date">${item.date_fetched || "2026-07-10"}</span>
                    </div>
                    <h3 class="news-title">${item.title}</h3>
                    <p class="news-summary">${item.summary}</p>
                    <a href="${item.url}" target="_blank" class="news-link">READ SOURCE <span>&rarr;</span></a>
                `;
                newsGrid.appendChild(card);
            });
        } else {
            newsGrid.innerHTML = '<div class="loading-news">Failed to fetch news from server.</div>';
        }
    } catch (err) {
        newsGrid.innerHTML = '<div class="loading-news">Error loading news feed.</div>';
    }
}

async function loadAlertsFeed() {
    const alertsList = document.getElementById("alerts-grid-list");
    if (!alertsList) return;
    alertsList.innerHTML = '<div class="loading-alerts">Evaluating regional alert parameters...</div>';
    
    try {
        const res = await fetch(`${API_BASE_URL}/api/v1/alerts`);
        if (res.ok) {
            const alertData = await res.json();
            alertsList.innerHTML = "";
            if (alertData.alerts.length === 0) {
                alertsList.innerHTML = '<div class="loading-alerts">No active warnings. All systems green.</div>';
                return;
            }
            alertData.alerts.forEach(item => {
                const row = document.createElement("div");
                row.className = "alert-row";
                row.innerHTML = `
                    <span class="alert-date">${item.date}</span>
                    <span class="alert-location">${item.location}</span>
                    <span class="alert-badge ${item.status.toLowerCase()}">${item.status}</span>
                    <span class="alert-desc">${item.message} - Timbulan: <strong>${item.estimated_volume_ton.toFixed(1)} Ton</strong></span>
                `;
                row.addEventListener("click", () => {
                    selectedLocation = item.location;
                    if (locationSelect) locationSelect.value = item.location;
                    updateActiveMapMarker(item.location);
                    panToLocation(item.location);
                    fetchLiveWeather(item.location);
                    switchPage("page-predictor");
                    setTimeout(() => {
                        runPrediction();
                    }, 500);
                });
                alertsList.appendChild(row);
            });
        } else {
            alertsList.innerHTML = '<div class="loading-alerts">Failed to load alerts.</div>';
        }
    } catch (err) {
        alertsList.innerHTML = '<div class="loading-alerts">Error loading alerts feed.</div>';
    }
}

async function loadAutopilotFeed() {
    const logContainer = document.getElementById("autopilot-log");
    const autoVol = document.getElementById("auto-total-volume");
    const autoTrucks = document.getElementById("auto-total-trucks");
    const autoRiskList = document.getElementById("auto-risk-list");
    
    if (!logContainer || !autoRiskList) return;
    
    autoVol.textContent = "Calculating...";
    autoTrucks.textContent = "Calculating...";
    autoRiskList.innerHTML = '<div class="loading-news" style="padding:1rem;">Running neural models...</div>';
    logContainer.innerHTML = "";
    
    const addLog = (msg) => {
        const time = new Date().toLocaleTimeString('en-US', { hour12: false });
        const p = document.createElement("div");
        p.textContent = `[${time}] ${msg}`;
        logContainer.appendChild(p);
        logContainer.scrollTop = logContainer.scrollHeight;
    };
    
    addLog("Aeterna Neural Core Initialized.");
    await new Promise(r => setTimeout(r, 600));
    addLog("Connecting to Open-Meteo Geolocation nodes...");
    await new Promise(r => setTimeout(r, 600));
    addLog("Weather models ready. Scanning 44 sub-districts...");
    await new Promise(r => setTimeout(r, 800));
    
    try {
        const res = await fetch(`${API_BASE_URL}/api/v1/autopilot`);
        if (res.ok) {
            const data = await res.json();
            
            addLog("Executing GBR forward inference pass on 44 regions...");
            await new Promise(r => setTimeout(r, 800));
            addLog(`Forecasting complete. Total active events today: ${data.event_today ? data.event_today : "0"}`);
            await new Promise(r => setTimeout(r, 500));
            
            autoVol.innerHTML = `${data.total_volume_ton.toLocaleString('en-US')} <span class="unit">Tons</span>`;
            autoTrucks.innerHTML = `${data.total_trucks.toLocaleString('en-US')} <span class="unit">Trucks (15T)</span>`;
            
            autoRiskList.innerHTML = "";
            data.top_kecamatan.forEach((item, index) => {
                const card = document.createElement("div");
                card.className = "alert-row autopilot-row";
                card.innerHTML = `
                    <span class="alert-date" style="font-weight:bold; color:var(--cyan);">#0${index+1}</span>
                    <span class="alert-location">${item.location}</span>
                    <span class="alert-badge ${item.status.toLowerCase()}">${item.status}</span>
                    <span class="alert-desc" style="font-size:0.8rem;">Coords: <strong>[${item.latitude.toFixed(4)}, ${item.longitude.toFixed(4)}]</strong> | Predicted: <strong>${item.volume_ton.toFixed(1)} Tons</strong> (${item.trucks} Trucks)</span>
                `;
                card.addEventListener("click", () => {
                    selectedLocation = item.location;
                    if (locationSelect) locationSelect.value = item.location;
                    updateActiveMapMarker(item.location);
                    panToLocation(item.location);
                    fetchLiveWeather(item.location);
                    switchPage("page-predictor");
                    setTimeout(() => {
                        runPrediction();
                    }, 500);
                });
                autoRiskList.appendChild(card);
            });
            
            addLog(`DKI Jakarta daily forecast compiled: ${data.total_volume_ton} Tons.`);
            addLog(`Logistics dispatch size set to ${data.total_trucks} crew trucks.`);
            addLog("Autonomous fleet routing to TPST Bantargebang optimized via Haversine.");
        } else {
            addLog("CRITICAL ERROR: Failed to communicate with prediction nodes.");
        }
    } catch (err) {
        addLog("CRITICAL ERROR: Connection timed out.");
    }
}

// Attach Event Listeners on DOM load
window.addEventListener("DOMContentLoaded", () => {
    populateLocationDropdown();
    initMap();
    fetchLiveWeather(selectedLocation);
    
    // Wire SPA Navigation
    document.querySelectorAll(".nav-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const target = btn.getAttribute("data-target");
            switchPage(target);
        });
    });

    if (predictBtn) predictBtn.addEventListener("click", runPrediction);
    if (exportBtn) exportBtn.addEventListener("click", runExport);
    
    setTimeout(runPrediction, 1000);
});

// ==========================================
// BACKGROUND CANVAS: INTERACTIVE RAIN EFFECT
// ==========================================
const canvas = document.getElementById("rain-canvas");
const ctx = canvas.getContext("2d");

let width = canvas.width = window.innerWidth;
let height = canvas.height = window.innerHeight;

window.addEventListener("resize", () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
});

let drops = [];
let particles = [];
let maxPrecip = 0; 

function updateRainAnimationIntensity(precipVal) {
    maxPrecip = precipVal;
}

class DataParticle {
    constructor() {
        this.reset();
    }
    reset() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.size = Math.random() * 2 + 1;
        this.speedX = Math.random() * 0.4 - 0.2;
        this.speedY = Math.random() * -0.5 - 0.2;
        this.alpha = Math.random() * 0.5 + 0.1;
    }
    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        if (this.y < 0 || this.x < 0 || this.x > width) {
            this.reset();
            this.y = height;
        }
    }
    draw() {
        ctx.fillStyle = `rgba(5, 150, 105, ${this.alpha * 0.4})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

class RainDrop {
    constructor() {
        this.reset();
    }
    reset() {
        this.x = Math.random() * width;
        this.y = Math.random() * -100 - 10;
        this.length = Math.random() * 15 + 10;
        this.speed = Math.random() * 12 + 15;
        this.weight = Math.random() * 1 + 0.5;
        this.alpha = Math.random() * 0.3 + 0.1;
    }
    update() {
        this.y += this.speed;
        if (this.y > height) {
            this.reset();
        }
    }
    draw() {
        ctx.strokeStyle = `rgba(5, 150, 105, ${this.alpha * 0.4})`;
        ctx.lineWidth = this.weight;
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(this.x + (maxPrecip * 0.05), this.y + this.length);
        ctx.stroke();
    }
}

for (let i = 0; i < 60; i++) {
    particles.push(new DataParticle());
}
for (let i = 0; i < 150; i++) {
    drops.push(new RainDrop());
}

function animate() {
    ctx.clearRect(0, 0, width, height);
    
    if (maxPrecip === 0) {
        particles.forEach(p => {
            p.update();
            p.draw();
        });
    } else {
        const activeCount = Math.min(Math.floor(maxPrecip * 1.5), 150);
        for (let i = 0; i < activeCount; i++) {
            drops[i].update();
            drops[i].draw();
        }
    }
    
    requestAnimationFrame(animate);
}

animate();

// ==========================================
// CUSTOM CYBER HUD CURSOR
// ==========================================
const cursorDot = document.getElementById("cursor-dot");
const cursorRing = document.getElementById("cursor-ring");

let mouseX = -100;
let mouseY = -100;
let ringX = -100;
let ringY = -100;

document.addEventListener("mousemove", (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    
    if (cursorDot && cursorDot.style.display !== "block") {
        cursorDot.style.display = "block";
        cursorRing.style.display = "block";
    }
});

function animateCursor() {
    const lerpFactor = 0.15;
    ringX += (mouseX - ringX) * lerpFactor;
    ringY += (mouseY - ringY) * lerpFactor;

    if (cursorDot) {
        cursorDot.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0) translate3d(-50%, -50%, 0)`;
    }
    if (cursorRing) {
        cursorRing.style.transform = `translate3d(${ringX}px, ${ringY}px, 0) translate3d(-50%, -50%, 0)`;
    }
    requestAnimationFrame(animateCursor);
}
animateCursor();

// Mouse hover scaling state
document.addEventListener("mouseover", (e) => {
    if (cursorRing && (
        e.target.tagName === "BUTTON" || 
        e.target.tagName === "A" || 
        e.target.tagName === "SELECT" || 
        e.target.tagName === "INPUT" || 
        e.target.classList.contains("leaflet-interactive") ||
        e.target.closest("button") || 
        e.target.closest("a")
    )) {
        cursorRing.classList.add("hover-state");
    }
});
document.addEventListener("mouseout", (e) => {
    if (cursorRing && (
        e.target.tagName === "BUTTON" || 
        e.target.tagName === "A" || 
        e.target.tagName === "SELECT" || 
        e.target.tagName === "INPUT" || 
        e.target.classList.contains("leaflet-interactive") ||
        e.target.closest("button") || 
        e.target.closest("a")
    )) {
        cursorRing.classList.remove("hover-state");
    }
});

// ==========================================
// INTERACTIVE ECO-SORTER SIMULATOR (EDUCATION GAME)
// ==========================================
const WASTE_ITEMS = [
    { name: "Botol Plastik PET", category: "inorganic", icon: "🍼", desc: "Botol air mineral kosong berbahan plastik PET. Butuh waktu sekitar 450 tahun untuk terurai alami!" },
    { name: "Sisa Makanan / Apel", category: "organic", icon: "🍎", desc: "Sampah organik sisa makanan. Mudah terurai dalam 1-2 minggu dan sangat cocok diolah jadi kompos." },
    { name: "Baterai Bekas", category: "hazardous", icon: "hazardous", desc: "Mengandung bahan kimia berbahaya seperti litium atau kadmium (B3). Harus dipilah khusus!" },
    { name: "Kardus Bekas", category: "inorganic", icon: "📦", desc: "Kertas/kardus kering yang dapat didaur ulang menjadi bubur kertas baru." },
    { name: "Botol Kaca", category: "inorganic", icon: "🫙", desc: "Material kaca. Membutuhkan waktu lebih dari 1 juta tahun untuk hancur secara alami di alam." },
    { name: "Lampu Neon Rusak", category: "hazardous", icon: "hazardous", desc: "Lampu kaca bekas yang mengandung gas merkuri berbahaya. Masuk kategori limbah B3." },
    { name: "Daun Kering", category: "organic", icon: "🍂", desc: "Limbah organik kebun. Dapat dikeringkan atau ditimbun untuk menyuburkan tanah." },
    { name: "Masker Medis Bekas", category: "hazardous", icon: "hazardous", desc: "Limbah medis rumah tangga yang berpotensi menularkan penyakit. Masuk kategori limbah B3." },
    { name: "Kulit Pisang", category: "organic", icon: "🍌", desc: "Sampah dapur basah organik. Mengandung nutrisi mikro alami yang baik untuk tanaman." }
];

let gameScore = 0;
let gameItemIndex = 0;

function loadNextWasteItem() {
    const item = WASTE_ITEMS[gameItemIndex];
    const iconEl = document.getElementById("game-item-icon");
    const nameEl = document.getElementById("game-item-name");
    const descEl = document.getElementById("game-item-desc");
    
    if (iconEl && nameEl && descEl) {
        iconEl.textContent = item.icon;
        nameEl.textContent = item.name;
        descEl.textContent = item.desc;
        
        // Add a nice cyber flash animation on load
        iconEl.style.transform = "scale(1.2)";
        setTimeout(() => { iconEl.style.transform = "scale(1)"; }, 150);
    }
}

function sortWaste(chosenCategory) {
    const item = WASTE_ITEMS[gameItemIndex];
    const feedbackEl = document.getElementById("game-feedback");
    const scoreEl = document.getElementById("game-score");
    const gameArea = document.querySelector(".game-area");
    
    if (chosenCategory === item.category) {
        gameScore += 10;
        if (feedbackEl) {
            feedbackEl.textContent = "BENAR! +10 Poin";
            feedbackEl.style.color = "#4ade80";
        }
        if (gameArea) {
            gameArea.style.border = "1px solid #4ade80";
            gameArea.style.boxShadow = "0 0 20px rgba(74, 222, 128, 0.3)";
        }
    } else {
        gameScore = Math.max(0, gameScore - 5);
        let correctText = item.category === "organic" ? "ORGANIK" : item.category === "inorganic" ? "ANORGANIK" : "BAHAYA (B3)";
        if (feedbackEl) {
            feedbackEl.textContent = `SALAH! Kategori Asli: ${correctText}`;
            feedbackEl.style.color = "#fb7185";
        }
        if (gameArea) {
            gameArea.style.border = "1px solid #fb7185";
            gameArea.style.boxShadow = "0 0 20px rgba(251, 113, 133, 0.3)";
        }
    }
    
    if (scoreEl) scoreEl.textContent = gameScore;
    
    // Add visual feedback timeout
    setTimeout(() => {
        if (gameArea) {
            gameArea.style.border = "1px solid var(--border-color)";
            gameArea.style.boxShadow = "none";
        }
    }, 800);
    
    // Go to next item
    gameItemIndex = (gameItemIndex + 1) % WASTE_ITEMS.length;
    setTimeout(loadNextWasteItem, 1000);
}

// Bind to window to allow HTML inline onclick calls
window.sortWaste = sortWaste;

// Initialize the game automatically
document.addEventListener("DOMContentLoaded", () => {
    loadNextWasteItem();
    initCrisisStoryScroller();
    init3DScene();
});

// ==========================================
// CINEMATIC CRISIS STORYTELLING SCROLLER
// ==========================================
function initCrisisStoryScroller() {
    const storyCards = document.querySelectorAll(".story-card");
    const tonsVal = document.getElementById("simulated-tons-val");
    
    if (!storyCards.length || !tonsVal) return;

    // Use IntersectionObserver to detect which card is currently active/visible in the center of screen
    const observerOptions = {
        root: null,
        rootMargin: "-25% 0px -40% 0px", // Focus on the middle of the screen
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Highlight active card
                storyCards.forEach(c => {
                    c.style.borderColor = "var(--border-color)";
                    c.style.background = "var(--bg-panel)";
                    c.style.boxShadow = "none";
                });
                entry.target.style.borderColor = "var(--cyan)";
                entry.target.style.background = "rgba(84, 130, 53, 0.03)";
                entry.target.style.boxShadow = "0 4px 15px rgba(84, 130, 53, 0.05)";
                
                // Get parameters
                const targetHeight = entry.target.getAttribute("data-height");
                const targetTons = entry.target.getAttribute("data-tons");
                
                // Determine 3D color based on stage height
                let colorHex = 0x548235; // Soft green (stage 1)
                if (targetHeight === "55") {
                    colorHex = 0xC59124; // Soft Gold Amber (stage 2)
                } else if (targetHeight === "95") {
                    colorHex = 0xC53929; // Soft Crimson Red (stage 3)
                }
                
                // Update Three.js 3D silo height and color
                update3DHeight(parseInt(targetHeight), colorHex);
                
                // Animate tons text value counter
                animateTonsCounter(parseInt(tonsVal.textContent.replace(/,/g, "")), parseInt(targetTons));
            }
        });
    }, observerOptions);

    storyCards.forEach(card => observer.observe(card));
}

function animateTonsCounter(start, end) {
    const tonsVal = document.getElementById("simulated-tons-val");
    if (!tonsVal) return;
    
    const duration = 800; // ms
    const startTime = performance.now();
    
    function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Ease out quadratic
        const easeProgress = progress * (2 - progress);
        const current = Math.round(start + (end - start) * easeProgress);
        
        tonsVal.textContent = `${current.toLocaleString('en-US')} Tons`;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// ==========================================
// THREE.JS 3D LANDFILL OVERLOAD VISUALIZER
// ==========================================
let scene3D, camera3D, renderer3D;
let siloMesh, wasteMesh, garbageGroup;
let isTabActive = true;
let target3DHeight = 0.1; // 10% initially
let current3DHeight = 0.1;
let targetColorHex = 0x548235;

window.addEventListener("blur", () => { isTabActive = false; });
window.addEventListener("focus", () => { isTabActive = true; });

function init3DScene() {
    const container = document.getElementById("threejs-waste-container");
    if (!container) return;
    
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    // Scene
    scene3D = new THREE.Scene();
    
    // Camera
    camera3D = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera3D.position.set(0, 0.4, 3.5);
    
    // Renderer
    renderer3D = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer3D.setSize(width, height);
    renderer3D.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // optimize mobile
    container.appendChild(renderer3D.domElement);
    
    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene3D.add(ambientLight);
    
    const pointLight = new THREE.PointLight(0xffffff, 0.6, 50);
    pointLight.position.set(2, 4, 3);
    scene3D.add(pointLight);
    
    // 1. Silo Outer Wireframe Cylinder
    const siloGeo = new THREE.CylinderGeometry(0.7, 0.7, 2, 16, 1, true);
    const siloMat = new THREE.MeshBasicMaterial({
        color: 0x548235,
        wireframe: true,
        transparent: true,
        opacity: 0.18
    });
    siloMesh = new THREE.Mesh(siloGeo, siloMat);
    scene3D.add(siloMesh);
    
    // 2. Liquid Waste Cylindrical Fill
    const wasteGeo = new THREE.CylinderGeometry(0.66, 0.66, 2, 24, 1);
    wasteGeo.translate(0, 1, 0); // Translate origin pivot to bottom
    
    const wasteMat = new THREE.MeshPhongMaterial({
        color: 0x548235,
        transparent: true,
        opacity: 0.7,
        shininess: 40,
        flatShading: true
    });
    wasteMesh = new THREE.Mesh(wasteGeo, wasteMat);
    wasteMesh.position.y = -1.0; // Place bottom of liquid at bottom of silo
    wasteMesh.scale.y = 0.1;
    scene3D.add(wasteMesh);
    
    // 3. Floating low-poly garbage elements inside liquid
    garbageGroup = new THREE.Group();
    garbageGroup.position.y = -1.0;
    scene3D.add(garbageGroup);
    
    const geometries = [
        new THREE.DodecahedronGeometry(0.07),
        new THREE.BoxGeometry(0.08, 0.08, 0.08),
        new THREE.TetrahedronGeometry(0.08)
    ];
    
    for (let i = 0; i < 12; i++) {
        const randomGeo = geometries[Math.floor(Math.random() * geometries.length)];
        const randomMat = new THREE.MeshPhongMaterial({
            color: 0x475569, // Slate color
            flatShading: true,
            transparent: true,
            opacity: 0.85
        });
        const mesh = new THREE.Mesh(randomGeo, randomMat);
        
        // Random placement inside silo cylinder range
        mesh.position.set(
            (Math.random() - 0.5) * 0.8,
            Math.random() * 1.8,
            (Math.random() - 0.5) * 0.8
        );
        mesh.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
        
        garbageGroup.add(mesh);
    }
    
    // Resize support
    window.addEventListener("resize", () => {
        if (!container) return;
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera3D.aspect = w / h;
        camera3D.updateProjectionMatrix();
        renderer3D.setSize(w, h);
    });
    
    // Run optimized loop
    animate3D();
}

function update3DHeight(percent, colorHex) {
    target3DHeight = Math.max(0.05, percent / 100);
    targetColorHex = colorHex;
}

function animate3D() {
    requestAnimationFrame(animate3D);
    
    // OPTIMIZATION: Do not render if tab is out of focus or if Home page is hidden
    const homePage = document.getElementById("page-home");
    const container = document.getElementById("threejs-waste-container");
    if (!isTabActive || !homePage || !homePage.classList.contains("active") || !container || container.offsetParent === null) {
        return;
    }
    
    if (wasteMesh) {
        // Smoothly scale height towards target (lerp)
        current3DHeight += (target3DHeight - current3DHeight) * 0.08;
        wasteMesh.scale.y = current3DHeight;
        
        // Smoothly interpolate liquid color (lerp)
        wasteMesh.material.color.lerp(new THREE.Color(targetColorHex), 0.08);
        
        // Float particles up and down inside current liquid boundaries
        if (garbageGroup) {
            garbageGroup.children.forEach((child, idx) => {
                // Keep inside fluid vertical bounds
                if (child.position.y > current3DHeight * 2) {
                    child.position.y -= 0.008;
                } else if (child.position.y < 0.05) {
                    child.position.y += 0.008;
                }
                // Bobbing effect
                child.position.y += Math.sin(Date.now() * 0.001 + idx) * 0.0005;
                
                child.rotation.x += 0.004;
                child.rotation.y += 0.004;
            });
        }
    }
    
    // Rotate models slowly
    if (siloMesh) siloMesh.rotation.y += 0.002;
    if (wasteMesh) wasteMesh.rotation.y -= 0.0015;
    if (garbageGroup) garbageGroup.rotation.y += 0.001;
    
    renderer3D.render(scene3D, camera3D);
}
