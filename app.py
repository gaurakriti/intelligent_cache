from flask import Flask, request, jsonify
import pandas as pd
import os
from preprocess import preprocess_text
from model import filter_texts
from cache import get_cache, set_cache

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    print("Received request to upload file")
    print("Files:", request.files)
    print("Form:", request.form)

    user_id = request.headers.get('user-id')
    keyword = request.form.get('keyword', '')
    threshold = float(request.form.get('threshold', 0.3))
    file = request.files.get('file')

    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    print(f"File saved to {path}")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(path)
        if 'text' not in df.columns:
            return jsonify({'error': 'CSV must have "text" column'}), 400
        texts = df['text'].tolist()
    elif ext == '.txt':
        with open(path, encoding='utf-8') as f:
            texts = [line.strip() for line in f if line.strip()]
        if not texts:
            return jsonify({'error': 'TXT file is empty'}), 400
    else:
        return jsonify({'error': 'Unsupported file type'}), 400

    cache_key = f"user:{user_id}:{keyword}:{threshold}:{file.filename}"
    cached = get_cache(cache_key)
    if cached:
        return jsonify({'cached': True, 'data': cached})

    processed = [preprocess_text(t) for t in texts]
    filtered = filter_texts(processed, keyword, threshold)
    
    print("Processed texts:", processed)
    print("Filtered result:", filtered)

    set_cache(cache_key, filtered)
    # Optionally, save filtered results to a file or database here if needed
    return jsonify({'cached': False, 'data': filtered})

if __name__ == '__main__':
    app.run(debug=True)
