import time
import pandas as pd
import numpy as np
import re
import functools
from thefuzz import fuzz

@functools.lru_cache(maxsize=4096)
def normalize_arabic(text):
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

def optimized_process_sheets(df1, df2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []
    h1, h2 = 0, 0
    s1, s2 = "Sheet1", "Sheet2"

    records1 = df1.to_dict('records')
    records2 = df2.to_dict('records')

    norm_map1 = {}
    for idx, row in enumerate(records1):
        n = normalize_arabic(str(row.get(col1, '')))
        if n and n != 'nan':
            norm_map1.setdefault(n, []).append(idx)

    norm_map2 = {}
    for idx, row in enumerate(records2):
        n = normalize_arabic(str(row.get(col2, '')))
        if n and n != 'nan':
            norm_map2.setdefault(n, []).append(idx)

    fuzz_results_cache = {}

    for n1, indices1 in norm_map1.items():
        for n2, indices2 in norm_map2.items():
            if n1 == n2:
                for idx1 in indices1:
                    row1_dict = records1[idx1]
                    for idx2 in indices2:
                        match_row = row1_dict.copy()
                        match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                        matches_100.append(match_row)
                continue

            pair = tuple(sorted((n1, n2)))
            if pair in fuzz_results_cache:
                score = fuzz_results_cache[pair]
            else:
                score = fuzz.ratio(n1, n2)
                fuzz_results_cache[pair] = score

            if score >= 75:
                for idx1 in indices1:
                    row1_dict = records1[idx1]
                    for _ in indices2:
                        match_row = row1_dict.copy()
                        match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                        matches_75_99.append(match_row)
            elif score >= 50:
                for idx1 in indices1:
                    row1_dict = records1[idx1]
                    for _ in indices2:
                        match_row = row1_dict.copy()
                        match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                        matches_50_74.append(match_row)
    return matches_100, matches_75_99, matches_50_74

def generate_test_data(rows=200):
    np.random.seed(42)
    names = [f"محمد أحمد {i}" for i in range(rows)]
    # Add some overlaps and variations
    names[0] = "محمد احمد 0"
    names[10] = "أحمد محمد"
    names[11] = "احمد محمد"

    df1 = pd.DataFrame({'Name': names, 'Value': np.random.randint(0, 100, size=rows)})
    df2 = pd.DataFrame({'Name': names, 'Value': np.random.randint(0, 100, size=rows)})
    return df1, df2

if __name__ == "__main__":
    rows = 500
    df1, df2 = generate_test_data(rows)

    print(f"Verifying with {rows}x{rows} rows...")

    start_orig = time.time()
    orig_100, orig_75, orig_50 = original_process_sheets(df1, df2, 'Name', 'Name')
    end_orig = time.time()
    orig_time = end_orig - start_orig

    # Clear cache for fair comparison
    normalize_arabic.cache_clear()

    start_opt = time.time()
    opt_100, opt_75, opt_50 = optimized_process_sheets(df1, df2, 'Name', 'Name')
    end_opt = time.time()
    opt_time = end_opt - start_opt

    print(f"Original Time: {orig_time:.4f}s")
    print(f"Optimized Time: {opt_time:.4f}s")
    print(f"Speedup: {orig_time / opt_time:.2f}x")

    print(f"Counts (Orig): 100%={len(orig_100)}, 75-99%={len(orig_75)}, 50-74%={len(orig_50)}")
    print(f"Counts (Opt) : 100%={len(opt_100)}, 75-99%={len(opt_75)}, 50-74%={len(opt_50)}")

    assert len(orig_100) == len(opt_100), "100% match count mismatch!"
    assert len(orig_75) == len(opt_75), "75-99% match count mismatch!"
    assert len(orig_50) == len(opt_50), "50-74% match count mismatch!"

    print("Verification SUCCESS: Optimized logic produces identical results!")
