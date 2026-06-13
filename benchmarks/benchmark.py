import time
import pandas as pd
import numpy as np
import os
import sys
from io import BytesIO

# Add root to path so we can import app and streamlit_app
sys.path.append(os.getcwd())

from app import process_comparison as process_comparison_flask
from streamlit_app import process_comparison as process_comparison_streamlit

def generate_test_data(rows1=100, rows2=100):
    # Generate some Arabic-like names with variations
    names = ["أحمد محمد", "احمد محمد", "محمد علي", "محمد على", "فاطمة الزهراء", "فاطمه الزهراء", "زيد بن حارثة", "زيد بن حارثه"]

    data1 = {
        'Name': [np.random.choice(names) for _ in range(rows1)],
        'ID': range(rows1),
        'Other': np.random.randn(rows1)
    }
    data2 = {
        'Name': [np.random.choice(names) for _ in range(rows2)],
        'ID': range(rows2),
        'Other': np.random.randn(rows2)
    }

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    path1 = "test1.xlsx"
    path2 = "test2.xlsx"

    with pd.ExcelWriter(path1) as writer:
        df1.to_excel(writer, index=False, sheet_name="Sheet1")

    with pd.ExcelWriter(path2) as writer:
        df2.to_excel(writer, index=False, sheet_name="Sheet1")

    return path1, path2

def run_benchmark():
    rows1, rows2 = 500, 500
    print(f"Generating test data with {rows1} and {rows2} rows...")
    p1, p2 = generate_test_data(rows1, rows2)

    print("Benchmarking Flask process_comparison...")
    start = time.time()
    results_flask = process_comparison_flask(p1, p2, "Name", "Name")
    end = time.time()
    flask_time = end - start
    print(f"Flask Time: {flask_time:.4f}s")

    print("Benchmarking Streamlit process_comparison...")
    # Streamlit version takes file objects or paths depending on implementation,
    # but in streamlit_app.py it uses pd.ExcelFile(file1) which works with paths.
    start = time.time()
    results_streamlit = process_comparison_streamlit(p1, p2, "Name", "Name")
    end = time.time()
    streamlit_time = end - start
    print(f"Streamlit Time: {streamlit_time:.4f}s")

    # Cleanup
    os.remove(p1)
    os.remove(p2)

    return flask_time, streamlit_time

if __name__ == "__main__":
    run_benchmark()
