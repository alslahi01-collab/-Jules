import time
import pandas as pd
import numpy as np
from app import process_comparison
import os

def create_dummy_excel(filename, rows=100):
    data = {
        'Name': [f"Name_{i}" for i in range(rows)],
        'Value': np.random.randint(0, 1000, size=rows)
    }
    df = pd.DataFrame(data)
    # Add some variations for fuzzy matching
    df.loc[0:10, 'Name'] = [f"Name_{i}_varied" for i in range(11)]
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    file1 = 'test1.xlsx'
    file2 = 'test2.xlsx'
    create_dummy_excel(file1, 200)
    create_dummy_excel(file2, 200)

    start_time = time.time()
    results = process_comparison(file1, file2, 'Name', 'Name')
    end_time = time.time()

    print(f"Comparison took: {end_time - start_time:.4f} seconds")
    print(f"100% Matches: {len(results['matches_100'])}")
    print(f"75-99% Matches: {len(results['matches_75_99'])}")
    print(f"50-74% Matches: {len(results['matches_50_74'])}")

    os.remove(file1)
    os.remove(file2)
