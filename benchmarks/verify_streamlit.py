import pandas as pd
import io
import os
import sys

# Add current directory to path so we can import streamlit_app
sys.path.append(os.getcwd())

# We need to mock streamlit because process_comparison is in the same file as UI code
# But since process_comparison doesn't use st.*, we might be able to import it if it's not at top level
# Let's check streamlit_app.py structure
from streamlit_app import process_comparison

def test_process_comparison():
    # Create synthetic excel files in memory
    df1 = pd.DataFrame({'Name': ['محمد', 'احمد', 'محمود'], 'Age': [20, 30, 40]})
    df2 = pd.DataFrame({'Name': ['محمد', 'أحمد', 'على'], 'Score': [100, 90, 80]})

    # Save to bytes
    out1 = io.BytesIO()
    with pd.ExcelWriter(out1, engine='openpyxl') as writer:
        df1.to_excel(writer, sheet_name='Sheet1', index=False)
    out1.seek(0)

    out2 = io.BytesIO()
    with pd.ExcelWriter(out2, engine='openpyxl') as writer:
        df2.to_excel(writer, sheet_name='Sheet2', index=False)
    out2.seek(0)

    results = process_comparison(out1, out2, 'Name', 'Name')

    m100 = results['matches_100']
    m75_99 = results['matches_75_99']
    m50_74 = results['matches_50_74']

    print(f"Matches 100%: {len(m100)}")
    print(f"Matches 75-99%: {len(m75_99)}")
    print(f"Matches 50-74%: {len(m50_74)}")

    assert len(m100) == 2
    # 'محمد' and 'احمد' (normalized)

    print("Streamlit verification successful!")

if __name__ == "__main__":
    try:
        test_process_comparison()
    except Exception as e:
        print(f"Error during verification: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
