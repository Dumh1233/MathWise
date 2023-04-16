from flask import Flask, request, jsonify, send_from_directory
from .model import image_segmentation
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath("resources/static/assets/uploads/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
BASE_URL = "http://localhost:5000/files/"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in {
               'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}


@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_segmentation(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif, doc, docx, xls, xlsx'}), 400


@app.route('/api/files', methods=['GET'])
def getListFiles():
    try:
        fileInfos = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path) and allowed_file(filename):
                fileInfos.append({
                    "name": filename,
                    "url": BASE_URL + filename
                })
        return jsonify(fileInfos), 200
    except Exception as e:
        return jsonify({'message': 'Unable to scan files!', 'error': str(e)}), 500


@app.route('/api/files/<string:filename>', methods=['GET'])
def download(filename):
    try:
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=True)
    except Exception as e:
        return jsonify({'message': 'Could not download the file. ' + str(e)}), 500


@app.route('/api/files/<string:filename>', methods=['DELETE'])
def remove(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File is deleted.'}), 200
    except Exception as e:
        return jsonify({'message': 'Could not delete the file. ' + str(e)}), 500


@app.route('/api/files/<string:filename>/sync', methods=['DELETE'])
def removeSync(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File is deleted.'}), 200
    except Exception as e:
        return jsonify({'message': 'Could not delete the file. ' + str(e)}), 500
