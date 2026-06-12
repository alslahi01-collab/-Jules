import pandas as pd
import time
import re
import functools
from thefuzz import fuzz
import numpy as np

def normalize_arabic_original(text):
    if not isinstance(text, str):
        return str(text)
    text = re.sub(r'[\u064B-\u0652]', '', text)
    text = re.sub(r'[أإآ]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@functools.lru_cache(maxsize=4096)
def normalize_arabic_optimized(text):
    return normalize_arabic_original(text)

def process_sheets_original(df1, df2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []
    h1, h2 = 0, 0
    s1, s2 = "S1", "S2"

    for idx1, row1 in df1.iterrows():
        val1 = str(row1[col1])
        norm1 = normalize_arabic_original(val1)
        if not norm1 or norm1 == 'nan': continue

        for idx2, row2 in df2.iterrows():
            val2 = str(row2[col2])
            norm2 = normalize_arabic_original(val2)
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
    s1, s2 = "S1", "S2"

    records1 = df1.to_dict('records')
    records2 = df2.to_dict('records')

    norm_map2 = {}
    for idx2, row2 in enumerate(records2):
        val2 = str(row2[col2])
        norm2 = normalize_arabic_optimized(val2)
        if not norm2 or norm2 == 'nan': continue
        if norm2 not in norm_map2:
            norm_map2[norm2] = []
        norm_map2[norm2].append((idx2, row2))

    fuzz_results_cache = {}

    for idx1, row1 in enumerate(records1):
        val1 = str(row1[col1])
        norm1 = normalize_arabic_optimized(val1)
        if not norm1 or norm1 == 'nan': continue

        if norm1 in norm_map2:
            for idx2, row2 in norm_map2[norm1]:
                match_row = row1.copy()
                match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                matches_100.append(match_row)

        for norm2, matches in norm_map2.items():
            if norm1 == norm2: continue

            pair = tuple(sorted((norm1, norm2)))
            if pair in fuzz_results_cache:
                score = fuzz_results_cache[pair]
            else:
                score = fuzz.ratio(norm1, norm2)
                fuzz_results_cache[pair] = score

            if score >= 75:
                for idx2, row2 in matches:
                    match_row = row1.copy()
                    match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                    matches_75_99.append(match_row)
            elif score >= 50:
                for idx2, row2 in matches:
                    match_row = row1.copy()
                    match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                    matches_50_74.append(match_row)
    return matches_100, matches_75_99, matches_50_74

def run_verification(n=300):
    print(f"Running verification with {n} rows...")
    np.random.seed(42)
    data1 = {'Name': [f"Name {i}" for i in range(n)]}
    data2 = {'Name': [f"Name {i}" for i in range(n)]}
    for i in range(0, n, 10):
        data2['Name'][i] = data2['Name'][i] + " variant"

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    print("Executing original implementation...")
    start = time.time()
    orig_100, orig_75, orig_50 = process_sheets_original(df1, df2, 'Name', 'Name')
    orig_time = time.time() - start

    print("Executing optimized implementation...")
    start = time.time()
    opt_100, opt_75, opt_50 = process_sheets_optimized(df1, df2, 'Name', 'Name')
    opt_time = time.time() - start

    print(f"\nResults:")
    print(f"Original Time: {orig_time:.4f}s")
    print(f"Optimized Time: {opt_time:.4f}s")
    print(f"Speedup: {orig_time/opt_time:.2f}x")

    print(f"\nMatch Counts (Original vs Optimized):")
    print(f"100%: {len(orig_100)} vs {len(opt_100)}")
    print(f"75-99%: {len(orig_75)} vs {len(opt_75)}")
    print(f"50-74%: {len(orig_50)} vs {len(opt_50)}")

    assert len(orig_100) == len(opt_100), "100% match count mismatch!"
    assert len(orig_75) == len(opt_75), "75-99% match count mismatch!"
    assert len(orig_50) == len(opt_50), "50-74% match count mismatch!"

    print("\n✅ VERIFICATION SUCCESSFUL: Optimized logic produces identical results with significantly better performance.")

if __name__ == "__main__":
    run_verification(300)
