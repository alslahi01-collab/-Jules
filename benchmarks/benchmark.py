import pandas as pd
import numpy as np
import time
import os
from app import process_comparison
from streamlit_app import process_comparison as process_comparison_st

def generate_test_excel(filename, rows=500):
    np.random.seed(42)
    data = {
        'Name': [f"اسم الشخص رقم {i}" for i in range(rows)],
        'ID': range(rows),
        'City': ['القاهرة', 'الجيزة', 'الإسكندرية'] * (rows // 3 + 1)
    }
    # Add some duplicates and slight variations
    data['Name'][10] = "اسم الشخص رقم 0" # Exact match
    data['Name'][20] = "اسم الشحص رقم 0" # Fuzzy match (typo)

    df = pd.DataFrame(data[:rows] if isinstance(data, list) else {k: v[:rows] for k, v in data.items()})
    df.to_excel(filename, index=False)

def run_benchmark():
    file1 = 'benchmarks/test_file1.xlsx'
    file2 = 'benchmarks/test_file2.xlsx'
    os.makedirs('benchmarks', exist_ok=True)

    generate_test_excel(file1, 200)
    generate_test_excel(file2, 200)

    print("Benchmarking app.py process_comparison (200x200)...")
    start = time.time()
    # Mocking paths
    results = process_comparison(file1, file2, 'Name', 'Name')
    end = time.time()
    print(f"app.py time: {end - start:.4f}s")
    print(f"Matches 100: {len(results['matches_100'])}")
    print(f"Matches 75-99: {len(results['matches_75_99'])}")
    print(f"Matches 50-74: {len(results['matches_50_74'])}")

    print("\nBenchmarking streamlit_app.py process_comparison (200x200)...")
    # Need to mock file objects for streamlit version as it expects uploaded_file
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        start = time.time()
        results_st = process_comparison_st(f1, f2, 'Name', 'Name')
        end = time.time()
    print(f"streamlit_app.py time: {end - start:.4f}s")

if __name__ == "__main__":
    run_benchmark()
