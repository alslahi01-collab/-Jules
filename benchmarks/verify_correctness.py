import pandas as pd
import numpy as np
import os
import sys
import re
from thefuzz import fuzz

# Original functions from app.py
def normalize_arabic_orig(text):
    if not isinstance(text, str):
        return str(text)
    text = re.sub(r'[\u064B-\u0652]', '', text)
    text = re.sub(r'[أإآ]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def detect_header_row(df_raw):
    max_non_null = 0
    header_idx = 0
    for i in range(min(len(df_raw), 10)):
        non_null_count = df_raw.iloc[i].count()
        if non_null_count > max_non_null:
            max_non_null = non_null_count
            header_idx = i
    return header_idx

def process_sheets_orig(xls1, s1, xls2, s2, col1, col2, matches_100, matches_75_99, matches_50_74):
    df1_raw = pd.read_excel(xls1, sheet_name=s1, header=None)
    h1 = detect_header_row(df1_raw)
    df1 = pd.read_excel(xls1, sheet_name=s1, header=h1)
    df1.columns = df1.columns.astype(str).str.strip()

    df2_raw = pd.read_excel(xls2, sheet_name=s2, header=None)
    h2 = detect_header_row(df2_raw)
    df2 = pd.read_excel(xls2, sheet_name=s2, header=h2)
    df2.columns = df2.columns.astype(str).str.strip()

    if col1 in df1.columns and col2 in df2.columns:
        for idx1, row1 in df1.iterrows():
            val1 = str(row1[col1])
            norm1 = normalize_arabic_orig(val1)
            if not norm1 or norm1 == 'nan': continue

            for idx2, row2 in df2.iterrows():
                val2 = str(row2[col2])
                norm2 = normalize_arabic_orig(val2)
                if not norm2 or norm2 == 'nan': continue

                if norm1 == norm2:
                    match_row = row1.to_dict()
                    match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                    match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                    matches_100.append(match_row)
                    continue

                score = fuzz.ratio(norm1, norm2)
                if score >= 75:
                    match_row = row1.to_dict()
                    match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                    match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                    matches_75_99.append(match_row)
                elif score >= 50:
                    match_row = row1.to_dict()
                    match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                    match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                    matches_50_74.append(match_row)

# Optimized version
import functools

@functools.lru_cache(maxsize=4096)
def normalize_arabic_opt(text):
    if not isinstance(text, str):
        return str(text)
    text = re.sub(r'[\u064B-\u0652]', '', text)
    text = re.sub(r'[أإآ]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_sheets_opt(xls1, s1, xls2, s2, col1, col2, matches_100, matches_75_99, matches_50_74):
    df1_raw = pd.read_excel(xls1, sheet_name=s1, header=None)
    h1 = detect_header_row(df1_raw)
    df1 = pd.read_excel(xls1, sheet_name=s1, header=h1)
    df1.columns = df1.columns.astype(str).str.strip()

    df2_raw = pd.read_excel(xls2, sheet_name=s2, header=None)
    h2 = detect_header_row(df2_raw)
    df2 = pd.read_excel(xls2, sheet_name=s2, header=h2)
    df2.columns = df2.columns.astype(str).str.strip()

    if col1 not in df1.columns or col2 not in df2.columns:
        return

    records1 = df1.to_dict('records')
    records2 = df2.to_dict('records')

    norm2_map = {}
    for i2, rec2 in enumerate(records2):
        n2 = normalize_arabic_opt(str(rec2.get(col2, '')))
        if n2 and n2 != 'nan':
            norm2_map.setdefault(n2, []).append(i2)

    unique_norms2 = list(norm2_map.keys())
    fuzz_cache = {}

    for i1, rec1 in enumerate(records1):
        val1 = str(rec1.get(col1, ''))
        norm1 = normalize_arabic_opt(val1)
        if not norm1 or norm1 == 'nan': continue

        # 100% matches
        if norm1 in norm2_map:
            for i2 in norm2_map[norm1]:
                match_row = rec1.copy()
                match_row['Similarity Location'] = f"Row {i1+h1+2} in {s1} vs Row {i2+h2+2} in {s2}"
                match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                matches_100.append(match_row)

        # Fuzzy matches
        for n2 in unique_norms2:
            if norm1 == n2: continue

            pair = tuple(sorted((norm1, n2)))
            if pair in fuzz_cache:
                score = fuzz_cache[pair]
            else:
                score = fuzz.ratio(norm1, n2)
                fuzz_cache[pair] = score

            if score >= 50:
                # Need to add for EACH row in df2 that has this n2
                count = len(norm2_map[n2])
                for _ in range(count):
                    match_row = rec1.copy()
                    match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                    match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                    if score >= 75:
                        matches_75_99.append(match_row)
                    else:
                        matches_50_74.append(match_row)

def test_correctness():
    data1 = {'Name': ['محمد', 'أحمد', 'محمد', 'علي'], 'Age': [20, 25, 30, 35]}
    data2 = {'Name': ['محمد', 'احمد', 'محمد '], 'Job': ['Eng', 'Doc', 'Tch']}
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    file1 = "v_test1.xlsx"
    file2 = "v_test2.xlsx"
    df1.to_excel(file1, index=False)
    df2.to_excel(file2, index=False)

    xls1 = pd.ExcelFile(file1)
    xls2 = pd.ExcelFile(file2)

    m100_orig, m75_orig, m50_orig = [], [], []
    process_sheets_orig(xls1, 'Sheet1', xls2, 'Sheet1', 'Name', 'Name', m100_orig, m75_orig, m50_orig)

    m100_opt, m75_opt, m50_opt = [], [], []
    process_sheets_opt(xls1, 'Sheet1', xls2, 'Sheet1', 'Name', 'Name', m100_opt, m75_opt, m50_opt)

    print(f"Orig: 100%={len(m100_orig)}, 75-99%={len(m75_orig)}, 50-74%={len(m50_orig)}")
    print(f"Opt:  100%={len(m100_opt)}, 75-99%={len(m75_opt)}, 50-74%={len(m50_opt)}")

    assert len(m100_orig) == len(m100_opt)
    assert len(m75_orig) == len(m75_opt)
    assert len(m50_orig) == len(m50_opt)

    # Sort and compare
    df_m100_orig = pd.DataFrame(m100_orig).sort_values(by=['Age', 'Similarity Location']).reset_index(drop=True)
    df_m100_opt = pd.DataFrame(m100_opt).sort_values(by=['Age', 'Similarity Location']).reset_index(drop=True)
    pd.testing.assert_frame_equal(df_m100_orig, df_m100_opt)

    print("Success! Optimized version is correct.")

    os.remove(file1)
    os.remove(file2)

if __name__ == "__main__":
    test_correctness()
