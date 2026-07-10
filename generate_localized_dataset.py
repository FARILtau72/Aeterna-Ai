import pandas as pd
import numpy as np

def generate_local_data():
    print("Starting localized dataset generation...")
    
    # Load original dataset
    try:
        df_global = pd.read_csv("dataset_vibe_coder_2026.csv")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    # Ensure chronological order
    df_global['TANGGAL'] = pd.to_datetime(df_global['TANGGAL'])
    df_global = df_global.sort_values('TANGGAL').reset_index(drop=True)

    # Add lag features on global level (weather is shared across Jakarta)
    df_global['Rain_Lag_1'] = df_global['RR'].shift(1).fillna(0.0)
    df_global['Rain_Lag_2'] = df_global['RR'].shift(2).fillna(0.0)

    # Holiday checker for major Indonesian holidays in 2026
    def get_holiday_flag(date_obj):
        m, d = date_obj.month, date_obj.day
        # Specific holiday dates in 2026
        holidays = {
            (1, 1),   # New Year
            (2, 17),  # Imlek
            (3, 18),  # Nyepi
            (3, 19),  # Eid al-Fitr Day 1
            (3, 20),  # Eid al-Fitr Day 2
            (4, 3),   # Good Friday
            (5, 1),   # Labor Day
            (5, 14),  # Ascension Day
            (5, 27),  # Eid al-Adha Day 1
            (5, 28),  # Eid al-Adha Day 2
            (5, 31),  # Waisak
            (6, 16),  # Islamic New Year
            (8, 17),  # Independence Day
            (8, 25),  # Prophet Birthday
            (12, 25)  # Christmas
        }
        # Eid al-Fitr mudik window: March 15 to March 26
        if m == 3 and (15 <= d <= 26):
            return 1
        if (m, d) in holidays:
            return 1
        return 0

    df_global['Is_Holiday'] = df_global['TANGGAL'].apply(get_holiday_flag)
    df_global['Hari_Dalam_Minggu'] = df_global['TANGGAL'].dt.dayofweek
    df_global['Bulan'] = df_global['TANGGAL'].dt.month

    local_rows = []
    for idx, row in df_global.iterrows():
        date_str = row['TANGGAL'].strftime("%Y-%m-%d")
        global_vol = row['Volume_Total_Ton']
        rr = row['RR']
        rain_lag1 = row['Rain_Lag_1']
        rain_lag2 = row['Rain_Lag_2']
        is_holiday = row['Is_Holiday']
        ada_event = row['Ada_Event']
        crowd_scale = row['Crowd_Scale']
        hari_ke = row['Hari_Ke']
        is_weekend = row['Is_Weekend']
        hari_dalam_minggu = row['Hari_Dalam_Minggu']
        bulan = row['Bulan']
        
        # Apply Lebaran mudik population drop factor
        # If inside March Lebaran window, drop global base volume by 35%
        vol_scale = global_vol
        if is_holiday == 1 and row['TANGGAL'].month == 3:
            vol_scale = global_vol * 0.65
            
        # JIS (North Jakarta)
        # Base volume: ~120 tons average
        jis_vol = vol_scale * (120.0 / 7700.0)
        # Event spikes at Stadium
        if ada_event == 1:
            jis_vol += crowd_scale * 15.0
        # Weekend recreation factor
        if is_weekend == 1:
            jis_vol *= 1.05
        local_rows.append({
            'Tanggal': date_str, 'Location': 'JIS', 'Volume_Ton': jis_vol,
            'RR': rr, 'Rain_Lag_1': rain_lag1, 'Rain_Lag_2': rain_lag2,
            'Is_Holiday': is_holiday, 'Ada_Event': ada_event, 'Crowd_Scale': crowd_scale,
            'Hari_Ke': hari_ke, 'Is_Weekend': is_weekend, 'Hari_Dalam_Minggu': hari_dalam_minggu, 'Bulan': bulan
        })
        
        # GBK (Central/South)
        # Base volume: ~85 tons average
        gbk_vol = vol_scale * (85.0 / 7700.0)
        # Event spikes at Stadium
        if ada_event == 1:
            gbk_vol += crowd_scale * 12.0
        # Weekend public sports factor
        if is_weekend == 1:
            gbk_vol *= 1.15
        local_rows.append({
            'Tanggal': date_str, 'Location': 'GBK', 'Volume_Ton': gbk_vol,
            'RR': rr, 'Rain_Lag_1': rain_lag1, 'Rain_Lag_2': rain_lag2,
            'Is_Holiday': is_holiday, 'Ada_Event': ada_event, 'Crowd_Scale': crowd_scale,
            'Hari_Ke': hari_ke, 'Is_Weekend': is_weekend, 'Hari_Dalam_Minggu': hari_dalam_minggu, 'Bulan': bulan
        })
        
        # Pasar Senen (Central)
        # Base volume: ~45 tons average
        senen_vol = vol_scale * (45.0 / 7700.0)
        # Weekday market commerce factor
        if is_weekend == 0:
            senen_vol *= 1.10
        local_rows.append({
            'Tanggal': date_str, 'Location': 'Pasar Senen', 'Volume_Ton': senen_vol,
            'RR': rr, 'Rain_Lag_1': rain_lag1, 'Rain_Lag_2': rain_lag2,
            'Is_Holiday': is_holiday, 'Ada_Event': 0, 'Crowd_Scale': 0,
            'Hari_Ke': hari_ke, 'Is_Weekend': is_weekend, 'Hari_Dalam_Minggu': hari_dalam_minggu, 'Bulan': bulan
        })
        
        # Gang Sempit Tambora (West)
        # Base volume: ~8.5 tons average
        tambora_vol = vol_scale * (8.5 / 7700.0)
        # Hujan block factor (heavy rain delays alley collection)
        if rr > 20:
            tambora_vol *= 0.75
        local_rows.append({
            'Tanggal': date_str, 'Location': 'Gang Sempit Tambora', 'Volume_Ton': tambora_vol,
            'RR': rr, 'Rain_Lag_1': rain_lag1, 'Rain_Lag_2': rain_lag2,
            'Is_Holiday': is_holiday, 'Ada_Event': 0, 'Crowd_Scale': 0,
            'Hari_Ke': hari_ke, 'Is_Weekend': is_weekend, 'Hari_Dalam_Minggu': hari_dalam_minggu, 'Bulan': bulan
        })

    df_local = pd.DataFrame(local_rows)
    df_local.to_csv("dataset_local_2026.csv", index=False)
    print("dataset_local_2026.csv generated successfully with 1460 rows!")

if __name__ == "__main__":
    generate_local_data()
