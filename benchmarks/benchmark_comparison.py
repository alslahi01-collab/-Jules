import pandas as pd
import time
import re
from thefuzz import fuzz
import functools

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

@functools.lru_cache(maxsize=4096)
def optimized_normalize_arabic(text):
    return normalize_arabic(text)

def optimized_process_sheets(df1, df2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []

    h1, h2 = 0, 0
    s1, s2 = "Sheet1", "Sheet2"

    # Pre-calculate normalized values and group by them
    def get_norm_map(df, col):
        norm_map = {}
        for idx, val in enumerate(df[col]):
            norm = optimized_normalize_arabic(str(val))
            if not norm or norm == 'nan': continue
            if norm not in norm_map:
                norm_map[norm] = []
            norm_map[norm].append(idx)
        return norm_map

    map1 = get_norm_map(df1, col1)
    map2 = get_norm_map(df2, col2)

    fuzz_results_cache = {}

    for norm1, indices1 in map1.items():
        # Exact matches
        if norm1 in map2:
            indices2 = map2[norm1]
            for idx1 in indices1:
                row1 = df1.iloc[idx1]
                for idx2 in indices2:
                    match_row = row1.to_dict()
                    match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                    match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                    matches_100.append(match_row)

        # Fuzzy matches
        for norm2, indices2 in map2.items():
            if norm1 == norm2: continue

            # Use symmetric caching for fuzz results
            pair = tuple(sorted((norm1, norm2)))
            if pair in fuzz_results_cache:
                score = fuzz_results_cache[pair]
            else:
                score = fuzz.ratio(norm1, norm2)
                fuzz_results_cache[pair] = score

            if score >= 75:
                for idx1 in indices1:
                    row1 = df1.iloc[idx1]
                    for idx2 in indices2:
                        match_row = row1.to_dict()
                        match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                        match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                        matches_75_99.append(match_row)
            elif score >= 50:
                for idx1 in indices1:
                    row1 = df1.iloc[idx1]
                    for idx2 in indices2:
                        match_row = row1.to_dict()
                        match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                        match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                        matches_50_74.append(match_row)

    return len(matches_100), len(matches_75_99), len(matches_50_74)

# Create dummy data with some duplicates to test grouping
n = 300
data1 = {'Name': ['احمد محمد ' + str(i % 50) for i in range(n)]}
data2 = {'Name': ['أحمد محمد ' + str(i % 50) for i in range(n)]}
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

print(f"Running benchmark with {n}x{n} rows...")

start_time = time.time()
orig_m100, orig_m75, orig_m50 = original_process_sheets(df1, df2, 'Name', 'Name')
orig_time = time.time() - start_time
print(f"Original Time: {orig_time:.4f} seconds")
print(f"Original Matches: 100%: {orig_m100}, 75-99%: {orig_m75}, 50-74%: {orig_m50}")

start_time = time.time()
opt_m100, opt_m75, opt_m50 = optimized_process_sheets(df1, df2, 'Name', 'Name')
opt_time = time.time() - start_time
print(f"Optimized Time: {opt_time:.4f} seconds")
print(f"Optimized Matches: 100%: {opt_m100}, 75-99%: {opt_m75}, 50-74%: {opt_m50}")

if orig_m100 == opt_m100 and orig_m75 == opt_m75 and orig_m50 == opt_m50:
    print("SUCCESS: Results match!")
    print(f"Speedup: {orig_time / opt_time:.2f}x")
else:
    print("FAILURE: Results do not match!")
