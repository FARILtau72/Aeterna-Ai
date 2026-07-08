// Coordinates and Map Data
const LOCATION_COORDINATES = {
    "GBK": {latitude: -6.2183, longitude: 106.8022},
    "JIS": {latitude: -6.1244, longitude: 106.8622},
    "Pasar Senen": {latitude: -6.1744, longitude: 106.8444},
    "Gang Sempit Tambora": {latitude: -6.1500, longitude: 106.8000}
};

const LOCATION_MAP_DATA = {
    "JIS": {coords: [-6.1244, 106.8622], label: "JIS"},
    "GBK": {coords: [-6.2183, 106.8022], label: "GBK"},
    "Pasar Senen": {coords: [-6.1744, 106.8444], label: "Senen"},
    "Gang Sempit Tambora": {coords: [-6.1500, 106.8000], label: "Tambora"}
};

const LOCATION_RADIUS = {
    "JIS": "1.5 km",
    "GBK": "2.0 km",
    "Pasar Senen": "1.2 km",
    "Gang Sempit Tambora": "0.8 km"
};

const BANTARGEBANG_COORDS = [-6.3477, 106.9939];

// UI Elements
const locationSelect = document.getElementById("location-select");
const modelSelect = document.getElementById("model-select");
const forecastSlider = document.getElementById("forecast-slider");
const forecastVal = document.getElementById("forecast-val");
const rainOverride = document.getElementById("rain-override");
const rainOverrideVal = document.getElementById("rain-override-val");
const eventOverride = document.getElementById("event-override");
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
const barOrganic = document.getElementById("bar-organic");
const barPlastic = document.getElementById("bar-plastic");

// Logistics elements
const logManpower = document.getElementById("log-manpower");
const logDuration = document.getElementById("log-duration");
const logEfficiency = document.getElementById("log-efficiency");
const logConfidence = document.getElementById("log-confidence");

// Timeline & Hourly
const timelineList = document.getElementById("timeline-list");
const hourlySection = document.getElementById("hourly-section");
const hourlyGrid = document.getElementById("hourly-grid");

// State
let selectedLocation = "JIS";
let rainValue = 0; // 0 means Auto (Open-Meteo)
let map;
let mapMarkers = {};
let routeLine = null;

// Event Listeners for controls
forecastSlider.addEventListener("input", (e) => {
    forecastVal.textContent = e.target.value;
});

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

locationSelect.addEventListener("change", (e) => {
    selectedLocation = e.target.value;
    updateActiveMapMarker(selectedLocation);
    panToLocation(selectedLocation);
    fetchLiveWeather(selectedLocation);
});

// Initialize Leaflet Map
function initMap() {
    // Centered around Central Jakarta
    map = L.map('map', {
        zoomControl: true,
        attributionControl: false,
        maxZoom: 15,
        minZoom: 9
    }).setView([-6.175, 106.825], 11.5);

    // CartoDB Dark Matter tile layer for premium dark look
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 20
    }).addTo(map);

    // Add Special Final Disposal Site (TPST Bantargebang) Marker
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
            <div>Active Capacity: <b>Calibrated</b></div>
        </div>
    `);

    // Add Custom Location Markers
    Object.keys(LOCATION_MAP_DATA).forEach(loc => {
        const data = LOCATION_MAP_DATA[loc];
        const customIcon = L.divIcon({
            className: 'leaflet-custom-marker',
            html: `<div class="marker-pulse"></div><div class="marker-core"></div><div class="marker-label">${data.label}</div>`,
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        });

        const marker = L.marker(data.coords, { icon: customIcon }).addTo(map);

        // Marker Click logic
        marker.on('click', () => {
            selectedLocation = loc;
            locationSelect.value = loc;
            updateActiveMapMarker(loc);
            panToLocation(loc);
            fetchLiveWeather(loc);
            runPrediction();
        });

        // Save reference
        mapMarkers[loc] = marker;
    });

    // Initial Active Node highlight
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
    const coords = LOCATION_MAP_DATA[locName]?.coords;
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

// Draw polyline route to TPST Bantargebang
function drawTransitRoute(locName) {
    const startCoords = LOCATION_MAP_DATA[locName]?.coords;
    if (!startCoords || !map) return;

    if (routeLine) {
        map.removeLayer(routeLine);
    }

    // Cyan glowing dashed line representing logistical transit path
    routeLine = L.polyline([startCoords, BANTARGEBANG_COORDS], {
        color: '#00F0FF',
        weight: 3.5,
        opacity: 0.75,
        dashArray: '8, 8',
        className: 'glowing-route'
    }).addTo(map);

    // Hardcoded logistics profile distance mappings
    const distanceMap = {
        "JIS": "41.2 km",
        "GBK": "38.5 km",
        "Pasar Senen": "34.8 km",
        "Gang Sempit Tambora": "43.5 km"
    };

    const timeMap = {
        "JIS": "1.5 Hours",
        "GBK": "1.8 Hours",
        "Pasar Senen": "1.4 Hours",
        "Gang Sempit Tambora": "2.1 Hours"
    };

    routeLine.bindPopup(`
        <div class="route-popup">
            <h3>LOGISTICS DISPATCH ROUTE</h3>
            <div>Start: <b>${locName}</b></div>
            <div>Destination: <b>TPST Bantargebang</b></div>
            <div>Transit Distance: <b class="highlight">${distanceMap[locName]}</b></div>
            <div>Est. Travel Time: <b class="highlight">${timeMap[locName]}</b></div>
        </div>
    `).openPopup();

    // Automatically zoom/fit bounds to show both the collection point and Bantargebang nicely
    map.fitBounds([startCoords, BANTARGEBANG_COORDS], {
        padding: [60, 60]
    });
}

// Fetch Live Weather from Open-Meteo
async function fetchLiveWeather(loc) {
    const coord = LOCATION_COORDINATES[loc];
    if (!coord) return;

    weatherForecastText.textContent = "Fetching...";
    weatherPrecip.textContent = "0.0 mm";
    weatherAlert.textContent = "Checking...";

    const url = `https://api.open-meteo.com/v1/forecast?latitude=${coord.latitude}&longitude=${coord.longitude}&current_weather=true&daily=precipitation_sum&timezone=Asia/Jakarta&past_days=2`;
    
    try {
        const response = await fetch(url);
        if (response.ok) {
            const data = await response.json();
            const temp = data.current_weather.temperature;
            const wind = data.current_weather.windspeed;
            const code = data.current_weather.weathercode;
            
            // Set precip sum for today
            const dailyData = data.daily || {};
            const precipList = dailyData.precipitation_sum || [];
            // past_days=2 means indices: 0 (H-2), 1 (H-1), 2 (H0)
            const precipToday = precipList[2] || 0;
            
            let cond = "Cloudy";
            if (code === 0) cond = "Clear Sky";
            else if (code > 0 && code < 4) cond = "Partly Cloudy";
            else if (code >= 51 && code <= 67) cond = "Rainy";
            else if (code >= 80 && code <= 82) cond = "Showers";

            weatherForecastText.textContent = `${temp}°C - ${cond}`;
            weatherLocationText.textContent = `${loc} coordinates`;
            weatherPrecip.textContent = `${precipToday.toFixed(1)} mm`;
            
            if (precipToday > 30) {
                weatherAlert.textContent = "HEAVY RAIN 🟡";
                weatherAlert.className = "highlight text-warning";
            } else if (precipToday > 50) {
                weatherAlert.textContent = "FLOOD DANGER 🔴";
                weatherAlert.className = "highlight text-red";
            } else {
                weatherAlert.textContent = "Normal conditions";
                weatherAlert.className = "highlight";
            }
        } else {
            throw new Error("HTTP Error");
        }
    } catch (err) {
        weatherForecastText.textContent = "Weather Unavailable";
        weatherPrecip.textContent = "N/A";
        weatherAlert.textContent = "Error fetching";
    }
}

// Run prediction calling FastAPI backend
async function runPrediction() {
    predictBtn.disabled = true;
    predictBtn.querySelector(".btn-text").textContent = "PROCESSING FORECAST...";

    const payload = {
        forecast_days: parseInt(forecastSlider.value),
        rainfall_mm: parseFloat(rainValue),
        event_scale: parseInt(eventOverride.value),
        location: selectedLocation,
        model_type: modelSelect.value,
        granularity: forecastSlider.value <= 7 ? "hourly" : "daily" // auto hourly for short horizons
    };

    try {
        const response = await fetch("/api/v1/predict", {
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
            alert("Prediction failed. Make sure the API server is running.");
        }
    } catch (err) {
        console.error(err);
        alert("Network error connecting to Waste Intelligence API.");
    } finally {
        predictBtn.disabled = false;
        predictBtn.querySelector(".btn-text").textContent = "RUN PREDICTION";
    }
}

function updateDashboardData(data, confScore, message) {
    const results = data.prediction_results;
    if (results.length === 0) return;

    // Calculate sum of tonnage
    const totalVolume = results.reduce((acc, curr) => acc + curr.total_volume_ton, 0);
    const avgVolume = totalVolume / results.length;
    
    // Update main cards
    statTotalVolume.innerHTML = `${totalVolume.toFixed(2)} <span class="unit">Tons</span>`;
    
    // Determine overall risk
    let maxRisk = "SAFE";
    results.forEach(r => {
        if (r.risk_status === "CRITICAL") maxRisk = "CRITICAL";
        else if (r.risk_status === "WARNING" && maxRisk !== "CRITICAL") maxRisk = "WARNING";
    });
    
    statRiskStatus.textContent = maxRisk;
    statRiskStatus.className = `card-value status-badge ${maxRisk.toLowerCase()}`;

    // Update map marker risk status dynamically
    updateMarkerRisk(selectedLocation, maxRisk);

    // Draw active logistics route to TPST Bantargebang
    drawTransitRoute(selectedLocation);

    statTrucks.innerHTML = `${data.logistics_plan.trucks_needed} <span class="unit">Trucks (5T)</span>`;

    // Update metadata labels (Prediction Period & Target Location with Radius)
    const startDateStr = results[0].date;
    const endDateStr = results[results.length - 1].date;
    
    statPeriodMeta.textContent = `Period: ${startDateStr} to ${endDateStr}`;
    statLocationMeta.textContent = `${selectedLocation} (Radius ${LOCATION_RADIUS[selectedLocation]})`;

    // Composition Breakdown
    const totalOrganic = results.reduce((acc, curr) => acc + curr.organic_waste_ton, 0);
    const totalPlastic = results.reduce((acc, curr) => acc + curr.plastic_waste_ton, 0);
    
    valOrganic.textContent = `${totalOrganic.toFixed(2)} Ton`;
    valPlastic.textContent = `${totalPlastic.toFixed(2)} Ton`;

    const organicPercentage = totalVolume > 0 ? (totalOrganic / totalVolume) * 100 : 0;
    const plasticPercentage = totalVolume > 0 ? (totalPlastic / totalVolume) * 100 : 0;

    barOrganic.style.width = `${organicPercentage}%`;
    barPlastic.style.width = `${plasticPercentage}%`;

    // Logistics plan
    logManpower.textContent = `${data.logistics_plan.manpower} Crew`;
    logDuration.textContent = `${data.logistics_plan.estimated_duration_hours.toFixed(1)} Hours`;
    logEfficiency.textContent = data.logistics_plan.efficiency_rate;
    logConfidence.textContent = `${(confScore * 100).toFixed(1)}%`;

    // Event Info banner
    const eventDay = results.find(r => r.event_info !== null);
    if (eventDay) {
        eventDescText.innerHTML = `⚠️ <strong>${eventDay.event_info}</strong> on ${eventDay.date}. Heavy crowd expected near site.`;
        document.getElementById("event-box").style.borderColor = "var(--red)";
    } else {
        eventDescText.textContent = "No major public events scheduled for this location in the forecast window.";
        document.getElementById("event-box").style.borderColor = "var(--yellow)";
    }

    // Daily timeline breakdown cards
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

    // Hourly Risk Heatmap
    const hourlyDay = results[0]; // show hourly for first day if requested
    if (hourlyDay && hourlyDay.hourly_breakdown) {
        hourlySection.style.display = "block";
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
    } else {
        hourlySection.style.display = "none";
    }
}

// Request CSV from Backend API and download it
async function runExport() {
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
        } else {
            alert("CSV export failed. Ensure the server is online.");
        }
    } catch (err) {
        console.error(err);
        alert("Network error connecting to Export API.");
    } finally {
        exportBtn.disabled = false;
        exportBtn.querySelector(".btn-text").textContent = "EXPORT CSV";
    }
}

predictBtn.addEventListener("click", runPrediction);
exportBtn.addEventListener("click", runExport);

// Initial loading setup
window.addEventListener("DOMContentLoaded", () => {
    initMap();
    fetchLiveWeather("JIS");
    // Run initial prediction after models load
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
let maxPrecip = 0; // Current precipitation override

function updateRainAnimationIntensity(precipVal) {
    maxPrecip = precipVal;
}

// Particle class for normal state (no rain)
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
        ctx.fillStyle = `rgba(0, 240, 255, ${this.alpha})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

// Rain Drop class for rainy state
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
        ctx.strokeStyle = `rgba(0, 240, 255, ${this.alpha})`;
        ctx.lineWidth = this.weight;
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(this.x + (maxPrecip * 0.05), this.y + this.length);
        ctx.stroke();
    }
}

// Initialize particles and rain drops
for (let i = 0; i < 60; i++) {
    particles.push(new DataParticle());
}
for (let i = 0; i < 150; i++) {
    drops.push(new RainDrop());
}

function animate() {
    ctx.clearRect(0, 0, width, height);
    
    if (maxPrecip === 0) {
        // Normal floating data particles
        particles.forEach(p => {
            p.update();
            p.draw();
        });
    } else {
        // Cyber rain drops falling
        // Number of raindrops drawn depends on the rain scale override
        const activeCount = Math.min(Math.floor(maxPrecip * 1.5), 150);
        for (let i = 0; i < activeCount; i++) {
            drops[i].update();
            drops[i].draw();
        }
    }
    
    requestAnimationFrame(animate);
}

animate();
