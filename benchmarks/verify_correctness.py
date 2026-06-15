import pandas as pd
import numpy as np
from app import process_comparison as process_comparison_flask
from streamlit_app import process_comparison as process_comparison_streamlit
import os
import re
from thefuzz import fuzz

def normalize_arabic_orig(text):
    if not isinstance(text, str):
        return str(text)
    text = re.sub(r'[\u064B-\u0652]', '', text)
    text = re.sub(r'[أإآ]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_sheets_orig(df1, h1, s1, df2, h2, s2, col1, col2):
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []

    for idx1, row1 in df1.iterrows():
        val1 = str(row1[col1])
        norm1 = normalize_arabic_orig(val1)
        if not norm1 or norm1 == 'nan': continue

        for idx2, row2 in df2.iterrows():
            val2 = str(row2[col2])
            norm2 = normalize_arabic_orig(val2)
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

def verify_correctness():
    file1 = "verify_file1.xlsx"
    file2 = "verify_file2.xlsx"
    num_rows = 50
    col1 = "name"
    col2 = "name"

    # Seed for reproducibility
    np.random.seed(42)

    # Generate data with some duplicates and some fuzzy matches
    names = ["محمد", "أحمد", "علي", "فاطمة", "زينب", "عمر", "خالد", "ليلى"]
    data1 = {col1: np.random.choice(names, num_rows)}
    df1 = pd.DataFrame(data1)
    df1.to_excel(file1, index=False)

    # Slight variations for file2
    names2 = ["محمد", "احمد", "على", "فاطمه", "زينب", "عمر", "خالد", "ليلي", "سارة"]
    data2 = {col2: np.random.choice(names2, num_rows)}
    df2 = pd.DataFrame(data2)
    df2.to_excel(file2, index=False)

    print("Verifying correctness...")

    # Original logic counts
    df1_loaded = pd.read_excel(file1)
    df2_loaded = pd.read_excel(file2)
    orig_100, orig_75, orig_50 = process_sheets_orig(df1_loaded, 0, "Sheet1", df2_loaded, 0, "Sheet1", col1, col2)

    print(f"Original logic: 100% matches: {orig_100}, 75-99%: {orig_75}, 50-74%: {orig_50}")

    # Flask optimized logic counts
    results_flask = process_comparison_flask(file1, file2, col1, col2)
    flask_100 = len(results_flask['matches_100'])
    flask_75 = len(results_flask['matches_75_99'])
    flask_50 = len(results_flask['matches_50_74'])
    print(f"Flask optimized: 100% matches: {flask_100}, 75-99%: {flask_75}, 50-74%: {flask_50}")

    # Streamlit optimized logic counts
    results_streamlit = process_comparison_streamlit(file1, file2, col1, col2)
    streamlit_100 = len(results_streamlit['matches_100'])
    streamlit_75 = len(results_streamlit['matches_75_99'])
    streamlit_50 = len(results_streamlit['matches_50_74'])
    print(f"Streamlit optimized: 100% matches: {streamlit_100}, 75-99%: {streamlit_75}, 50-74%: {streamlit_50}")

    assert flask_100 == orig_100, f"Flask 100% mismatch: {flask_100} != {orig_100}"
    assert flask_75 == orig_75, f"Flask 75-99% mismatch: {flask_75} != {orig_75}"
    assert flask_50 == orig_50, f"Flask 50-74% mismatch: {flask_50} != {orig_50}"

    assert streamlit_100 == orig_100, f"Streamlit 100% mismatch: {streamlit_100} != {orig_100}"
    assert streamlit_75 == orig_75, f"Streamlit 75-99% mismatch: {streamlit_75} != {orig_75}"
    assert streamlit_50 == orig_50, f"Streamlit 50-74% mismatch: {streamlit_50} != {orig_50}"

    print("Verification SUCCESSFUL: Optimized logic produces identical results to original logic.")

    os.remove(file1)
    os.remove(file2)

if __name__ == "__main__":
    verify_correctness()
