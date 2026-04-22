import pandas as pd
import time
import re
from thefuzz import fuzz
import numpy as np
from functools import lru_cache

@lru_cache(maxsize=4096)
def normalize_arabic(text):
    if not isinstance(text, str):
        text = str(text)

    # Remove diacritics
    text = re.sub(r'[\u064B-\u0652]', '', text)
    # Unify Alef
    text = re.sub(r'[أإآ]', 'ا', text)
    # Unify Teh Marbuta and Heh
    text = re.sub(r'ة', 'ه', text)
    # Unify Yeh
    text = re.sub(r'ى', 'ي', text)
    # Remove extra whitespace
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
        norm1 = normalize_arabic.__wrapped__(val1) # Use unwrapped to simulate no cache
        if not norm1 or norm1 == 'nan': continue

        for idx2, row2 in df2.iterrows():
            val2 = str(row2[col2])
            norm2 = normalize_arabic.__wrapped__(val2)
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
    return matches_100, matches_75_99, matches_50_74

def process_sheets_optimized(df1, df2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []
    h1, h2 = 0, 0
    s1, s2 = "Sheet1", "Sheet2"

    # Pre-normalize and store indices
    # We use dict to group by normalized value to avoid repeated fuzzy calculations
    df1_records = df1.to_dict('records')
    df2_records = df2.to_dict('records')

    norm1_list = [normalize_arabic(str(r[col1])) for r in df1_records]
    norm2_list = [normalize_arabic(str(r[col2])) for r in df2_records]

    # Group df2 by normalized value
    norm2_map = {}
    for idx2, n2 in enumerate(norm2_list):
        if not n2 or n2 == 'nan': continue
        if n2 not in norm2_map:
            norm2_map[n2] = []
        norm2_map[n2].append(idx2)

    unique_norm2 = list(norm2_map.keys())

    # Cache fuzzy results between unique normalized strings
    fuzz_cache = {}

    for idx1, n1 in enumerate(norm1_list):
        if not n1 or n1 == 'nan': continue

        row1_dict = df1_records[idx1]

        # 1. Exact matches
        if n1 in norm2_map:
            for idx2 in norm2_map[n1]:
                match_row = row1_dict.copy()
                match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                matches_100.append(match_row)

        # 2. Fuzzy matches
        for n2 in unique_norm2:
            if n1 == n2: continue

            pair = tuple(sorted((n1, n2)))
            if pair in fuzz_cache:
                score = fuzz_cache[pair]
            else:
                score = fuzz.ratio(n1, n2)
                fuzz_cache[pair] = score

            if score >= 50:
                # For each idx2 that has this n2
                for idx2 in norm2_map[n2]:
                    match_row = row1_dict.copy()
                    match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                    if score >= 75:
                        match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                        matches_75_99.append(match_row)
                    else:
                        match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                        matches_50_74.append(match_row)

    return matches_100, matches_75_99, matches_50_74

# Generate synthetic data
n_rows = 100
data1 = {'name': [f'اسم {i}' for i in range(n_rows)], 'val': range(n_rows)}
data2 = {'name': [f'إسم {i}' if i % 2 == 0 else f'مختلف {i}' for i in range(n_rows)], 'val': range(n_rows)}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

print(f"Benchmarking with {n_rows}x{n_rows} rows...")

start_time = time.time()
m100, m75, m50 = process_sheets_original(df1, df2, 'name', 'name')
end_time = time.time()
print(f"Original time: {end_time - start_time:.4f} seconds")
orig_len = len(m100) + len(m75) + len(m50)

# Reset cache for fair comparison of first run if needed, but here we want to see it in action
normalize_arabic.cache_clear()

start_time = time.time()
m100_opt, m75_opt, m50_opt = process_sheets_optimized(df1, df2, 'name', 'name')
end_time = time.time()
print(f"Optimized time: {end_time - start_time:.4f} seconds")
opt_len = len(m100_opt) + len(m75_opt) + len(m50_opt)

print(f"Original Matches found: 100%={len(m100)}, 75-99%={len(m75)}, 50-74%={len(m50)}")
print(f"Optimized Matches found: 100%={len(m100_opt)}, 75-99%={len(m75_opt)}, 50-74%={len(m50_opt)}")

assert len(m100) == len(m100_opt)
assert len(m75) == len(m75_opt)
assert len(m50) == len(m50_opt)
print("SUCCESS: Results match!")
