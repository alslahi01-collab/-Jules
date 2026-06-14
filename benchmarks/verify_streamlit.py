import pandas as pd
import numpy as np
import time
import os
import sys
from io import BytesIO

# Add root to path
sys.path.append(os.getcwd())
import streamlit_app

def run_verification():
    df1 = pd.DataFrame({'Name': ['أحمد', 'محمد'], 'ID': [1, 2]})
    df2 = pd.DataFrame({'Name': ['أحمد', 'محمود'], 'ID': [3, 4]})

    f1 = BytesIO()
    df1.to_excel(f1, index=False)
    f1.seek(0)

    f2 = BytesIO()
    df2.to_excel(f2, index=False)
    f2.seek(0)

    print("Running streamlit process_comparison...")
    start_time = time.time()
    results = streamlit_app.process_comparison(f1, f2, 'Name', 'Name')
    end_time = time.time()

    print(f"Time taken: {end_time - start_time:.4f}s")
    print(f"Matches 100: {len(results['matches_100'])}")
    print(f"Matches 75-99: {len(results['matches_75_99'])}")
    print(f"Matches 50-74: {len(results['matches_50_74'])}")

    # Simple assertions
    assert len(results['matches_100']) == 1, f"Expected 1 exact match, got {len(results['matches_100'])}"
    assert len(results['matches_75_99']) >= 1, "Expected at least 1 fuzzy match"
    print("Verification successful!")

if __name__ == "__main__":
    run_verification()
