import pandas as pd
import time
import os
import sys
import functools
from thefuzz import fuzz

# Add root to sys.path to import from app or streamlit_app
sys.path.append(os.getcwd())

from app import normalize_arabic

@functools.lru_cache(maxsize=4096)
def normalize_arabic_cached(text):
    return normalize_arabic(text)

def process_sheets_original(df1, h1, s1, df2, h2, s2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []

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

def process_sheets_optimized(df1, h1, s1, df2, h2, s2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []

    norm_map1 = {}
    for idx, val in df1[col1].items():
        norm = normalize_arabic_cached(str(val))
        if norm and norm != 'nan':
            norm_map1.setdefault(norm, []).append(idx)

    norm_map2 = {}
    for idx, val in df2[col2].items():
        norm = normalize_arabic_cached(str(val))
        if norm and norm != 'nan':
            norm_map2.setdefault(norm, []).append(idx)

    records1 = df1.to_dict('records')

    unique_norms1 = list(norm_map1.keys())
    unique_norms2 = list(norm_map2.keys())

    for n1 in unique_norms1:
        indices1 = norm_map1[n1]
        for n2 in unique_norms2:
            indices2 = norm_map2[n2]

            if n1 == n2:
                for idx1 in indices1:
                    row_dict = records1[idx1]
                    for idx2 in indices2:
                        match_row = row_dict.copy()
                        match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                        match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                        matches_100.append(match_row)
                continue

            score = fuzz.ratio(n1, n2)
            if score >= 50:
                for idx1 in indices1:
                    row_dict = records1[idx1]
                    for idx2 in indices2:
                        match_row = row_dict.copy()
                        match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                        match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                        if score >= 75:
                            matches_75_99.append(match_row)
                        else:
                            matches_50_74.append(match_row)

    return len(matches_100), len(matches_75_99), len(matches_50_74)

# Create synthetic data
n_rows = 300
data1 = {'Name': [f'Person {i}' for i in range(n_rows)], 'Value': range(n_rows)}
data2 = {'Name': [f'Person {i}' if i % 2 == 0 else f'Persun {i}' for i in range(n_rows)], 'Other': range(n_rows)}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

print(f"Benchmarking {n_rows}x{n_rows} rows...")

start_time = time.time()
m100, m75, m50 = process_sheets_original(df1, 0, 'S1', df2, 0, 'S2', 'Name', 'Name')
end_time = time.time()
orig_time = end_time - start_time
print(f"Original time: {orig_time:.4f} seconds")
print(f"Matches: 100%={m100}, 75-99%={m75}, 50-74%={m50}")

start_time = time.time()
m100_opt, m75_opt, m50_opt = process_sheets_optimized(df1, 0, 'S1', df2, 0, 'S2', 'Name', 'Name')
end_time = time.time()
opt_time = end_time - start_time
print(f"Optimized time: {opt_time:.4f} seconds")
print(f"Matches: 100%={m100_opt}, 75-99%={m75_opt}, 50-74%={m50_opt}")

print(f"Speedup: {orig_time / opt_time:.2f}x")
assert (m100, m75, m50) == (m100_opt, m75_opt, m50_opt), "Results mismatch!"
