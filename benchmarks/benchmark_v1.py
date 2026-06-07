import pandas as pd
import numpy as np
import time
import re
from thefuzz import fuzz
import functools

# Cached normalize_arabic
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

def process_sheets_original(df1, df2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []
    h1, h2 = 0, 0
    s1, s2 = "Sheet1", "Sheet2"

    # Original logic (without caching for fair comparison with what's in the files)
    def normalize_no_cache(text):
        if not isinstance(text, str): return str(text)
        text = re.sub(r'[\u064B-\u0652]', '', text)
        text = re.sub(r'[أإآ]', 'ا', text)
        text = re.sub(r'ة', 'ه', text)
        text = re.sub(r'ى', 'ي', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    for idx1, row1 in df1.iterrows():
        val1 = str(row1[col1])
        norm1 = normalize_no_cache(val1)
        if not norm1 or norm1 == 'nan': continue

        for idx2, row2 in df2.iterrows():
            val2 = str(row2[col2])
            norm2 = normalize_no_cache(val2)
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
    return len(matches_100), len(matches_75_99), len(matches_50_74)

def process_sheets_optimized(df1, df2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []
    h1, h2 = 0, 0
    s1, s2 = "Sheet1", "Sheet2"

    # Pre-convert to records for faster access
    records1 = df1.to_dict('records')
    records2 = df2.to_dict('records')

    # Pre-calculate normalized values and group indices
    norm_map1 = {}
    for i, row in enumerate(records1):
        norm = normalize_arabic(str(row[col1]))
        if norm and norm != 'nan':
            norm_map1.setdefault(norm, []).append(i)

    norm_map2 = {}
    for i, row in enumerate(records2):
        norm = normalize_arabic(str(row[col2]))
        if norm and norm != 'nan':
            norm_map2.setdefault(norm, []).append(i)

    fuzz_cache = {}

    for norm1, indices1 in norm_map1.items():
        # 100% Matches
        if norm1 in norm_map2:
            indices2 = norm_map2[norm1]
            for idx1 in indices1:
                for idx2 in indices2:
                    match_row = records1[idx1].copy()
                    match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                    matches_100.append(match_row)

        # Fuzzy Matches
        for norm2, indices2 in norm_map2.items():
            if norm1 == norm2:
                continue

            # Use cached fuzz result if available
            pair = tuple(sorted((norm1, norm2)))
            if pair in fuzz_cache:
                score = fuzz_cache[pair]
            else:
                score = fuzz.ratio(norm1, norm2)
                fuzz_cache[pair] = score

            if score >= 75:
                for idx1 in indices1:
                    for _ in indices2: # Original logic appends row1 for EACH match in df2
                        match_row = records1[idx1].copy()
                        match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                        matches_75_99.append(match_row)
            elif score >= 50:
                for idx1 in indices1:
                    for _ in indices2:
                        match_row = records1[idx1].copy()
                        match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                        matches_50_74.append(match_row)

    return len(matches_100), len(matches_75_99), len(matches_50_74)

# Create synthetic data
np.random.seed(42)
names = ["محمد", "أحمد", "علي", "حسين", "محمود", "إبراهيم", "يوسف", "جاسم", "خالد", "سعيد"]
data1 = {"الاسم": [np.random.choice(names) + " " + np.random.choice(names) for _ in range(300)]}
data2 = {"الاسم": [np.random.choice(names) + " " + np.random.choice(names) for _ in range(300)]}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

print(f"Benchmarking with {len(df1)} rows vs {len(df2)} rows...")

start_orig = time.time()
m100_o, m75_o, m50_o = process_sheets_original(df1, df2, "الاسم", "الاسم")
end_orig = time.time()
orig_time = end_orig - start_orig
print(f"Original took: {orig_time:.2f}s")

start_opt = time.time()
m100_n, m75_n, m50_n = process_sheets_optimized(df1, df2, "الاسم", "الاسم")
end_opt = time.time()
opt_time = end_opt - start_opt
print(f"Optimized took: {opt_time:.2f}s")

print(f"Speedup: {orig_time / opt_time:.2f}x")
print(f"Matches Match: {m100_o == m100_n and m75_o == m75_n and m50_o == m50_n}")
print(f"Original Matches: 100%={m100_o}, 75-99%={m75_o}, 50-74%={m50_o}")
print(f"Optimized Matches: 100%={m100_n}, 75-99%={m75_n}, 50-74%={m50_n}")
