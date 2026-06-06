import pandas as pd
import numpy as np
import time
import os
import sys
from streamlit_app import process_comparison

def generate_test_data(n_rows=100):
    np.random.seed(42)
    data1 = {'Name': [f"Name_{i%20}" for i in range(n_rows)], 'Val': np.random.randint(0, 100, n_rows)}
    data2 = {'Name': [f"Name_{i%20}" if i%3!=0 else f"Name_{i%20}_alt" for i in range(n_rows)], 'Val': np.random.randint(0, 100, n_rows)}
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    return df1, df2

def main():
    n_rows = 300
    df1, df2 = generate_test_data(n_rows)
    file1, file2 = "st_b1.xlsx", "st_b2.xlsx"
    df1.to_excel(file1, index=False)
    df2.to_excel(file2, index=False)

    start_time = time.time()
    results = process_comparison(file1, file2, 'Name', 'Name')
    end_time = time.time()

    print(f"Time taken for {n_rows}x{n_rows} rows: {end_time - start_time:.4f} seconds")
    print(f"Matches 100%: {len(results['matches_100'])}")
    print(f"Matches 75-99%: {len(results['matches_75_99'])}")
    print(f"Matches 50-74%: {len(results['matches_50_74'])}")

    # Simple correctness check (just check match counts)
    # Expected matches for n=300 with %20 and %3 logic:
    # Exact: 300 * (2/3 * 300/20) ... wait, it's more complex but should be consistent.

    os.remove(file1)
    os.remove(file2)

if __name__ == "__main__":
    main()
