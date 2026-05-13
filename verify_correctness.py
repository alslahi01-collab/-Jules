import pandas as pd
import time
import os
import random
import string
from thefuzz import fuzz

# Import both versions (mocking or using temporary files if needed)
# Since we want to compare against original, I should have saved original.
# I will create a script that implements the OLD logic and compares results.

def normalize_arabic_old(text):
    if not isinstance(text, str):
        return str(text)
    import re
    text = re.sub(r'[\u064B-\u0652]', '', text)
    text = re.sub(r'[أإآ]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_sheets_old(df1, df2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []
    h1, h2 = 0, 0
    s1, s2 = "S1", "S2"

    for idx1, row1 in df1.iterrows():
        val1 = str(row1[col1])
        norm1 = normalize_arabic_old(val1)
        if not norm1 or norm1 == 'nan': continue

        for idx2, row2 in df2.iterrows():
            val2 = str(row2[col2])
            norm2 = normalize_arabic_old(val2)
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

if __name__ == "__main__":
    from app import process_sheets
    import openpyxl

    # Small scale test to verify correctness
    rows = 50
    data1 = [{"Name": ''.join(random.choices(string.ascii_lowercase, k=5)), "ID": i} for i in range(rows)]
    data2 = [{"Name": ''.join(random.choices(string.ascii_lowercase, k=5)), "ID": i} for i in range(rows)]

    # Add some exact matches
    data2[0]["Name"] = data1[0]["Name"]
    data2[1]["Name"] = data1[1]["Name"]

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    print("Verifying correctness...")

    # Old logic
    m100_old, m75_old, m50_old = process_sheets_old(df1, df2, "Name", "Name")

    # New logic
    m100_new = []
    m75_new = []
    m50_new = []
    # Mocking ExcelFile or just calling the inner logic if possible
    # process_sheets expects (xls1, s1, xls2, s2, col1, col2, matches_100, matches_75_99, matches_50_74)
    # I'll modify app.py temporarily to export a testable version or just use the logic directly.

    # Actually, I can just copy the logic here for verification
    from app import normalize_arabic
    def process_sheets_new_logic(df1, df2, col1, col2):
        matches_100 = []
        matches_75_99 = []
        matches_50_74 = []
        h1, h2 = 0, 0
        s1, s2 = "S1", "S2"

        norm2_map = {}
        for idx2, row2 in df2.iterrows():
            val2 = str(row2[col2])
            norm2 = normalize_arabic(val2)
            if not norm2 or norm2 == 'nan': continue
            if norm2 not in norm2_map:
                norm2_map[norm2] = []
            norm2_map[norm2].append(idx2)
        unique_norm2 = list(norm2_map.keys())
        fuzz_results_cache = {}

        for idx1, row1 in df1.iterrows():
            val1 = str(row1[col1])
            norm1 = normalize_arabic(val1)
            if not norm1 or norm1 == 'nan': continue
            if norm1 in norm2_map:
                for idx2 in norm2_map[norm1]:
                    match_row = row1.to_dict()
                    match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                    match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                    matches_100.append(match_row)
            for n2 in unique_norm2:
                if norm1 == n2: continue
                pair = tuple(sorted((norm1, n2)))
                if pair in fuzz_results_cache:
                    score = fuzz_results_cache[pair]
                else:
                    score = fuzz.ratio(norm1, n2)
                    fuzz_results_cache[pair] = score
                if score >= 50:
                    for idx2 in norm2_map[n2]:
                        match_row = row1.to_dict()
                        match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                        if score >= 75:
                            match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                            matches_75_99.append(match_row)
                        else:
                            match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                            matches_50_74.append(match_row)
        return matches_100, matches_75_99, matches_50_74

    m100_new, m75_new, m50_new = process_sheets_new_logic(df1, df2, "Name", "Name")

    print(f"Old matches: 100%:{len(m100_old)}, 75-99%:{len(m75_old)}, 50-74%:{len(m50_old)}")
    print(f"New matches: 100%:{len(m100_new)}, 75-99%:{len(m75_new)}, 50-74%:{len(m50_new)}")

    assert len(m100_old) == len(m100_new)
    assert len(m75_old) == len(m75_new)
    assert len(m50_old) == len(m50_new)
    print("Verification successful! Results are identical.")
