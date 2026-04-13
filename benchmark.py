import pandas as pd
import time
import os
from app import process_comparison

def create_dummy_excel(filename, col_name, data):
    df = pd.DataFrame({col_name: data})
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    file1 = "test_file1.xlsx"
    file2 = "test_file2.xlsx"
    col1 = "Name"
    col2 = "Name"

    # Create dummy data
    data1 = ["أحمد", "محمد", "علي", "عمر", "عثمان"] * 30  # 150 rows
    data2 = ["احمد", "محمود", "علي", "عمرو", "عثمان"] * 30 # 150 rows

    create_dummy_excel(file1, col1, data1)
    create_dummy_excel(file2, col2, data2)

    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    start_time = time.time()
    results = process_comparison(file1, file2, col1, col2)
    end_time = time.time()

    print(f"Comparison took: {end_time - start_time:.4f} seconds")
    print(f"Matches 100%: {len(results['matches_100'])}")
    print(f"Matches 75-99%: {len(results['matches_75_99'])}")
    print(f"Matches 50-74%: {len(results['matches_50_74'])}")

    # Cleanup
    os.remove(file1)
    os.remove(file2)
