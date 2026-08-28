# AETERNA AI — Audit Report
**Branch**: refactor/jsc-data-integrity-v1  
**Audited by**: AETERNA AI MLOps Auditor  
**Date**: 2026-08-28  
**Purpose**: Scientific defensibility assessment for Jakarta Smart City / DLH DKI Jakarta R&D presentation

---

## Severity Legend
- **P0** — Scientifically misleading or incorrect. Must be fixed before any government presentation.
- **P1** — Important engineering issue. Must be resolved before production deployment.
- **P2** — Improvement. Recommended for quality and transparency.

---

## P0 — Critical Scientific Integrity Issues

### P0-1 · Synthetic Dataset Misrepresented as Real DLH/SIPSN Observations

**Affected files**:
- `scripts/generate_real_kecamatan_dataset.py`
- `data/dataset_real_kecamatan_2024_2025.csv`
- `app.py` (startup log, line ~393)

**Finding**:  
`generate_real_kecamatan_dataset.py` creates `Volume_Sampah_Ton` entirely from:
- Manually defined `base_ton` constants per kecamatan (not measured)
- `np.random.exponential` rainfall simulation
- Hardcoded day-of-week, zone, mudik, and event multipliers
- Gaussian noise: `np.random.normal(0, base_vol * 0.075)`

The output CSV is named `dataset_real_kecamatan_2024_2025.csv`, suggesting it contains real observational data. The app startup log calls it `"Real DLH Jakarta baseline dataset"`.

All model evaluation metrics (R², MAE, RMSE, MAPE) therefore measure how well the ML model learns the **synthetic generation function**, not real-world forecasting performance.

**Classification**: SYNTHETIC SIMULATION DATA  
**Impact**: All published model performance metrics are synthetic benchmarks only.  
**Required fix**: Rename dataset, update documentation, label all metrics as synthetic benchmarks.

---

### P0-2 · R² Converted to Operational "Efficiency" and "Accuracy"

**Affected files**:
- `frontend/index.html` lines ~148, ~181
- `app.py` `/llms.txt`, `/llms-full.txt` endpoints
- `README.md`

**Finding**:
- `index.html`: *"Meningkatkan efisiensi tata kelola sampah DKI Jakarta hingga 98.28%"*
- `index.html`: *"Akurasi Validitas Tinggi (98.28%)"*
- `app.py` llms.txt: *"R²=98.28%, MAPE=1.72%"*
- `app.py` llms-full.txt: *"GBR trained with R² = 98.28% accuracy"*

Additionally, the figures are inconsistent: README states GBR R²=88.45%, while llms.txt states 98.28%. The current deployed model is a StackingRegressor, not GBR.

**Classification**: Misleading metric representation  
**Required fix**: Remove all R²-as-efficiency/accuracy conversions. Remove inconsistent metric values. Label remaining metrics as synthetic benchmark only.

---

### P0-3 · News System Fabricates Articles with Real Publisher Branding

**Affected files**:
- `app.py` lines ~587–659 (`generate_dynamic_news_fallback`)
- `app.py` lines ~661–737 (`/api/v1/news`)

**Finding**:  
The LLM prompt instructs the model to *"generate mock but highly realistic and valid-looking news articles"* under real publisher names (Kompas.com, Detik.com, Antara News). The fallback function reuses real article URLs from Detik.com/Antara with randomly modified content (random truck counts, random dates). A user clicking the URL receives a real article whose content does not match the displayed headline.

**Classification**: Fabricated journalism under trusted publisher branding  
**Required fix**: Remove LLM fabrication. Remove dynamic fallback generator. Serve only curated static articles with verified URLs.

---

### P0-4 · Normal_Avg_Ton Creates Target Leakage

**Affected files**:
- `scripts/generate_real_kecamatan_dataset.py` line 217
- `scripts/train.py` line 69

**Finding**:  
`Normal_Avg_Ton` in the dataset is exactly `base_ton`, the constant used to generate `Volume_Sampah_Ton`. The model is trained with this constant as a feature. Since `Volume_Sampah_Ton = f(base_ton, noise)`, the model trivially learns to predict using `Normal_Avg_Ton`, which explains the high R² achieved on synthetic data. This is not evidence of meaningful learning.

**Classification**: Target leakage risk (within synthetic context)  
**Note**: This does not affect real-world deployment if real data is substituted (real `Normal_Avg_Ton` from DLH could be genuinely informative). The leakage is only critical within the synthetic training/evaluation loop.

---

### P0-5 · Truck Capacity Inconsistency (8T docs vs 15T code)

**Affected files**:
- `README.md` line 51: *"Armada Truk Compactor (8-Ton Divisor)"*
- `app.py` `/llms.txt` line ~532: *"Truck Divisor: 8-Ton"*
- `app.py` `/llms-full.txt` line ~561: *"8-Ton Compactor trucks (vol / 8)"*
- `services/logistics_engine.py` line 25: `truck_capacity_ton: 15.0` (active code)

**Finding**:  
All public-facing documentation describes 8T trucks. The active logistics engine uses 15T. Fleet calculations differ by 87.5% depending on which figure is referenced.

**Required fix**: Standardize to 15T throughout (matches active code). Label as prototype assumption, not validated DLH specification.

---

## P1 — Engineering Issues

### P1-1 · Architecture Description Outdated (GBR/Chronos vs StackingRegressor)
- `README.md`, `docs/BACKEND_DOC.md`, `/status` API endpoint still describe GBR + Chronos as the spatial ML engine.
- Active trained model (`models/model_sampah_advanced.pkl`) is a StackingRegressor (DT + RF + GBR → Ridge).
- **Fix**: Update all documentation to describe actual StackingRegressor architecture.

### P1-2 · Model Metadata Lacks Provenance Fields
- Current `model_metadata.pkl` stores only `feature_cols`, `zone_map`, `metrics`, `best_params`.
- Missing: `model_name`, `model_version`, `trained_at`, `training_dataset`, `dataset_type`, `evaluation_type`, `evaluation_note`, `git_commit`.
- **Fix**: Extend metadata schema in `scripts/train.py`.

### P1-3 · CORS Misconfiguration
- `app.py`: `allow_origins=["*"]` combined with `allow_credentials=True` is invalid per browser CORS spec.
- **Fix**: Remove `allow_credentials=True`.

### P1-4 · Startup Log Misidentifies Data Source
- `app.py` line ~393: `"Real DLH Jakarta baseline dataset loaded"`
- **Fix**: Update to `"Synthetic spatial training dataset loaded"`.

### P1-5 · No Baseline Model Comparison
- The ML model is not compared against simple baselines (last-value, rolling mean, historical mean).
- **Fix**: Add baseline comparison in `scripts/train.py`.

### P1-6 · Logistics Config Labeled as "DLH Standards" Without Citation
- `services/logistics_engine.py` line 21: *"Standards derived from Dinas Lingkungan Hidup (DLH) DKI Jakarta"*
- No official DLH document cited.
- **Fix**: Change to `"Prototype Operational Assumptions"` with a note that DLH validation is pending.

### P1-7 · Forecast Reliability Score Uses MAPE as Accuracy Complement
- `services/logistics_engine.py` line ~361: *"A MAPE of 6.12% represents ~93.88% accuracy precision"*
- MAPE is not a complement of accuracy.
- **Fix**: Remove incorrect framing.

### P1-8 · Hardcoded Fallback MAPE in Reliability Score
- `calculate_forecast_reliability_score` defaults to `test_mape=6.12` — a hardcoded value from a previous evaluation.
- **Fix**: Load MAPE from model metadata, document the hardcoded fallback explicitly.

---

## P2 — Improvements

### P2-1 · No `data_status` Field in API Responses
- API responses lack fields: `data_status`, `disclaimer`, `model_version`, `training_data_type`, `generated_at`.

### P2-2 · Uncertainty Intervals Are Hardcoded ±15%
- `app.py` line ~316: `"lower": round(vol*0.85, 2), "upper": round(vol*1.15, 2)` — not statistically derived.
- **Fix**: Label as `"indicative_range"` and document as non-statistical.

### P2-3 · No Data Provenance Documentation
- No `docs/DATA_PROVENANCE.md`.

### P2-4 · No Real Data Connector Architecture
- No `data_sources/` package.

### P2-5 · No Methodology Page in Frontend

### P2-6 · No Frontend Data Status Badge

---

## Pipeline Trace

```
SOURCE
  └─ scripts/generate_real_kecamatan_dataset.py
     Type: SYNTHETIC SIMULATION
     Inputs: hardcoded constants, np.random
     Output: data/dataset_real_kecamatan_2024_2025.csv

PREPROCESSING
  └─ scripts/train.py
     - Chronological sort (prevents temporal ordering issue)
     - Zone_Type categorical encoding
     - Train cutoff: 2025-07-01 (chronological split — correct approach)

FEATURES
  └─ Population_Jiwa: SYNTHETIC (from generator constants)
  └─ Normal_Avg_Ton: SYNTHETIC (= base_ton, source of target leakage)
  └─ Zone_Type_Code: DERIVED (ordinal encoding)
  └─ Rainfall_mm: SYNTHETIC (in training) / EXTERNAL_REALTIME (in inference)
  └─ Rain_Lag_1: SYNTHETIC/DERIVED
  └─ Is_Weekend, Hari_Dalam_Minggu, Bulan: DERIVED (calendar)
  └─ Is_Mudik: DERIVED (hardcoded window)
  └─ Ada_Event, Event_Crowd_Headcount: SYNTHETIC (hardcoded event calendar)

TRAINING
  └─ StackingRegressor (DT + RF + GBR → Ridge)
  └─ Chronological split: Train < 2025-07-01, Test >= 2025-07-01
  └─ Evaluation: MODE A SYNTHETIC BENCHMARK ONLY

INFERENCE
  └─ Rainfall: EXTERNAL_REALTIME via Open-Meteo API
  └─ Population: UNVERIFIED (manually entered, needs BPS validation)
  └─ Events: MANUALLY CURATED calendar

FRONTEND
  └─ Volume forecast labeled as FORECAST (correct)
  └─ Compositions labeled as derived proportions (correct)
  └─ Logistics plan: DETERMINISTIC OPERATIONAL SIMULATION (not AI)

LOGISTICS
  └─ services/logistics_engine.py
  └─ Fleet: ceil(volume / effective_capacity) — DETERMINISTIC MATH
  └─ Manpower: trucks × 3 crew — PROTOTYPE ASSUMPTION
  └─ Collection time: volume / (trucks × rate) — DETERMINISTIC MATH
  └─ Efficiency score: weighted formula — PROTOTYPE SIMULATION
```

---

## Summary

| Category | Count |
|----------|-------|
| P0 Critical | 5 |
| P1 Engineering | 8 |
| P2 Improvement | 6 |
| **Total** | **19** |

All P0 issues are addressed in this refactor branch. P1 and P2 issues are addressed where feasible without breaking existing functionality.
