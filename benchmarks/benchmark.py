import pandas as pd
import numpy as np
import time
from app import process_comparison as process_comparison_flask
from streamlit_app import process_comparison as process_comparison_streamlit
import os

def generate_test_excel(filename, num_rows, col_name):
    data = {
        col_name: [f"قيمة تجريبية {i}" for i in range(num_rows)],
        "other_col": np.random.rand(num_rows)
    }
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def run_benchmark():
    file1 = "test_file1.xlsx"
    file2 = "test_file2.xlsx"
    num_rows = 200
    col1 = "اسم"
    col2 = "اسم"

    generate_test_excel(file1, num_rows, col1)
    # Generate file2 with some modifications to trigger fuzzy matching
    data2 = {
        col2: [f"قيمة تجريبية {i}" if i % 2 == 0 else f"قيمة تجريبيه {i}" for i in range(num_rows)],
        "other_col": np.random.rand(num_rows)
    }
    df2 = pd.DataFrame(data2)
    df2.to_excel(file2, index=False)

    print(f"Benchmarking with {num_rows}x{num_rows} rows...")

    # Benchmark Flask version
    start_time = time.time()
    process_comparison_flask(file1, file2, col1, col2)
    flask_duration = time.time() - start_time
    print(f"Flask process_comparison took: {flask_duration:.4f} seconds")

    # Benchmark Streamlit version
    # Streamlit version takes file objects or paths?
    # In streamlit_app.py: xls1 = pd.ExcelFile(file1) - pd.ExcelFile accepts path or file-like
    start_time = time.time()
    process_comparison_streamlit(file1, file2, col1, col2)
    streamlit_duration = time.time() - start_time
    print(f"Streamlit process_comparison took: {streamlit_duration:.4f} seconds")

    os.remove(file1)
    os.remove(file2)

if __name__ == "__main__":
    run_benchmark()
