import pandas as pd
import time
import os
import shutil
from io import BytesIO

# Import the optimized functions
from app import process_sheets as app_process_sheets, normalize_arabic as app_normalize_arabic
from streamlit_app import process_comparison as st_process_comparison

def create_mock_excel(data_dict, filename):
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        for sheet_name, data in data_dict.items():
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    return filename

def verify_app_logic():
    print("Verifying app.py process_sheets...")
    # Mock data
    data1 = {'Name': ['محمد', 'احمد', 'علي', 'عمر'], 'ID': [1, 2, 3, 4]}
    data2 = {'الاسم': ['محمّد', 'أحمد', 'عثمان'], 'ID': [10, 20, 30]}

    file1 = create_mock_excel({'Sheet1': data1}, 'test1.xlsx')
    file2 = create_mock_excel({'Sheet1': data2}, 'test2.xlsx')

    xls1 = pd.ExcelFile(file1)
    xls2 = pd.ExcelFile(file2)

    m100, m75, m50 = [], [], []
    app_process_sheets(xls1, 'Sheet1', xls2, 'Sheet1', 'Name', 'الاسم', m100, m75, m50)

    print(f"Matches found: 100%={len(m100)}, 75-99%={len(m75)}, 50-74%={len(m50)}")

    # Check expected matches
    # 'محمد' vs 'محمّد' (normalized to 'محمد') -> 100%
    # 'احمد' vs 'أحمد' (normalized to 'احمد') -> 100%
    assert len(m100) == 2
    print("app.py verification SUCCESS")

    os.remove(file1)
    os.remove(file2)

def verify_st_logic():
    print("\nVerifying streamlit_app.py process_comparison...")
    data1 = {'Name': ['محمد', 'احمد', 'علي'], 'ID': [1, 2, 3]}
    data2 = {'الاسم': ['محمّد', 'أحمد', 'خالد'], 'ID': [10, 20, 30]}

    f1_buf = BytesIO()
    with pd.ExcelWriter(f1_buf, engine='openpyxl') as writer:
        pd.DataFrame(data1).to_excel(writer, index=False)
    f1_buf.seek(0)

    f2_buf = BytesIO()
    with pd.ExcelWriter(f2_buf, engine='openpyxl') as writer:
        pd.DataFrame(data2).to_excel(writer, index=False)
    f2_buf.seek(0)

    results = st_process_comparison(f1_buf, f2_buf, 'Name', 'الاسم')

    m100 = results['matches_100']
    print(f"Matches found: 100%={len(m100)}")
    assert len(m100) == 2
    print("streamlit_app.py verification SUCCESS")

def benchmark_performance():
    print("\nBenchmarking performance...")
    n_rows = 500
    data1 = {'name': [f'اسم {i}' for i in range(n_rows)], 'val': range(n_rows)}
    data2 = {'name': [f'إسم {i}' if i % 10 == 0 else f'مختلف {i}' for i in range(n_rows)], 'val': range(n_rows)}

    f1_path = 'bench1.xlsx'
    f2_path = 'bench2.xlsx'
    create_mock_excel({'Sheet1': data1}, f1_path)
    create_mock_excel({'Sheet1': data2}, f2_path)

    xls1 = pd.ExcelFile(f1_path)
    xls2 = pd.ExcelFile(f2_path)

    start_time = time.time()
    m100, m75, m50 = [], [], []
    app_process_sheets(xls1, 'Sheet1', xls2, 'Sheet1', 'name', 'name', m100, m75, m50)
    end_time = time.time()

    print(f"Optimized app.py time for {n_rows}x{n_rows} rows: {end_time - start_time:.4f} seconds")
    print(f"Total matches: {len(m100) + len(m75) + len(m50)}")

    # Original would be roughly (500*500) iterations * fuzz.ratio time.
    # 250,000 iterations. At ~4 microseconds per ratio, it would take ~1 second just for ratios.
    # But Python overhead makes it much slower. 100x100 took 1s, so 500x500 would take ~25s.

    os.remove(f1_path)
    os.remove(f2_path)

if __name__ == "__main__":
    try:
        verify_app_logic()
        verify_st_logic()
        benchmark_performance()
    except Exception as e:
        print(f"Verification FAILED: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
