# AETERNA AI — Data Directory

## ⚠️ IMPORTANT: Dataset Classification

### `synthetic_spatial_training_data_2024_2025.csv` (previously: `dataset_real_kecamatan_2024_2025.csv`)

**Type**: SYNTHETIC SIMULATION DATA  
**Generator**: `scripts/generate_real_kecamatan_dataset.py`  
**Records**: ~32,120 (44 kecamatan × 730 days)  
**Period**: 2024-01-01 to 2025-12-31  

This dataset is **procedurally generated** using:
- Manually defined baseline waste volumes (`base_ton`) per kecamatan
- Simulated rainfall using `numpy.random.exponential`
- Hardcoded zone, weekday, mudik, and event multipliers
- Gaussian noise

**This is NOT observed DLH/SIPSN daily measurement data.**

All model evaluation metrics computed against this dataset are:
> **SYNTHETIC BENCHMARK — Not evidence of real-world forecasting accuracy**

**Permitted uses**:
- Model development and pipeline testing (MODE A)
- UI development and demonstration
- Architecture validation

**Prohibited uses**:
- Claiming real-world prediction accuracy based on these metrics
- Presenting evaluation scores to government stakeholders as observed ground-truth performance
- Replacing authoritative DLH/SIPSN data in any official report

---

### `dataset_real_kecamatan_2024_2025.csv`

This filename is **misleading**. It is identical in content to `synthetic_spatial_training_data_2024_2025.csv`.
Kept for backward compatibility. The canonical name is `synthetic_spatial_training_data_2024_2025.csv`.

---

### `latest_waste_news.json`

**Type**: CURATED STATIC — Manually verified articles  
Contains references to real published articles about waste management in Jakarta.
URLs should be periodically verified. Articles are not auto-generated.

---

### `event_jakarta_2026.txt`

**Type**: MANUALLY CURATED  
Event calendar for 2026, manually assembled. Not from official Pemprov DKI event database.

---

### `dataset_advanced_eco_twin.csv`, `dataset_local_2026.csv`, `dataset_vibe_coder_2026.csv`

**Type**: SYNTHETIC — Legacy development datasets  
Generated during earlier development iterations. Not used in the current production model.
