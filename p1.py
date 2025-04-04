from flask import Flask, request, jsonify,render_template
import os
import pandas as pd

from show import show_data


uploaded_files = []

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath('uploads')  # Get absolute path

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

csv_filename = ""  # Global variable for file storage

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to save CSV files
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create folder if not exists
@app.route('/')
def home():
    return render_template('index.html') 
    
@app.route('/upload', methods=['POST', 'GET'])
def upload_csv():
    global csv_filename

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Invalid file type. Only CSV files are allowed."}), 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)  # Save file

        csv_filename = filepath         # Save full path
        uploaded_files.append(file.filename)  # Store just the name

        return jsonify({"message": "CSV uploaded successfully", "file_path": filepath}), 200

    return "This is the upload page. Please use a POST request to upload a CSV file."

@app.route("/showdata", methods=["GET"])
def show():
    return show_data()  # Call the separated function

@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({"uploaded_files": files}), 200

if __name__ == '__main__':
    app.run(debug=True)

