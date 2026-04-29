import time
import pandas as pd
import sys
import os

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from app or streamlit_app depending on which one you want to benchmark
# Both now have optimized process_comparison or process_sheets
from app import process_comparison

def run_benchmark():
    file1 = "test_file1.xlsx"
    file2 = "test_file2.xlsx"
    col1 = "Name"
    col2 = "Name"

    if not os.path.exists(file1) or not os.path.exists(file2):
        print("Test files not found. Run generate_test_data.py first.")
        return

    start_time = time.time()
    results = process_comparison(file1, file2, col1, col2)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Comparison took {duration:.4f} seconds")
    print(f"Matches 100%: {len(results['matches_100'])}")
    print(f"Matches 75-99%: {len(results['matches_75_99'])}")
    print(f"Matches 50-74%: {len(results['matches_50_74'])}")

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    run_benchmark()
