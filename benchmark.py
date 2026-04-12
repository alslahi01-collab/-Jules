import pandas as pd
import numpy as np
import time
import os
from app import process_comparison as flask_process
from streamlit_app import process_comparison as streamlit_process

def generate_sample_excel(filename, num_rows=100, modified=False):
    if not modified:
        data = {
            'ID': range(num_rows),
            'Name': [f"اسم {i}" for i in range(num_rows)],
            'Value': [i * 10 for i in range(num_rows)]
        }
    else:
        # Rows 0-49: modified
        # Rows 50-99: same
        # Rows 100-149: different
        names = []
        for i in range(num_rows):
            if i < 50:
                names.append(f"اسم {i} معدل")
            elif i < 100:
                names.append(f"اسم {i}")
            else:
                names.append(f"شخص مختلف {i}")
        data = {
            'ID': range(num_rows),
            'Name': names,
            'Value': [i * 10 for i in range(num_rows)]
        }
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename

def benchmark():
    f1 = 'test1.xlsx'
    f2 = 'test2.xlsx'

    num_rows = 150
    generate_sample_excel(f1, num_rows, modified=False)
    generate_sample_excel(f2, num_rows, modified=True)

    print(f"Benchmarking with {num_rows}x{num_rows} rows...")

    # Expected counts from baseline run
    EXPECTED_100 = 50
    EXPECTED_75 = 2460
    EXPECTED_50 = 9031

    print("Running Flask optimization test...")
    start = time.time()
    results_flask = flask_process(f1, f2, 'Name', 'Name')
    flask_duration = time.time() - start

    print("Running Streamlit optimization test...")
    start = time.time()
    results_streamlit = streamlit_process(f1, f2, 'Name', 'Name')
    streamlit_duration = time.time() - start

    c100_f = len(results_flask['matches_100'])
    c75_f = len(results_flask['matches_75_99'])
    c50_f = len(results_flask['matches_50_74'])

    c100_s = len(results_streamlit['matches_100'])
    c75_s = len(results_streamlit['matches_75_99'])
    c50_s = len(results_streamlit['matches_50_74'])

    print(f"Flask: {flask_duration:.4f}s | 100%: {c100_f}, 75-99%: {c75_f}, 50-74%: {c50_f}")
    print(f"Streamlit: {streamlit_duration:.4f}s | 100%: {c100_s}, 75-99%: {c75_s}, 50-74%: {c50_s}")

    # Correctness assertions
    assert c100_f == EXPECTED_100, f"Flask 100% count mismatch: {c100_f} != {EXPECTED_100}"
    assert c75_f == EXPECTED_75, f"Flask 75-99% count mismatch: {c75_f} != {EXPECTED_75}"
    assert c50_f == EXPECTED_50, f"Flask 50-74% count mismatch: {c50_f} != {EXPECTED_50}"

    assert c100_s == EXPECTED_100, f"Streamlit 100% count mismatch: {c100_s} != {EXPECTED_100}"
    assert c75_s == EXPECTED_75, f"Streamlit 75-99% count mismatch: {c75_s} != {EXPECTED_75}"
    assert c50_s == EXPECTED_50, f"Streamlit 50-74% count mismatch: {c50_s} != {EXPECTED_50}"

    print("All correctness checks passed!")

    # Cleanup
    if os.path.exists(f1): os.remove(f1)
    if os.path.exists(f2): os.remove(f2)

if __name__ == "__main__":
    benchmark()
