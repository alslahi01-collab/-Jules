import time
import pandas as pd
import re
from thefuzz import fuzz
import functools

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

def process_sheets_optimized(df1, df2, col1, col2, s1="Sheet1", s2="Sheet2", h1=0, h2=0):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []

    df1_records = df1.to_dict('records')
    df2_records = df2.to_dict('records')

    norm1_list = [normalize_arabic(str(r.get(col1, ""))) for r in df1_records]

    norm2_map = {}
    for i, r in enumerate(df2_records):
        n2 = normalize_arabic(str(r.get(col2, "")))
        if n2 and n2 != 'nan':
            if n2 not in norm2_map:
                norm2_map[n2] = []
            norm2_map[n2].append(i)

    unique_norm2 = list(norm2_map.keys())

    unique_norm1 = {}
    for i, n1 in enumerate(norm1_list):
        if n1 and n1 != 'nan':
            if n1 not in unique_norm1:
                unique_norm1[n1] = []
            unique_norm1[n1].append(i)

    fuzz_results_cache = {}

    for n1, indices1 in unique_norm1.items():
        for n2 in unique_norm2:
            if n1 == n2:
                for idx1 in indices1:
                    r1 = df1_records[idx1]
                    for idx2 in norm2_map[n2]:
                        match_row = r1.copy()
                        match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                        match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                        matches_100.append(match_row)
            else:
                pair = tuple(sorted((n1, n2)))
                if pair in fuzz_results_cache:
                    score = fuzz_results_cache[pair]
                else:
                    score = fuzz.ratio(n1, n2)
                    fuzz_results_cache[pair] = score

                if score >= 50:
                    for idx1 in indices1:
                        r1 = df1_records[idx1]
                        for idx2 in norm2_map[n2]:
                            match_row = r1.copy()
                            match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                            match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                            if score >= 75:
                                matches_75_99.append(match_row)
                            else:
                                matches_50_74.append(match_row)

    return len(matches_100), len(matches_75_99), len(matches_50_74)

df1 = pd.read_excel('benchmark_file1.xlsx')
df2 = pd.read_excel('benchmark_file2.xlsx')

subset_n = 500 # Use full 500 rows for optimized
df1_sub = df1.head(subset_n)
df2_sub = df2.head(subset_n)

print(f"Benchmarking optimized logic with {subset_n}x{subset_n} rows...")
start = time.time()
m100, m75, m50 = process_sheets_optimized(df1_sub, df2_sub, 'Name1', 'Name2')
end = time.time()
print(f"Optimized logic took {end - start:.2f} seconds. Matches: 100%:{m100}, 75-99%:{m75}, 50-74%:{m50}")
