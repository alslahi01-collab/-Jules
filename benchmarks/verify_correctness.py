import pandas as pd
import numpy as np
import os
from app import process_comparison as process_optimized

# I'll need the original process_comparison to compare results.
# Since I'm going to overwrite it, I'll first save a copy of the current app.py
# Or I can just implement the original logic here for verification.

def process_original(path1, path2, col1, col2):
    import re
    from thefuzz import fuzz

    def normalize_arabic_orig(text):
        if not isinstance(text, str): return str(text)
        text = re.sub(r'[\u064B-\u0652]', '', text)
        text = re.sub(r'[أإآ]', 'ا', text)
        text = re.sub(r'ة', 'ه', text)
        text = re.sub(r'ى', 'ي', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def detect_header_row_orig(df_raw):
        max_non_null = 0
        header_idx = 0
        for i in range(min(len(df_raw), 10)):
            non_null_count = df_raw.iloc[i].count()
            if non_null_count > max_non_null:
                max_non_null = non_null_count
                header_idx = i
        return header_idx

    xls1 = pd.ExcelFile(path1)
    xls2 = pd.ExcelFile(path2)
    matches_100, matches_75_99, matches_50_74 = [], [], []

    for s1 in xls1.sheet_names:
        df1_raw = pd.read_excel(xls1, sheet_name=s1, header=None)
        h1 = detect_header_row_orig(df1_raw)
        df1 = pd.read_excel(xls1, sheet_name=s1, header=h1)
        df1.columns = df1.columns.astype(str).str.strip()
        if col1 not in df1.columns: continue

        for s2 in xls2.sheet_names:
            df2_raw = pd.read_excel(xls2, sheet_name=s2, header=None)
            h2 = detect_header_row_orig(df2_raw)
            df2 = pd.read_excel(xls2, sheet_name=s2, header=h2)
            df2.columns = df2.columns.astype(str).str.strip()
            if col2 not in df2.columns: continue

            for idx1, row1 in df1.iterrows():
                val1 = str(row1[col1]); norm1 = normalize_arabic_orig(val1)
                if not norm1 or norm1 == 'nan': continue
                for idx2, row2 in df2.iterrows():
                    val2 = str(row2[col2]); norm2 = normalize_arabic_orig(val2)
                    if not norm2 or norm2 == 'nan': continue
                    if norm1 == norm2:
                        matches_100.append(row1.to_dict()); continue
                    score = fuzz.ratio(norm1, norm2)
                    if score >= 75: matches_75_99.append(row1.to_dict())
                    elif score >= 50: matches_50_74.append(row1.to_dict())
    return len(matches_100), len(matches_75_99), len(matches_50_74)

def run_verification():
    from benchmarks.benchmark import generate_test_data
    f1, f2 = generate_test_data(50)

    print("Running original logic...")
    orig_counts = process_original(f1, f2, 'Name', 'Name')

    print("Running optimized logic...")
    results = process_optimized(f1, f2, 'Name', 'Name')
    opt_counts = (len(results['matches_100']), len(results['matches_75_99']), len(results['matches_50_74']))

    print(f"Original counts: {orig_counts}")
    print(f"Optimized counts: {opt_counts}")

    if orig_counts == opt_counts:
        print("SUCCESS: Match counts are identical.")
    else:
        print("FAILURE: Match counts differ!")
        exit(1)

    if os.path.exists(f1): os.remove(f1)
    if os.path.exists(f2): os.remove(f2)

if __name__ == "__main__":
    run_verification()
