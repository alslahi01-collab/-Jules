import pandas as pd
import time
import re
from thefuzz import fuzz
import functools
import sys
import os

# Add root to sys.path
sys.path.append(os.getcwd())

from app import process_sheets as app_process_sheets
from streamlit_app import process_comparison as st_process_comparison

# Original logic for comparison
def original_normalize_arabic(text):
    if not isinstance(text, str):
        return str(text)
    text = re.sub(r'[\u064B-\u0652]', '', text)
    text = re.sub(r'[أإآ]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def original_process_sheets(df1, df2, col1, col2):
    m100, m75, m50 = [], [], []
    for idx1, row1 in df1.iterrows():
        val1 = str(row1[col1])
        norm1 = original_normalize_arabic(val1)
        if not norm1 or norm1 == 'nan': continue
        for idx2, row2 in df2.iterrows():
            val2 = str(row2[col2])
            norm2 = original_normalize_arabic(val2)
            if not norm2 or norm2 == 'nan': continue
            if norm1 == norm2:
                m100.append(row1.to_dict())
                continue
            score = fuzz.ratio(norm1, norm2)
            if score >= 75: m75.append(row1.to_dict())
            elif score >= 50: m50.append(row1.to_dict())
    return len(m100), len(m75), len(m50)

# Create dummy data
n = 100
data1 = {'Name': ['احمد محمد ' + str(i % 20) for i in range(n)]}
data2 = {'Name': ['أحمد محمد ' + str(i % 20) for i in range(n)]}
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Save to excel files
df1.to_excel('test1.xlsx', index=False)
df2.to_excel('test2.xlsx', index=False)

print(f"Benchmarking with {n}x{n} rows (lots of duplicates)...")

# Benchmark Original
start = time.time()
o100, o75, o50 = original_process_sheets(df1, df2, 'Name', 'Name')
orig_time = time.time() - start
print(f"Original: {orig_time:.4f}s | 100%: {o100}, 75%: {o75}, 50%: {o50}")

# Benchmark app.py logic
matches_100, matches_75, matches_50 = [], [], []
start = time.time()
app_process_sheets('test1.xlsx', 'Sheet1', 'test2.xlsx', 'Sheet1', 'Name', 'Name', matches_100, matches_75, matches_50)
app_time = time.time() - start
print(f"app.py:   {app_time:.4f}s | 100%: {len(matches_100)}, 75%: {len(matches_75)}, 50%: {len(matches_50)}")

# Benchmark streamlit_app.py logic
start = time.time()
st_results = st_process_comparison('test1.xlsx', 'test2.xlsx', 'Name', 'Name')
st_time = time.time() - start
st_m100 = len(st_results['matches_100'])
st_m75 = len(st_results['matches_75_99'])
st_m50 = len(st_results['matches_50_74'])
print(f"streamlit: {st_time:.4f}s | 100%: {st_m100}, 75%: {st_m75}, 50%: {st_m50}")

# Verify correctness
app_ok = (o100 == len(matches_100) and o75 == len(matches_75) and o50 == len(matches_50))
st_ok = (o100 == st_m100 and o75 == st_m75 and o50 == st_m50)

if app_ok and st_ok:
    print("SUCCESS: All results match original implementation!")
    print(f"Speedup (app): {orig_time / app_time:.2f}x")
    print(f"Speedup (st):  {orig_time / st_time:.2f}x")
else:
    print(f"FAILURE! App OK: {app_ok}, Streamlit OK: {st_ok}")

# Cleanup
if os.path.exists('test1.xlsx'): os.remove('test1.xlsx')
if os.path.exists('test2.xlsx'): os.remove('test2.xlsx')
