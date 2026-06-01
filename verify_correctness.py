import pandas as pd
import numpy as np
from app import process_comparison
import os

def create_test_excel(filename, data_list):
    df = pd.DataFrame({'Name': data_list})
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    file1 = 'v_test1.xlsx'
    file2 = 'v_test2.xlsx'

    # Specific test cases: exact, fuzzy, duplicates, arabic
    data1 = ["أحمد", "محمد", "علي", "علي", "عمر"]
    data2 = ["احمد", "محمود", "عالي", "عمر", "عمر"]

    create_test_excel(file1, data1)
    create_test_excel(file2, data2)

    results = process_comparison(file1, file2, 'Name', 'Name')

    print(f"100% Matches: {len(results['matches_100'])}")
    print(f"75-99% Matches: {len(results['matches_75_99'])}")
    print(f"50-74% Matches: {len(results['matches_50_74'])}")

    # "أحمد" vs "احمد" should be 100% after normalization
    # "عمر" (file1) matches "عمر" (file2) twice -> 2 matches
    # "علي" (file1, twice) matches "عالي" (file2) fuzzy -> 2 matches

    expected_100 = 3 # أحمد-احمد, عمر-عمر(idx3), عمر-عمر(idx4)
    if len(results['matches_100']) == expected_100:
        print("Verification PASSED for 100% matches")
    else:
        print(f"Verification FAILED for 100% matches. Expected {expected_100}, got {len(results['matches_100'])}")

    os.remove(file1)
    os.remove(file2)
