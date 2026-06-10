import time
import pandas as pd
import numpy as np
import os
from app import process_comparison

# Generate synthetic data
def generate_test_data(rows=100):
    np.random.seed(42)
    data1 = {
        'Name': [f"Name_{i}" for i in range(rows)],
        'Other': np.random.rand(rows)
    }
    data2 = {
        'Name': [f"Name_{i}" for i in range(rows)],
        'Other': np.random.rand(rows)
    }
    # Introduce some variations
    data2['Name'][rows//2:] = [f"NameX_{i}" for i in range(rows//2, rows)]

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    file1 = f'benchmarks/test1_{rows}.xlsx'
    file2 = f'benchmarks/test2_{rows}.xlsx'

    df1.to_excel(file1, index=False)
    df2.to_excel(file2, index=False)

    return file1, file2

def run_benchmark(rows=100):
    f1, f2 = generate_test_data(rows)

    start_time = time.time()
    results = process_comparison(f1, f2, 'Name', 'Name')
    end_time = time.time()

    duration = end_time - start_time
    print(f"Benchmark with {rows} rows took {duration:.4f} seconds")

    # Clean up
    if os.path.exists(f1): os.remove(f1)
    if os.path.exists(f2): os.remove(f2)

    return duration

if __name__ == "__main__":
    run_benchmark(500)
