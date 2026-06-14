import pandas as pd
import numpy as np
import time
import os
import sys
from thefuzz import fuzz

# Add root to path to import from app.py
sys.path.append(os.getcwd())
from app import normalize_arabic, process_sheets

def generate_dummy_data(rows):
    data = {
        'Name': [f'اسم الشخص {i}' for i in range(rows)],
        'ID': range(rows)
    }
    # Add some duplicates and slight variations
    data['Name'][0] = 'أحمد محمد'
    data['Name'][1] = 'احمد محمد'
    data['Name'][2] = 'أحمد محمود'
    return pd.DataFrame(data)

def run_benchmark():
    rows = 200
    df1 = generate_dummy_data(rows)
    df2 = generate_dummy_data(rows)

    # Mocking ExcelFile objects
    class MockXls:
        def __init__(self, df):
            self.df = df
            self.sheet_names = ['Sheet1']

    # We need to mock pd.read_excel since process_sheets calls it
    # For benchmarking just the core logic, we might need to refactor a bit
    # or just use dummy files.

    f1 = 'benchmarks/test1.xlsx'
    f2 = 'benchmarks/test2.xlsx'
    df1.to_excel(f1, index=False)
    df2.to_excel(f2, index=False)

    xls1 = pd.ExcelFile(f1)
    xls2 = pd.ExcelFile(f2)

    m100, m75, m50 = [], [], []

    start_time = time.time()
    process_sheets(xls1, 'Sheet1', xls2, 'Sheet1', 'Name', 'Name', m100, m75, m50)
    end_time = time.time()

    print(f"Benchmark took: {end_time - start_time:.4f} seconds")
    print(f"Matches 100: {len(m100)}")
    print(f"Matches 75-99: {len(m75)}")
    print(f"Matches 50-74: {len(m50)}")

if __name__ == "__main__":
    run_benchmark()
