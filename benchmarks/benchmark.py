import pandas as pd
import numpy as np
import time
import sys
import os
sys.path.append(os.getcwd())
import os
from app import process_comparison as process_comparison_app
from streamlit_app import process_comparison as process_comparison_streamlit

def generate_sample_excel(filename, num_rows, overlap_rows, seed=42):
    np.random.seed(seed)
    data = {
        'Name': [f"Name_{i}" for i in range(num_rows)],
        'Value': np.random.randint(1000, 9999, size=num_rows)
    }
    df = pd.DataFrame(data)

    # Add some Arabic names with variations
    arabic_names = ["محمد", "أحمد", "علي", "فاطمة", "زينب", "عمر", "عثمان", "خديجة", "عائشة", "حمزة"]
    for i in range(min(10, num_rows)):
        df.iloc[i, 0] = arabic_names[i]

    df.to_excel(filename, index=False)
    return df

def run_benchmark():
    file1 = 'test1.xlsx'
    file2 = 'test2.xlsx'
    num_rows = 1000 # Small enough to run quickly but large enough to see difference

    generate_sample_excel(file1, num_rows, 50, seed=42)
    generate_sample_excel(file2, num_rows, 50, seed=43)

    print(f"Benchmarking with {num_rows}x{num_rows} rows...")

    start_time = time.time()
    # Mock the xls1 and xls2 objects since app.py expects paths but streamlit_app.py expects file-like objects or paths
    # Actually app.py: process_comparison(path1, path2, col1, col2)
    # streamlit_app.py: process_comparison(file1, file2, col1, col2)

    print("Running app.py process_comparison...")
    res_app = process_comparison_app(file1, file2, 'Name', 'Name')
    app_time = time.time() - start_time
    print(f"App time: {app_time:.4f}s")

    start_time = time.time()
    print("Running streamlit_app.py process_comparison...")
    # streamlit_app.py's process_comparison also takes file paths if they are strings
    res_st = process_comparison_streamlit(file1, file2, 'Name', 'Name')
    st_time = time.time() - start_time
    print(f"Streamlit time: {st_time:.4f}s")

    # Cleanup
    if os.path.exists(file1): os.remove(file1)
    if os.path.exists(file2): os.remove(file2)

if __name__ == "__main__":
    run_benchmark()
