import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')

print("MEMULAI PROSES TRAINING AI LEVEL PRODUCTION (LOCALIZED, LAG WEATHER & HOLIDAYS)...\n")

# ==========================================
# 1. LOAD LOCALIZED DATA
# ==========================================
print("1. Menarik & Memproses Data Historis Lokal...")
df = pd.read_csv('dataset_local_2026.csv')
df['Tanggal'] = pd.to_datetime(df['Tanggal'])

# Sort chronologically to maintain time order
df = df.sort_values(['Tanggal', 'Location']).reset_index(drop=True)

# ==========================================
# 2. FEATURE ENGINEERING (LOCAL BINDING)
# ==========================================
print("2. Melakukan One-Hot Encoding Lokasi & Verifikasi Fitur...")

# Defensive manual one-hot encoding to guarantee column names and order
locations = ['JIS', 'GBK', 'Pasar Senen', 'Gang Sempit Tambora']
for loc in locations:
    df[f'Loc_{loc}'] = (df['Location'] == loc).astype(int)

# Fitur yang dipakai AI buat berpikir
fitur = [
    'Loc_JIS', 'Loc_GBK', 'Loc_Pasar Senen', 'Loc_Gang Sempit Tambora',
    'RR', 'Rain_Lag_1', 'Rain_Lag_2', 'Is_Holiday', 'Ada_Event', 'Crowd_Scale',
    'Hari_Ke', 'Is_Weekend', 'Hari_Dalam_Minggu', 'Bulan'
]

X = df[fitur]
y = df['Volume_Ton']

# ==========================================
# 3. CHRONOLOGICAL SPLIT & TRAINING
# ==========================================
print("3. Membagi Data secara Kronologis (75/25) & Melatih Model...")

# 75% days for training, 25% for test. 
# Since we have 4 locations per day, we split at index: (len(df) // 4 * 0.75) * 4
num_days = len(df) // 4
train_days = int(num_days * 0.75)
train_size = train_days * 4

X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

# Menggunakan Gradient Boosting Regressor (Optimasi Parameter untuk Akurasi >90%)
model = GradientBoostingRegressor(
    n_estimators=300, 
    learning_rate=0.05, 
    max_depth=5, 
    random_state=42
)
model.fit(X_train, y_train)

# ==========================================
# 4. EVALUASI AKURASI
# ==========================================
print("4. Mengevaluasi Performa Model pada Data Pengujian...")
prediksi = model.predict(X_test)
rmse = mean_squared_error(y_test, prediksi) ** 0.5
mae = mean_absolute_error(y_test, prediksi)
r2 = r2_score(y_test, prediksi)

# Hitung Mean Absolute Percentage Error (MAPE)
mape = np.mean(np.abs((y_test - prediksi) / y_test)) * 100
akurasi = 100 - mape

print("\nHASIL EVALUASI MODEL (METRICS):")
print(f"   Root Mean Squared Error (RMSE) : {rmse:.2f} Ton")
print(f"   Mean Absolute Error (MAE)      : {mae:.2f} Ton")
print(f"   R-Squared (R2 Score)           : {r2 * 100:.2f}% (Tingkat Kepercayaan AI)")
print(f"   Mean Absolute Percentage Error (MAPE) : {mape:.2f}%")
print(f"   Akurasi Prediksi Sampah        : {akurasi:.2f}%")

# Cek Fitur Paling Berpengaruh
importances = model.feature_importances_
print("\nFITUR PALING BERPENGARUH PADA TIMBULAN SAMPAH:")
for name, importance in zip(fitur, importances):
    print(f"   - {name}: {importance*100:.1f}%")

# Simpan Model
joblib.dump(model, 'model_sampah_advanced.pkl')
print("\nSUCCESS! 'model_sampah_advanced.pkl' berhasil di-generate!")
