import time
import pandas as pd
import numpy as np
import os
import sys

# Mocking parts of the app for benchmarking
import re
from thefuzz import fuzz

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
    s1, s2 = "Sheet1", "Sheet1"

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
                match_row['Similarity Location'] = f"Score: {score}%"
                matches_75_99.append(match_row)
            elif score >= 50:
                match_row = row1.to_dict()
                match_row['Similarity Location'] = f"Score: {score}%"
                matches_50_74.append(match_row)
    return len(matches_100), len(matches_75_99), len(matches_50_74)

def generate_test_data(rows=100):
    names = [f"محمد أحمد {i}" for i in range(rows)]
    # Add some duplicates and slight variations
    names[0] = "محمد احمد 0" # Normalization should catch this
    names[10] = "أحمد محمد"
    names[11] = "احمد محمد"

    df1 = pd.DataFrame({'Name': names, 'Value': np.random.randint(0, 100, size=rows)})
    df2 = pd.DataFrame({'Name': names, 'Value': np.random.randint(0, 100, size=rows)})
    return df1, df2

if __name__ == "__main__":
    rows = 200 # Small number for baseline as O(N^2) is slow
    df1, df2 = generate_test_data(rows)

    print(f"Benchmarking with {rows} rows...")
    start_time = time.time()
    m100, m75, m50 = original_process_sheets(df1, df2, 'Name', 'Name')
    end_time = time.time()

    print(f"Original took: {end_time - start_time:.4f} seconds")
    print(f"Matches found: 100%={m100}, 75-99%={m75}, 50-74%={m50}")
