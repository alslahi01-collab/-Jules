import streamlit as st
import pandas as pd
import re
import functools
from thefuzz import fuzz
from io import BytesIO

@functools.lru_cache(maxsize=4096)
def normalize_arabic(text):
    if not isinstance(text, str):
        return str(text)
    # Remove diacritics
    text = re.sub(r'[\u064B-\u0652]', '', text)
    # Unify Alef
    text = re.sub(r'[أإآ]', 'ا', text)
    # Unify Teh Marbuta and Heh
    text = re.sub(r'ة', 'ه', text)
    # Unify Yeh
    text = re.sub(r'ى', 'ي', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def detect_header_row(df_raw):
    max_non_null = 0
    header_idx = 0
    for i in range(min(len(df_raw), 10)):
        non_null_count = df_raw.iloc[i].count()
        if non_null_count > max_non_null:
            max_non_null = non_null_count
            header_idx = i
    return header_idx

def extract_metadata(uploaded_file):
    xls = pd.ExcelFile(uploaded_file)
    all_columns = set()
    for sheet_name in xls.sheet_names:
        df_raw = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        if df_raw.empty: continue
        h = detect_header_row(df_raw)
        df = pd.read_excel(xls, sheet_name=sheet_name, header=h)
        for col in df.columns:
            all_columns.add(str(col).strip())
    return sorted(list(all_columns))

def process_comparison(file1, file2, col1, col2):
    xls1 = pd.ExcelFile(file1)
    xls2 = pd.ExcelFile(file2)

    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []

    sheets1 = xls1.sheet_names
    sheets2 = xls2.sheet_names

    # Pre-process all sheets in file2 to avoid redundant I/O and processing
    processed_sheets2 = []
    for s2 in sheets2:
        df2_raw = pd.read_excel(xls2, sheet_name=s2, header=None)
        if df2_raw.empty: continue
        h2 = detect_header_row(df2_raw)
        df2 = pd.read_excel(xls2, sheet_name=s2, header=h2)
        df2.columns = df2.columns.astype(str).str.strip()
        if col2 not in df2.columns: continue

        records2 = df2.to_dict('records')
        norm2_map = {}
        for i2, rec2 in enumerate(records2):
            n2 = normalize_arabic(str(rec2.get(col2, '')))
            if n2 and n2 != 'nan':
                norm2_map.setdefault(n2, []).append(i2)

        processed_sheets2.append({
            'name': s2,
            'header_idx': h2,
            'records': records2,
            'norm_map': norm2_map,
            'unique_norms': list(norm2_map.keys())
        })

    fuzz_results_cache = {}

    for s1 in sheets1:
        df1_raw = pd.read_excel(xls1, sheet_name=s1, header=None)
        if df1_raw.empty: continue
        h1 = detect_header_row(df1_raw)
        df1 = pd.read_excel(xls1, sheet_name=s1, header=h1)
        df1.columns = df1.columns.astype(str).str.strip()

        if col1 not in df1.columns: continue

        records1 = df1.to_dict('records')

        for ps2 in processed_sheets2:
            s2 = ps2['name']
            h2 = ps2['header_idx']
            records2 = ps2['records']
            norm2_map = ps2['norm_map']
            unique_norms2 = ps2['unique_norms']

            for i1, rec1 in enumerate(records1):
                val1 = str(rec1.get(col1, ''))
                norm1 = normalize_arabic(val1)
                if not norm1 or norm1 == 'nan': continue

                # 1. Exact matches
                if norm1 in norm2_map:
                    for i2 in norm2_map[norm1]:
                        match_row = rec1.copy()
                        match_row['Similarity Location'] = f"Row {i1+h1+2} in {s1} vs Row {i2+h2+2} in {s2}"
                        match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                        matches_100.append(match_row)

                # 2. Fuzzy matches
                for n2 in unique_norms2:
                    if norm1 == n2: continue

                    pair = tuple(sorted((norm1, n2)))
                    if pair in fuzz_results_cache:
                        score = fuzz_results_cache[pair]
                    else:
                        score = fuzz.ratio(norm1, n2)
                        fuzz_results_cache[pair] = score

                    if score >= 50:
                        for _ in range(len(norm2_map[n2])):
                            match_row = rec1.copy()
                            match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                            match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                            if score >= 75:
                                matches_75_99.append(match_row)
                            else:
                                matches_50_74.append(match_row)

    return {
        'matches_100': pd.DataFrame(matches_100),
        'matches_75_99': pd.DataFrame(matches_75_99),
        'matches_50_74': pd.DataFrame(matches_50_74)
    }

st.set_page_config(page_title="مقارنة ملفات إكسل", layout="centered")

st.title("أداة مقارنة ملفات الإكسل")

col1_ui, col2_ui = st.columns(2)

with col1_ui:
    st.subheader("الملف الأول (الأصل)")
    file1 = st.file_uploader("اختر الملف الأول", type=["xlsx", "xls"], key="file1")
    if file1:
        cols1 = extract_metadata(file1)
        selected_col1 = st.selectbox("اختر عمود المقارنة من الملف الأول", cols1)

with col2_ui:
    st.subheader("الملف الثاني")
    file2 = st.file_uploader("اختر الملف الثاني", type=["xlsx", "xls"], key="file2")
    if file2:
        cols2 = extract_metadata(file2)
        selected_col2 = st.selectbox("اختر عمود المقارنة من الملف الثاني", cols2)

if __name__ == '__main__':
    if file1 and file2 and st.button("بدء المقارنة"):
        with st.spinner("جاري المعالجة..."):
            results = process_comparison(file1, file2, selected_col1, selected_col2)

            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Re-read files for original sheets (simplified for streamlit)
                file1.seek(0)
                xls1 = pd.ExcelFile(file1)
                for s in xls1.sheet_names:
                    df = pd.read_excel(xls1, sheet_name=s)
                    df.to_excel(writer, sheet_name=f"File1_{s}", index=False)

                file2.seek(0)
                xls2 = pd.ExcelFile(file2)
                for s in xls2.sheet_names:
                    df = pd.read_excel(xls2, sheet_name=s)
                    df.to_excel(writer, sheet_name=f"File2_{s}", index=False)

                results['matches_100'].to_excel(writer, sheet_name='المتطابقة_100', index=False)
                results['matches_75_99'].to_excel(writer, sheet_name='متشابهة_75_فوق', index=False)
                results['matches_50_74'].to_excel(writer, sheet_name='متشابهة_50_إلى_74', index=False)

            st.success("تمت المقارنة بنجاح!")
        st.download_button(
            label="تحميل ملف النتائج",
            data=output.getvalue(),
            file_name="comparison_result.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
