import pandas as pd
import numpy as np
import time
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from app import process_comparison

def generate_test_excel(filename, rows=500):
    np.random.seed(42)
    data = {
        'Name': [f"اسم الشخص رقم {i}" for i in range(rows)],
        'ID': range(rows),
        'City': ['القاهرة', 'الجيزة', 'الإسكندرية'] * (rows // 3 + 1)
    }
    # Add some duplicates and slight variations
    df = pd.DataFrame({k: v[:rows] for k, v in data.items()})
    df.to_excel(filename, index=False)

def run_benchmark():
    file1 = 'benchmarks/test_file1.xlsx'
    file2 = 'benchmarks/test_file2.xlsx'
    os.makedirs('benchmarks', exist_ok=True)

    rows = 500
    generate_test_excel(file1, rows)
    generate_test_excel(file2, rows)

    print(f"Benchmarking app.py process_comparison ({rows}x{rows})...")
    start = time.time()
    results = process_comparison(file1, file2, 'Name', 'Name')
    end = time.time()
    print(f"Time: {end - start:.4f}s")
    print(f"Matches 100: {len(results['matches_100'])}")
    print(f"Matches 75-99: {len(results['matches_75_99'])}")
    print(f"Matches 50-74: {len(results['matches_50_74'])}")

if __name__ == "__main__":
    run_benchmark()
