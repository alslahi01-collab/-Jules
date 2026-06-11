import pandas as pd
import numpy as np
import os
import sys

# Add root to path to import app and streamlit_app
sys.path.append(os.getcwd())

from app import process_comparison as process_comparison_app
from streamlit_app import process_comparison as process_comparison_streamlit

def generate_test_files():
    file1 = 'v_test1.xlsx'
    file2 = 'v_test2.xlsx'

    data1 = {
        'ID': [1, 2, 3, 4, 5],
        'Name': ["محمد", "أحمد", "علي", "فاطمة", "زينب"],
        'City': ["القاهرة", "دبي", "الرياض", "عمان", "بيروت"]
    }
    data2 = {
        'ID': [101, 102, 103, 104, 105],
        'Name': ["محمد", "احمد", "علاء", "فاطمه", "زينب "], # intentional variations
        'City': ["القاهرة", "دبي", "بغداد", "القدس", "بيروت"]
    }

    pd.DataFrame(data1).to_excel(file1, index=False)
    pd.DataFrame(data2).to_excel(file2, index=False)
    return file1, file2

def get_stats(results):
    return {
        '100': len(results['matches_100']),
        '75_99': len(results['matches_75_99']),
        '50_74': len(results['matches_50_74'])
    }

def run_verification():
    file1, file2 = generate_test_files()

    print("Capturing baseline matches...")
    res_app = process_comparison_app(file1, file2, 'Name', 'Name')
    res_st = process_comparison_streamlit(file1, file2, 'Name', 'Name')

    stats_app = get_stats(res_app)
    stats_st = get_stats(res_st)

    print(f"App Baseline: {stats_app}")
    print(f"Streamlit Baseline: {stats_st}")

    # In a real scenario, we would save these and compare later
    # For now, we just print them to confirm we can run it

    if os.path.exists(file1): os.remove(file1)
    if os.path.exists(file2): os.remove(file2)

    return stats_app, stats_st

if __name__ == "__main__":
    run_verification()
