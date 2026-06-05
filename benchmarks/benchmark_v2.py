import pandas as pd
import time
import re
from thefuzz import fuzz
import numpy as np
import functools

@functools.lru_cache(maxsize=4096)
def normalize_arabic(text):
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r'[\u064B-\u0652]', '', text)
    text = re.sub(r'[أإآ]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_sheets_original(df1, df2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []
    h1, h2 = 0, 0
    s1, s2 = "Sheet1", "Sheet2"

    for idx1, row1 in df1.iterrows():
        val1 = str(row1[col1])
        norm1 = normalize_arabic(val1)
        if not norm1 or norm1 == 'nan': continue

        for idx2, row2 in df2.iterrows():
            val2 = str(row2[col2])
            norm2 = normalize_arabic(val2)
            if not norm2 or norm2 == 'nan': continue

            if norm1 == norm2:
                match_row = row1.to_dict()
                match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                matches_100.append(match_row)
                continue

            score = fuzz.ratio(norm1, norm2)
            if score >= 75:
                match_row = row1.to_dict()
                match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                matches_75_99.append(match_row)
            elif score >= 50:
                match_row = row1.to_dict()
                match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                matches_50_74.append(match_row)
    return matches_100, matches_75_99, matches_50_74

def process_sheets_optimized(df1, df2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []
    h1, h2 = 0, 0
    s1, s2 = "Sheet1", "Sheet2"

    # Pre-convert to records for faster access
    records1 = df1.to_dict('records')
    records2 = df2.to_dict('records')

    # Pre-normalize and group indices
    norm_map2 = {}
    for idx2, row2 in enumerate(records2):
        val2 = str(row2[col2])
        norm2 = normalize_arabic(val2)
        if not norm2 or norm2 == 'nan': continue
        if norm2 not in norm_map2:
            norm_map2[norm2] = []
        norm_map2[norm2].append(idx2)

    unique_norms2 = list(norm_map2.keys())

    # Cache for fuzzy results to avoid re-calculating for same norm1, norm2 pairs
    fuzz_results_cache = {}

    for idx1, row1 in enumerate(records1):
        val1 = str(row1[col1])
        norm1 = normalize_arabic(val1)
        if not norm1 or norm1 == 'nan': continue

        for norm2 in unique_norms2:
            if norm1 == norm2:
                for idx2 in norm_map2[norm2]:
                    match_row = row1.copy()
                    match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                    matches_100.append(match_row)
                continue

            # Fuzzy match
            pair = tuple(sorted((norm1, norm2)))
            if pair in fuzz_results_cache:
                score = fuzz_results_cache[pair]
            else:
                score = fuzz.ratio(norm1, norm2)
                fuzz_results_cache[pair] = score

            if score >= 75:
                match_row = row1.copy()
                match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                matches_75_99.append(match_row)
            elif score >= 50:
                match_row = row1.copy()
                match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                matches_50_74.append(match_row)

    return matches_100, matches_75_99, matches_50_74

# Create dummy data
n_rows = 300
data1 = {'Name': [f"Name {i % 50}" for i in range(n_rows)]}
data2 = {'Name': [f"Name {i % 50}" for i in range(10, n_rows + 10)]}
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

print(f"Benchmarking with {n_rows}x{n_rows} rows...")

start_time = time.time()
orig_m100, orig_m75, orig_m50 = process_sheets_original(df1, df2, 'Name', 'Name')
orig_time = time.time() - start_time
print(f"Original Time: {orig_time:.4f} seconds")

start_time = time.time()
opt_m100, opt_m75, opt_m50 = process_sheets_optimized(df1, df2, 'Name', 'Name')
opt_time = time.time() - start_time
print(f"Optimized Time: {opt_time:.4f} seconds")

print(f"Speedup: {orig_time / opt_time:.2f}x")

# Verify correctness
print(f"Verifying correctness...")
print(f"100% matches: Orig={len(orig_m100)}, Opt={len(opt_m100)}")
print(f"75-99% matches: Orig={len(orig_m75)}, Opt={len(opt_m75)}")
print(f"50-74% matches: Orig={len(orig_m50)}, Opt={len(opt_m50)}")

assert len(orig_m100) == len(opt_m100)
assert len(orig_m75) == len(opt_m75)
assert len(orig_m50) == len(opt_m50)
print("Correctness verified!")
