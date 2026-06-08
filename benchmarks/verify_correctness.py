import pandas as pd
import sys
import os
from thefuzz import fuzz
from io import BytesIO

sys.path.append(os.getcwd())
import app
import streamlit_app

def create_complex_test_excel():
    data = {
        'Name': ['Ahmed', 'Mohamed', 'Fatima', 'Ahmed', 'Zainab', 'Ali', 'Ali'],
        'Value': [1, 2, 3, 4, 5, 6, 7]
    }
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output

def create_target_excel():
    data = {
        'Name': ['Ahmed', 'Muhammad', 'Fatma', 'Ali', 'Zeynab'],
        'Extra': ['A', 'B', 'C', 'D', 'E']
    }
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output

def verify():
    f1 = create_complex_test_excel()
    f2 = create_target_excel()

    with open('c1.xlsx', 'wb') as f: f.write(f1.getbuffer())
    with open('c2.xlsx', 'wb') as f: f.write(f2.getbuffer())

    results = app.process_comparison('c1.xlsx', 'c2.xlsx', 'Name', 'Name')

    # Ahmed (Row 2, 4) matches Ahmed (Row 2) in f2 -> 2 matches in 100%
    # Ali (Row 6, 7) matches Ali (Row 4) in f2 -> 2 matches in 100%
    # Total 100% matches = 4

    print(f"Correctness Check:")
    print(f"  App 100% matches: {len(results['matches_100'])}")
    assert len(results['matches_100']) == 4

    f1.seek(0)
    f2.seek(0)
    results_st = streamlit_app.process_comparison(f1, f2, 'Name', 'Name')
    print(f"  Streamlit 100% matches: {len(results_st['matches_100'])}")
    assert len(results_st['matches_100']) == 4

    # Check fuzzy matches
    # Mohamed vs Muhammad
    # Fatima vs Fatma
    # Zainab vs Zeynab
    # etc.
    print(f"  App fuzzy matches: {len(results['matches_75_99']) + len(results['matches_50_74'])}")
    print(f"  Streamlit fuzzy matches: {len(results_st['matches_75_99']) + len(results_st['matches_50_74'])}")
    assert len(results['matches_75_99']) == len(results_st['matches_75_99'])

    os.remove('c1.xlsx')
    os.remove('c2.xlsx')
    print("Correctness verified!")

if __name__ == '__main__':
    verify()
