from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
import pandas as pd
import os
from utils import analyze_dataset

app = Flask(__name__)
CORS(app)
Swagger(app)  # Enable Swagger UI

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_csv():
    """
    Upload a CSV or Excel file and get dashboard recommendations
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The CSV or Excel file to upload
    responses:
      200:
        description: Recommendations based on dataset
        schema:
          type: object
          properties:
            headers:
              type: array
              items:
                type: string
            recommendations:
              type: object
    """
    file = request.files['file']
    filename = file.filename.lower()

    if not (filename.endswith('.csv') or filename.endswith('.xlsx') or filename.endswith('.xls')):
        return jsonify({'error': 'Unsupported file format. Upload CSV or Excel files only.'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Load based on file extension
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filepath, engine='openpyxl')
        elif filename.endswith('.xls'):
            df = pd.read_excel(filepath, engine='xlrd')
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
    except Exception as e:
        return jsonify({'error': f'Error reading file: {str(e)}'}), 500

    headers = list(df.columns)

    recommendations = analyze_dataset(headers)

    return jsonify({
        'headers': headers,
        'recommendations': recommendations
    })


if __name__ == '__main__':
    app.run(debug=True)
