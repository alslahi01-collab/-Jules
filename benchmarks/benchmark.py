import os
import pandas as pd
import time
import numpy as np
from app import process_comparison

def create_sample_excel(filename, num_rows, col_name, seed=42):
    np.random.seed(seed)
    data = {
        col_name: [f"قيمة {i}" for i in range(num_rows)],
        "OtherCol": np.random.randint(0, 1000, size=num_rows)
    }
    # Introduce some variations for fuzzy matching
    for i in range(0, num_rows, 10):
        data[col_name][i] = data[col_name][i] + " اضافة"

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    file1 = "benchmarks/file1.xlsx"
    file2 = "benchmarks/file2.xlsx"
    num_rows = 200 # Small enough to run quickly but large enough to see difference

    create_sample_excel(file1, num_rows, "اسم_العميل")
    create_sample_excel(file2, num_rows, "اسم_العميل", seed=43)

    start_time = time.time()
    results = process_comparison(file1, file2, "اسم_العميل", "اسم_العميل")
    end_time = time.time()

    print(f"Comparison took {end_time - start_time:.4f} seconds")
    print(f"Matches 100%: {len(results['matches_100'])}")
    print(f"Matches 75-99%: {len(results['matches_75_99'])}")
    print(f"Matches 50-74%: {len(results['matches_50_74'])}")
