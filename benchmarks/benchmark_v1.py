import pandas as pd
import numpy as np
import time
import os
import sys

# Add root to sys.path to import from app.py
sys.path.append(os.getcwd())
from app import normalize_arabic, process_sheets

def generate_test_data(n_rows=100):
    data1 = {
        'Name': [f"Name_{i}" for i in range(n_rows)],
        'Value': np.random.randint(0, 1000, n_rows)
    }
    data2 = {
        'Name': [f"Name_{i}" if i % 2 == 0 else f"Name_{i}_suffix" for i in range(n_rows)],
        'Value': np.random.randint(0, 1000, n_rows)
    }
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    # Add some Arabic names with variations
    arabic_names = ["محمد", "أحمد", "علي", "فاطمة", "زينب", "عائشة", "محمود", "إبراهيم", "مريم", "سارة"]
    for i in range(min(10, n_rows)):
        df1.iloc[i, 0] = arabic_names[i % len(arabic_names)]
        if i % 2 == 0:
            df2.iloc[i, 0] = arabic_names[i % len(arabic_names)] + " " # Extra space
        else:
            # Change Alif
            name = arabic_names[i % len(arabic_names)]
            if "أ" in name:
                name = name.replace("أ", "ا")
            elif "إ" in name:
                name = name.replace("إ", "ا")
            df2.iloc[i, 0] = name

    return df1, df2

def main():
    n_rows = 300 # Enough to see the impact but not too slow
    df1, df2 = generate_test_data(n_rows)

    file1 = "test1.xlsx"
    file2 = "test2.xlsx"
    df1.to_excel(file1, index=False)
    df2.to_excel(file2, index=False)

    xls1 = pd.ExcelFile(file1)
    xls2 = pd.ExcelFile(file2)

    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []

    start_time = time.time()
    process_sheets(xls1, 'Sheet1', xls2, 'Sheet1', 'Name', 'Name', matches_100, matches_75_99, matches_50_74)
    end_time = time.time()

    print(f"Time taken for {n_rows}x{n_rows} rows: {end_time - start_time:.4f} seconds")
    print(f"Matches 100%: {len(matches_100)}")
    print(f"Matches 75-99%: {len(matches_75_99)}")
    print(f"Matches 50-74%: {len(matches_50_74)}")

    os.remove(file1)
    os.remove(file2)

if __name__ == "__main__":
    main()
