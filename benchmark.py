import pandas as pd
import time
import os
import random
import string
from app import process_comparison, normalize_arabic
from thefuzz import fuzz

def generate_sample_excel(filename, num_rows, columns, noise=False):
    data = []
    for i in range(num_rows):
        row = {}
        for col in columns:
            val = ''.join(random.choices(string.ascii_lowercase + "        ", k=10))
            if noise and random.random() > 0.8:
                val = val[:-1] + "!" # Introduce slight difference
            row[col] = val
        data.append(row)
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    f1 = "bench_file1.xlsx"
    f2 = "bench_file2.xlsx"

    # Generate ~500 rows for comparison
    rows = 500
    generate_sample_excel(f1, rows, ["Name", "ID"])
    generate_sample_excel(f2, rows, ["Name", "ID"], noise=True)

    print(f"Starting benchmark with {rows}x{rows} rows...")
    start_time = time.time()
    # In app.py, process_comparison expects file paths
    results = process_comparison(f1, f2, "Name", "Name")
    end_time = time.time()

    print(f"Comparison took: {end_time - start_time:.4f} seconds")
    print(f"Matches found: 100%: {len(results['matches_100'])}, 75-99%: {len(results['matches_75_99'])}, 50-74%: {len(results['matches_50_74'])}")

    # Cleanup
    if os.path.exists(f1): os.remove(f1)
    if os.path.exists(f2): os.remove(f2)
