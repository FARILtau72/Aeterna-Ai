import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, StackingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
import joblib
import sys
import io
import os
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
import warnings
warnings.filterwarnings('ignore')

# Ensure dataset generator can be imported if CSV is missing
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from generate_real_kecamatan_dataset import generate_dataset
except ImportError:
    from scripts.generate_real_kecamatan_dataset import generate_dataset

print("STARTING SPATIAL ENSEMBLE STACKING REGRESSOR TRAINING (AETERNA AI 44 KECAMATAN)...\n")

# ==========================================
# 1. DATA INGESTION (44 KECAMATAN SPATIAL DATASET)
# ==========================================
csv_file = "data/dataset_real_kecamatan_2024_2025.csv"
if not os.path.exists(csv_file) and os.path.exists("waste-prediction-api/data/dataset_real_kecamatan_2024_2025.csv"):
    csv_file = "waste-prediction-api/data/dataset_real_kecamatan_2024_2025.csv"

if not os.path.exists(csv_file):
    print("[Dataset] Dataset tidak ditemukan. Membuat dataset spasial 44 Kecamatan baru...")
    df = generate_dataset()
else:
    print(f"[Dataset] Loading dataset dari '{csv_file}'...")
    df = pd.read_csv(csv_file)

print(f"[Status] Dataset terload: {len(df)} total baris sampel dari 44 Kecamatan (2024-2025).\n")

# Sort chronologically to prevent temporal data leakage
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df = df.sort_values('Tanggal').reset_index(drop=True)

# ==========================================
# 2. FEATURE ENGINEERING & ENCODING
# ==========================================
print("[Info] Ekstraksi & Enkodasi Fitur Spasial-Temporal...")

# Categorical One-Hot / Target Mapping for Zone_Type
zone_map = {
    "Pusat Komersial": 1,
    "Permukiman Padat": 2,
    "Permukiman Menengah": 3,
    "Pariwisata & Olahraga": 4,
    "Pesisir & Pelabuhan": 5,
    "Industri & Pergudangan": 6,
    "Kepulauan": 7
}
df['Zone_Type_Code'] = df['Zone_Type'].map(zone_map).fillna(0)

# Feature matrix for spatial ML model
feature_cols = [
    'Population_Jiwa',
    'Normal_Avg_Ton',
    'Zone_Type_Code',
    'Rainfall_mm',
    'Rain_Lag_1',
    'Is_Weekend',
    'Hari_Dalam_Minggu',
    'Bulan',
    'Is_Mudik',
    'Ada_Event',
    'Event_Crowd_Headcount'
]

X = df[feature_cols]
y = df['Volume_Sampah_Ton']

# ==========================================
# 3. CHRONOLOGICAL TRAIN-TEST SPLIT
# ==========================================
train_idx = df['Tanggal'] < pd.Timestamp("2025-07-01")

X_train, X_test = X[train_idx], X[~train_idx]
y_train, y_test = y[train_idx], y[~train_idx]

print(f"[Split] Split Data Kronologis: Train={len(X_train)} baris, Test={len(X_test)} baris.")

# ==========================================
# 4. ENSEMBLE STACKING REGRESSOR TRAINING
# ==========================================
print("\n[Train] Melatih Model Stacking Regressor (Decision Tree + Random Forest + GBR)...")

estimators = [
    ('dt', DecisionTreeRegressor(max_depth=6, random_state=42)),
    ('rf', RandomForestRegressor(n_estimators=150, max_depth=6, random_state=42, n_jobs=-1)),
    ('gbr', GradientBoostingRegressor(n_estimators=150, max_depth=5, learning_rate=0.05, random_state=42))
]

best_model = StackingRegressor(
    estimators=estimators,
    final_estimator=Ridge(alpha=1.0),
    cv=3,
    n_jobs=-1
)
best_model.fit(X_train, y_train)

pred_test = best_model.predict(X_test)

# Calculate out-of-sample metrics
mae = mean_absolute_error(y_test, pred_test)
rmse = mean_squared_error(y_test, pred_test) ** 0.5
r2 = r2_score(y_test, pred_test)
mape = mean_absolute_percentage_error(y_test, pred_test) * 100

# ==========================================
# 5. PERBANDINGAN METRICS & LAPORAN AUDIT
# ==========================================
print("\n[Metrics] HASIL EVALUASI MODEL STACKING REGRESSOR (OUT-OF-SAMPLE TEST SET):")
print(f"┌─────────────────────────┬──────────────────────┬────────────────────────────────────────┐")
print(f"│ Metric                  │ Stacking Regressor   │ Interpretation                         │")
print(f"├─────────────────────────┼──────────────────────┼────────────────────────────────────────┤")
print(f"│ Mean Absolute Error     │ {mae:16.2f} Ton │ Rata-rata deviasi tebakan vs riil      │")
print(f"│ Root Mean Squared Error │ {rmse:16.2f} Ton │ Penalti deviasi ekstrem                │")
print(f"│ R-Squared (R² Score)    │ {r2*100:15.2f}% │ Varian data riil yang dapat dijelaskan │")
print(f"│ MAPE (Error Persentase) │ {mape:15.2f}% │ Tingkat persentase eror rata-rata      │")
print(f"└─────────────────────────┴──────────────────────┴────────────────────────────────────────┘")

# Feature Importance Approximation for Stacking Model
meta_coefs = np.abs(best_model.final_estimator_.coef_)
meta_coefs /= (np.sum(meta_coefs) + 1e-9)

importances = np.zeros(len(feature_cols))
for i, (name, est) in enumerate(best_model.estimators):
    fitted_est = best_model.estimators_[i]
    if hasattr(fitted_est, 'feature_importances_'):
        importances += fitted_est.feature_importances_ * meta_coefs[i]
    elif hasattr(fitted_est, 'coef_'):
        coefs = np.abs(fitted_est.coef_)
        importances += (coefs / (np.sum(coefs) + 1e-9)) * meta_coefs[i]

importances /= (np.sum(importances) + 1e-9)

print("\n[Features] FITUR SPASIAL PALING BERPENGARUH PADA TIMBULAN SAMPAH:")
for name, imp in sorted(zip(feature_cols, importances), key=lambda x: x[1], reverse=True):
    print(f"   - {name:22s}: {imp*100:5.2f}%")

# ==========================================
# 6. MODEL PERFORMANCE PLOT GENERATION
# ==========================================
if HAS_MATPLOTLIB:
    print("\n[Plot] Membuat Visualisasi Scatter Plot Actual vs Predicted...")
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, pred_test, alpha=0.4, color='#00f2fe', edgecolors='#0072ff', label='Stacking Regressor Predictions')
    
    # Perfect prediction line (y = x)
    min_val = min(y_test.min(), pred_test.min())
    max_val = max(y_test.max(), pred_test.max())
    plt.plot([min_val, max_val], [min_val, max_val], color='#ff007f', linestyle='--', linewidth=2, label='Perfect Prediction')
    
    plt.title('Stacking Regressor: Actual vs Predicted Waste Volume (DKI Jakarta)', fontsize=14, color='#0f172a', pad=15)
    plt.xlabel('Actual Waste Volume (tons)', fontsize=12)
    plt.ylabel('Predicted Waste Volume (tons)', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper left')
    
    # Dark theme styling adjustments
    plt.tight_layout()
    
    # Ensure target directories exist
    os.makedirs("frontend", exist_ok=True)
    plot_path = "frontend/model_actual_vs_predicted.png"
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"[Plot] Saved performance plot to '{plot_path}'!")
else:
    print("\n[Plot] Skipping visualization plot generation because matplotlib is not installed.")

# Save model artifacts
os.makedirs("models", exist_ok=True)
model_file_path = "models/model_sampah_advanced.pkl"
meta_file_path = "models/model_metadata.pkl"

metadata = {
    "feature_cols": feature_cols,
    "zone_map": zone_map,
    "metrics": {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "mape": float(mape)
    },
    "best_params": {
        "meta_coefs": meta_coefs.tolist()
    }
}

joblib.dump(best_model, model_file_path)
joblib.dump(metadata, meta_file_path)

print(f"\n[Save] SUCCESS! Saved Stacking Regressor model to '{model_file_path}' and metadata to '{meta_file_path}'!")
