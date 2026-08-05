import os
import sys

# Ensure current working directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate_real_kecamatan_dataset import generate_dataset

def run_pipeline():
    print("🚀 Running full data generation and spatial model training pipeline...")
    df = generate_dataset()
    import train
    print("✨ Pipeline build completed successfully!")

if __name__ == "__main__":
    run_pipeline()
