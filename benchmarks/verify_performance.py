import pandas as pd
import time
import os
import sys
from thefuzz import fuzz
from io import BytesIO

# Add root to sys.path
sys.path.append(os.getcwd())

import app
import streamlit_app

def create_test_excel(n_rows):
    data = {'Name': [f'Person {i}' for i in range(n_rows)], 'Value': range(n_rows)}
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output

def benchmark_app(n_rows):
    file1 = create_test_excel(n_rows)
    file2 = create_test_excel(n_rows)

    # Need actual file paths for app.process_comparison but it uses pd.ExcelFile
    # We can pass the BytesIO objects directly if we mock pd.ExcelFile or just use real files
    with open('test1.xlsx', 'wb') as f: f.write(file1.getbuffer())
    with open('test2.xlsx', 'wb') as f: f.write(file2.getbuffer())

    start_time = time.time()
    results = app.process_comparison('test1.xlsx', 'test2.xlsx', 'Name', 'Name')
    end_time = time.time()

    print(f"App optimization results for {n_rows} rows:")
    print(f"  Time: {end_time - start_time:.4f}s")
    print(f"  Matches 100%: {len(results['matches_100'])}")

    os.remove('test1.xlsx')
    os.remove('test2.xlsx')
    return end_time - start_time

def benchmark_streamlit(n_rows):
    file1 = create_test_excel(n_rows)
    file2 = create_test_excel(n_rows)

    start_time = time.time()
    results = streamlit_app.process_comparison(file1, file2, 'Name', 'Name')
    end_time = time.time()

    print(f"Streamlit optimization results for {n_rows} rows:")
    print(f"  Time: {end_time - start_time:.4f}s")
    print(f"  Matches 100%: {len(results['matches_100'])}")
    return end_time - start_time

if __name__ == '__main__':
    n = 300
    t_app = benchmark_app(n)
    t_st = benchmark_streamlit(n)

    # Original baseline was ~10s for 300x300
    print(f"\nFinal verification:")
    print(f"App time: {t_app:.4f}s (Expected < 1s)")
    print(f"Streamlit time: {t_st:.4f}s (Expected < 1s)")
