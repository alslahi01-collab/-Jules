import pandas as pd
import numpy as np
import os
import sys
from io import BytesIO

# Add root to path
sys.path.append(os.getcwd())

from app import process_comparison as process_comparison_flask
from streamlit_app import process_comparison as process_comparison_streamlit

def generate_fixed_test_data():
    # Use fixed seed for reproducibility
    np.random.seed(42)
    names1 = ["أحمد محمد", "محمد علي", "فاطمة الزهراء", "زيد بن حارثة", "عمر الخطاب"]
    names2 = ["احمد محمد", "محمد على", "فاطمه الزهراء", "زيد بن حارثه", "عثمان عفان"]

    df1 = pd.DataFrame({
        'Name': names1 * 2, # 10 rows
        'ID': range(10)
    })
    df2 = pd.DataFrame({
        'Name': names2 * 2, # 10 rows
        'ID': range(10)
    })

    p1, p2 = "verify1.xlsx", "verify2.xlsx"
    df1.to_excel(p1, index=False)
    df2.to_excel(p2, index=False)
    return p1, p2

def verify():
    p1, p2 = generate_fixed_test_data()

    print("Running Flask comparison...")
    res_flask = process_comparison_flask(p1, p2, "Name", "Name")

    print("Running Streamlit comparison...")
    res_streamlit = process_comparison_streamlit(p1, p2, "Name", "Name")

    def print_stats(res, label):
        print(f"--- {label} ---")
        print(f"100% Matches: {len(res['matches_100'])}")
        print(f"75-99% Matches: {len(res['matches_75_99'])}")
        print(f"50-74% Matches: {len(res['matches_50_74'])}")
        return len(res['matches_100']), len(res['matches_75_99']), len(res['matches_50_74'])

    stats_f = print_stats(res_flask, "Flask")
    stats_s = print_stats(res_streamlit, "Streamlit")

    os.remove(p1)
    os.remove(p2)

    return stats_f, stats_s

if __name__ == "__main__":
    verify()
