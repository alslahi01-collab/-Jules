import pandas as pd
import time
import os
import re
from thefuzz import fuzz
import numpy as np

def normalize_arabic(text):
    if not isinstance(text, str):
        return str(text)
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

    h1 = 0
    h2 = 0
    s1 = "Sheet1"
    s2 = "Sheet1"

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

def run_benchmark(n=200):
    print(f"Generating synthetic data with {n} rows...")
    data1 = {'Name': [f"Name {i}" for i in range(n)]}
    data2 = {'Name': [f"Name {i}" for i in range(n)]}
    # Add some variations for fuzzy matching
    for i in range(0, n, 10):
        data2['Name'][i] = data2['Name'][i] + " variant"

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    print("Running original process_sheets...")
    start_time = time.time()
    m100, m75, m50 = process_sheets_original(df1, df2, 'Name', 'Name')
    end_time = time.time()

    duration = end_time - start_time
    print(f"Original took: {duration:.4f} seconds")
    print(f"Matches: 100%={m100}, 75-99%={m75}, 50-74%={m50}")

if __name__ == "__main__":
    run_benchmark(300)
