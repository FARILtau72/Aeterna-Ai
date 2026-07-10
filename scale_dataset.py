import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("dataset_vibe_coder_2026.csv")

print("Original Stats:")
print(df[["Volume_Total_Ton", "Vol_Sisa_Makanan_Ton", "Vol_Plastik_Ton"]].describe())

# Scale values to match DKI Jakarta daily average (~7,700 tons/day)
# original mean is ~1,100 tons/day, so we scale by ~7
scale_factor = 7.0

df["Volume_Total_Ton"] = (df["Volume_Total_Ton"] * scale_factor).round(2)

# Organic/Food waste (Sisa Makanan) is ~49.87% of total
df["Vol_Sisa_Makanan_Ton"] = (df["Volume_Total_Ton"] * 0.4987).round(2)

# Plastic waste is ~22.95% of total
df["Vol_Plastik_Ton"] = (df["Volume_Total_Ton"] * 0.2295).round(2)

# Save the scaled dataset
df.to_csv("dataset_vibe_coder_2026.csv", index=False)

print("\nScaled Stats:")
print(df[["Volume_Total_Ton", "Vol_Sisa_Makanan_Ton", "Vol_Plastik_Ton"]].describe())
print("\nDataset successfully scaled to DKI Jakarta Province scale!")
