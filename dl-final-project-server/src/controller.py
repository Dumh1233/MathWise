from flask import Flask, request, jsonify, send_from_directory
from .model import image_segmentation
from .detect_equation import detect
from .calculator import parser_equation
from .pages_segmentation import split_equations
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath("resources/static/assets/uploads/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_SPLITS_FOLDER = os.path.abspath(
    "resources/static/assets/uploads_splits/")
app.config['UPLOAD_SPLITS_FOLDER'] = UPLOAD_SPLITS_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
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

    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], file.filename)):
        return jsonify({'message': 'File name already exists, please choose a different file name'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        for file in split_equations(filename):
            image_segmentation(file)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif, doc, docx, xls, xlsx'}), 400


@app.route('/api/answer', methods=['GET'])
def getAnswer():
    equation = detect()
    equationAnswer = parser_equation(equation)
    studentAnswer = equation.split("=")[1]
    if equationAnswer == studentAnswer:
        # return jsonify({'message': 'Correct:  student: ${studentAnswer} , model: ${equationAnswer}'}), 200
        return jsonify({'message': 'Correct'}), 200
    else:
        # return jsonify({'message': 'Wrong:    student: ${studentAnswer} , model: ${equationAnswer}'}), 200
        return jsonify({'message': 'Wrong'}), 200


@app.route('/api/files', methods=['GET'])
def getListFiles():
    try:
        fileInfos = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path) and allowed_file(filename):
                filenameNoExtensions = filename.partition('.')
                filenameNoExtensions = filenameNoExtensions[0]
                segmented_pages_url = os.path.join(
                    app.config['UPLOAD_SPLITS_FOLDER'], filenameNoExtensions)
                segmentedPages = []
                for path in os.listdir(segmented_pages_url):
                    # check if current path is a file
                    if os.path.isdir(os.path.join(segmented_pages_url, path)):
                        segmentedPages.append("http://localhost:5000/getSegmentedPage/" +
                                              filenameNoExtensions + "/" + path)
                fileInfos.append({
                    "name": filename,
                    "url": BASE_URL + filename,
                    "segmentedPages": segmentedPages
                })
        return jsonify(fileInfos), 200
    except Exception as e:
        return jsonify({'message': 'Unable to scan files!', 'error': str(e)}), 500


@app.route('/api/files/<string:filename>', methods=['GET'])
def download(filename):
    try:
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=filename, as_attachment=True)
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


@app.route('/api/getSegmentedPage/<string:filename>/<string:page>', methods=['GET'])
def getSegmentedPage(filename, page):
    try:
        filename = filename.partition('.')
        filename = filename[0]
        return send_from_directory(directory=app.config['UPLOAD_SPLITS_FOLDER'] + "/" + filename + "/" + page + "/equations", path=page + ".jpg", as_attachment=True)
    except Exception as e:
        print("exception : " + str(e))
        print(app.config['UPLOAD_SPLITS_FOLDER'] +
              "/" + filename + "/page_" + page + "/equations")
        return jsonify({'message': 'Could not download the file. ' + str(e)}), 500
