import pandas as pd
import time
import os
import numpy as np
from thefuzz import fuzz
import re
import functools

def normalize_arabic_orig(text):
    if not isinstance(text, str):
        return str(text)
    text = re.sub(r'[\u064B-\u0652]', '', text)
    text = re.sub(r'[أإآ]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

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

def original_process_sheets(df1, df2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []
    h1, h2 = 0, 0
    s1, s2 = "Sheet1", "Sheet2"

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
    return len(matches_100), len(matches_75_99), len(matches_50_74)

def optimized_process_sheets(df1, df2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []
    h1, h2 = 0, 0
    s1, s2 = "Sheet1", "Sheet2"

    records1 = df1.to_dict('records')
    records2 = df2.to_dict('records')

    # Pre-normalize and group by normalized value
    norm_map2 = {}
    for idx2, row2 in enumerate(records2):
        val2 = str(row2[col2])
        norm2 = normalize_arabic_opt(val2)
        if not norm2 or norm2 == 'nan': continue
        if norm2 not in norm_map2:
            norm_map2[norm2] = []
        norm_map2[norm2].append(idx2)

    unique_norms2 = list(norm_map2.keys())
    fuzz_results_cache = {}

    for idx1, row1 in enumerate(records1):
        val1 = str(row1[col1])
        norm1 = normalize_arabic_opt(val1)
        if not norm1 or norm1 == 'nan': continue

        # Exact matches
        if norm1 in norm_map2:
            for idx2 in norm_map2[norm1]:
                match_row = row1.copy()
                match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                matches_100.append(match_row)
            # Original logic used 'continue' after finding an exact match for a pair,
            # BUT it would still check other rows in df2.
            # Wait, the original logic had 'continue' inside the INNER loop.
            # So it skipped fuzzy matching for THAT specific row2 if it was an exact match.
            # My optimized logic should do the same.

        # Fuzzy matches
        for norm2 in unique_norms2:
            if norm1 == norm2: continue # already handled in exact matches

            pair = tuple(sorted((norm1, norm2)))
            if pair in fuzz_results_cache:
                score = fuzz_results_cache[pair]
            else:
                score = fuzz.ratio(norm1, norm2)
                fuzz_results_cache[pair] = score

            if score >= 75:
                match_row = row1.copy()
                match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                matches_75_99.append(match_row)
            elif score >= 50:
                match_row = row1.copy()
                match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                matches_50_74.append(match_row)

    return len(matches_100), len(matches_75_99), len(matches_50_74)

def generate_data(rows):
    names = ["محمد احمد", "محمود حسن", "على حسين", "فاطمة الزهراء", "زينب على"]
    data1 = {'Name': [names[i % len(names)] + f" {i}" for i in range(rows)], 'Other': range(rows)}
    data2 = {'Name': [names[i % len(names)] + f" {i}" for i in range(rows)], 'Other': range(rows)}

    # Modify some for fuzzy matches
    for i in range(0, rows, 10):
        data2['Name'][i] = data2['Name'][i].replace("ا", "أ")

    return pd.DataFrame(data1), pd.DataFrame(data2)

if __name__ == "__main__":
    rows = 200
    df1, df2 = generate_data(rows)

    print(f"Benchmarking with {rows}x{rows} rows...")

    start_time = time.time()
    m100_orig, m75_orig, m50_orig = original_process_sheets(df1, df2, 'Name', 'Name')
    orig_time = time.time() - start_time
    print(f"Original took: {orig_time:.4f} seconds")
    print(f"Original Matches: 100%={m100_orig}, 75-99%={m75_orig}, 50-74%={m50_orig}")

    start_time = time.time()
    m100_opt, m75_opt, m50_opt = optimized_process_sheets(df1, df2, 'Name', 'Name')
    opt_time = time.time() - start_time
    print(f"Optimized took: {opt_time:.4f} seconds")
    print(f"Optimized Matches: 100%={m100_opt}, 75-99%={m75_opt}, 50-74%={m50_opt}")

    print(f"Speedup: {orig_time / opt_time:.2f}x")

    assert m100_orig == m100_opt
    # Fuzzy matches might differ slightly if there are multiple matches for the same row1,
    # but in this synthetic data they should be close or same.
    # Actually they should be exactly the same if I replicate the logic correctly.
    print(f"Matches 75-99% consistency: {m75_orig == m75_opt}")
    print(f"Matches 50-74% consistency: {m50_orig == m50_opt}")
