import os
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import uuid
import re
from thefuzz import fuzz
from io import BytesIO
from functools import lru_cache

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}{ext}")
        file.save(filepath)
        
        try:
            metadata = extract_metadata(filepath)
            return jsonify({
                'file_id': file_id,
                'filename': filename,
                'sheets': metadata['sheets'],
                'columns': metadata['columns']
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/compare', methods=['POST'])
def compare_files():
    file1_id = request.form.get('file1_id')
    file2_id = request.form.get('file2_id')
    col1 = request.form.get('col1')
    col2 = request.form.get('col2')

    if not all([file1_id, file2_id, col1, col2]):
        return jsonify({'error': 'Missing parameters'}), 400

    filepath1 = find_file_by_id(file1_id)
    filepath2 = find_file_by_id(file2_id)

    if not filepath1 or not filepath2:
        return jsonify({'error': 'Files not found'}), 404

    try:
        results = process_comparison(filepath1, filepath2, col1, col2)
        
        output_id = str(uuid.uuid4())
        output_filename = f"comparison_result_{output_id}.xlsx"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Write original sheets
            xls1 = pd.ExcelFile(filepath1)
            for sheet_name in xls1.sheet_names:
                df_raw = pd.read_excel(xls1, sheet_name=sheet_name, header=None)
                h = detect_header_row(df_raw)
                df = pd.read_excel(xls1, sheet_name=sheet_name, header=h)
                df.to_excel(writer, sheet_name=f"File1_{sheet_name}", index=False)
            
            xls2 = pd.ExcelFile(filepath2)
            for sheet_name in xls2.sheet_names:
                df_raw = pd.read_excel(xls2, sheet_name=sheet_name, header=None)
                h = detect_header_row(df_raw)
                df = pd.read_excel(xls2, sheet_name=sheet_name, header=h)
                df.to_excel(writer, sheet_name=f"File2_{sheet_name}", index=False)
            
            # Write match results
            results['matches_100'].to_excel(writer, sheet_name='المتطابقة_100', index=False)
            results['matches_75_99'].to_excel(writer, sheet_name='متشابهة_75_فوق', index=False)
            results['matches_50_74'].to_excel(writer, sheet_name='متشابهة_50_إلى_74', index=False)

        return jsonify({'download_url': f'/download/{output_filename}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_result(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found", 404

def find_file_by_id(file_id):
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if f.startswith(file_id):
            return os.path.join(app.config['UPLOAD_FOLDER'], f)
    return None

def detect_header_row(df_raw):
    """
    Tries to find the row that most likely contains headers.
    """
    max_non_null = 0
    header_idx = 0
    for i in range(min(len(df_raw), 10)):  # Check first 10 rows
        non_null_count = df_raw.iloc[i].count()
        if non_null_count > max_non_null:
            max_non_null = non_null_count
            header_idx = i
    return header_idx

@lru_cache(maxsize=4096)
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

def extract_metadata(filepath):
    xls = pd.ExcelFile(filepath)
    sheets_metadata = []
    all_columns = set()
    
    for sheet_name in xls.sheet_names:
        df_raw = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        if df_raw.empty:
            continue
            
        header_idx = detect_header_row(df_raw)
        df = pd.read_excel(xls, sheet_name=sheet_name, header=header_idx)
        df.columns = df.columns.astype(str).str.strip()
        
        sheets_metadata.append({
            'name': sheet_name,
            'rows': len(df),
            'cols': len(df.columns)
        })
        for col in df.columns:
            all_columns.add(str(col))
            
    return {
        'sheets': sheets_metadata,
        'columns': sorted(list(all_columns))
    }

def process_comparison(path1, path2, col1, col2):
    xls1 = pd.ExcelFile(path1)
    xls2 = pd.ExcelFile(path2)
    
    matches_100 = []
    matches_75_99 = []
    matches_50_74 = []
    
    sheets1 = xls1.sheet_names
    sheets2 = xls2.sheet_names
    
    if len(sheets1) == 1 and len(sheets2) == 1:
        process_sheets(xls1, sheets1[0], xls2, sheets2[0], col1, col2, matches_100, matches_75_99, matches_50_74)
    else:
        for s1 in sheets1:
            best_s2 = None
            best_score = 0
            for s2 in sheets2:
                if s1 == s2:
                    best_s2 = s2
                    best_score = 100
                    break
                score = fuzz.ratio(s1, s2)
                if score > 70 and score > best_score:
                    best_score = score
                    best_s2 = s2
            
            if not best_s2 or best_score < 100:
                df1_raw_tmp = pd.read_excel(xls1, sheet_name=s1, header=None, nrows=10)
                h1_tmp = detect_header_row(df1_raw_tmp)
                df1_tmp = pd.read_excel(xls1, sheet_name=s1, header=h1_tmp, nrows=1)
                df1_cols = set(df1_tmp.columns.astype(str).str.strip())
                
                for s2 in sheets2:
                    df2_raw_tmp = pd.read_excel(xls2, sheet_name=s2, header=None, nrows=10)
                    h2_tmp = detect_header_row(df2_raw_tmp)
                    df2_tmp = pd.read_excel(xls2, sheet_name=s2, header=h2_tmp, nrows=1)
                    df2_cols = set(df2_tmp.columns.astype(str).str.strip())
                    
                    if col1 in df1_cols and col2 in df2_cols:
                        best_s2 = s2
                        break
            
            if best_s2:
                process_sheets(xls1, s1, xls2, best_s2, col1, col2, matches_100, matches_75_99, matches_50_74)

    return {
        'matches_100': pd.DataFrame(matches_100),
        'matches_75_99': pd.DataFrame(matches_75_99),
        'matches_50_74': pd.DataFrame(matches_50_74)
    }

def process_sheets(xls1, s1, xls2, s2, col1, col2, matches_100, matches_75_99, matches_50_74):
    # Read first 10 rows to detect header without loading full sheet twice
    df1_raw_preview = pd.read_excel(xls1, sheet_name=s1, header=None, nrows=10)
    h1 = detect_header_row(df1_raw_preview)
    df1 = pd.read_excel(xls1, sheet_name=s1, header=h1)
    df1.columns = df1.columns.astype(str).str.strip()
    
    df2_raw_preview = pd.read_excel(xls2, sheet_name=s2, header=None, nrows=10)
    h2 = detect_header_row(df2_raw_preview)
    df2 = pd.read_excel(xls2, sheet_name=s2, header=h2)
    df2.columns = df2.columns.astype(str).str.strip()
    
    if col1 in df1.columns and col2 in df2.columns:
        # Pre-convert to records for faster access
        records1 = df1.to_dict('records')
        records2 = df2.to_dict('records')

        # Group indices by unique normalized values
        norm_map1 = {}
        for idx, row in enumerate(records1):
            norm = normalize_arabic(str(row[col1]))
            if norm and norm != 'nan':
                norm_map1.setdefault(norm, []).append(idx)
                
        norm_map2 = {}
        for idx, row in enumerate(records2):
            norm = normalize_arabic(str(row[col2]))
            if norm and norm != 'nan':
                norm_map2.setdefault(norm, []).append(idx)

        fuzz_results_cache = {}

        for n1, indices1 in norm_map1.items():
            for n2, indices2 in norm_map2.items():
                if n1 == n2:
                    for idx1 in indices1:
                        for idx2 in indices2:
                            match_row = records1[idx1].copy()
                            match_row['Similarity Location'] = f"Row {idx1+h1+2} in {s1} vs Row {idx2+h2+2} in {s2}"
                            match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                            matches_100.append(match_row)
                else:
                    # Cache fuzzy score for unique pairs (fuzz.ratio is symmetric)
                    pair = tuple(sorted((n1, n2)))
                    if pair in fuzz_results_cache:
                        score = fuzz_results_cache[pair]
                    else:
                        score = fuzz.ratio(n1, n2)
                        fuzz_results_cache[pair] = score

                    if score >= 75:
                        for idx1 in indices1:
                            for idx2 in indices2:
                                match_row = records1[idx1].copy()
                                match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                                match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                                matches_75_99.append(match_row)
                    elif score >= 50:
                        for idx1 in indices1:
                            for idx2 in indices2:
                                match_row = records1[idx1].copy()
                                match_row['Similarity Location'] = f"Score: {score}%, {col1} vs {col2}"
                                match_row['Source Metadata'] = f"File1: {s1}, File2: {s2}"
                                matches_50_74.append(match_row)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Disable debug and reloader to avoid signal issues on some platforms (like Streamlit or certain containers)
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=port)
