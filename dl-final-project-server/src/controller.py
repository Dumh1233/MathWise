from flask import Flask, request, jsonify, send_from_directory
from .model import image_segmentation
from .detect_equation import detect
from .calculator import parser_equation
from .pages_segmentation import split_equations
from .remove_equation_line import remove_lines_from_equation
from werkzeug.utils import secure_filename
import os
import shutil
import json

app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath("resources/static/assets/uploads/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

QUESTIONS_DATA_FOLDER = os.path.abspath("questions/")
app.config['QUESTIONS_DATA_FOLDER'] = QUESTIONS_DATA_FOLDER

UPLOAD_SPLITS_FOLDER = os.path.abspath(
    "resources/static/assets/uploads_splits/")
app.config['UPLOAD_SPLITS_FOLDER'] = UPLOAD_SPLITS_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QUESTIONS_DATA_FOLDER, exist_ok=True)

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
            if ("shape" not in file):
                remove_lines_from_equation(file)
            image_segmentation(file)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif, doc, docx, xls, xlsx'}), 400


def _getFileNameData(filename):
    filenameNoExtensions = filename.partition('.')
    filenameNoExtensions = filenameNoExtensions[0]

    file_splits_url = os.path.join(
        app.config['UPLOAD_SPLITS_FOLDER'], filenameNoExtensions)

    return filenameNoExtensions, file_splits_url


@app.route('/api/pages/<string:filename>', methods=['GET'])
def getFilePages(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(file_path) and allowed_file(filename):
        filenameNoExtensions, file_splits_url = _getFileNameData(filename)
    else:
        return jsonify({'message': 'Unable to scan file!'}), 500

    # Build list of images of the file's pages
    segmentedPages = []
    for page in os.listdir(file_splits_url):
        # check if current path is a file
        if os.path.isdir(os.path.join(file_splits_url, page)):
            segmentedPages.append("http://localhost:5000/getSegmentedPage/" +
                                    filenameNoExtensions + "/" + page)
    
    return jsonify({'filename': filename, 'pages': segmentedPages}), 200


def _getAnswer(equation):
    try:
        equationAnswer = parser_equation(equation)
        studentAnswer = equation.split("=")[1]
        return 'Correct' if equationAnswer == studentAnswer else 'Wrong'
    except Exception:
        return "could not parse"


@app.route('/api/questions/<string:filename>', methods=['GET'])
def getQuestionsData(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(file_path) and allowed_file(filename):
        filenameNoExtensions, file_splits_url = _getFileNameData(filename)
    else:
        return jsonify({'message': 'Unable to scan file!'}), 500

    json_file_path = os.path.join(app.config['QUESTIONS_DATA_FOLDER'], filenameNoExtensions + '.json')

    if os.path.isfile(json_file_path):
        with open(json_file_path, 'r') as json_file:
            questions_data = json.load(json_file)
    else:
        try: 
            questions_data = []
            for path in next(os.walk(file_splits_url))[1]:
                questions_base_path = os.path.join(app.config['UPLOAD_SPLITS_FOLDER'], file_splits_url, path, 'equations')
                crops_equations_path = os.path.join(questions_base_path, 'crops')
                segmented_equations_path = os.path.join(questions_base_path, 'segmentations')
                
                for _, dirs, _ in os.walk(crops_equations_path):
                    for dir in dirs:
                        page_equations_path = os.path.join(crops_equations_path, dir)

                        if os.path.isdir(page_equations_path):
                            for equation in os.listdir(page_equations_path):
                                currentQuestionData = {}
                                currentQuestionData['type'] = dir
                                # Get equation image
                                equation = equation.split('.')[0]
                                page_equations_path = page_equations_path.replace("\\", "!") # Replace '/' with '!' in path to pass as parameter
                                currentQuestionData['image'] = "http://localhost:5000/getQuestion/" + page_equations_path + "/" + equation

                                # Get result for equation
                                print(equation)
                                equation = detect(os.path.join(segmented_equations_path, equation))
                                print("equation: " + equation)

                                currentQuestionData['parsed'] = equation
                                currentQuestionData['result'] = _getAnswer(equation)

                                questions_data.append(currentQuestionData)

                                with open(json_file_path, 'w') as json_file:
                                    json.dump(questions_data, json_file)
        except Exception as e:
            return jsonify({'message': 'Could not get questions data!', 'error': str(e)}), 500
        
    return jsonify({'filename': filename, 'questions_data': questions_data}), 200


@app.route('/api/files', methods=['GET'])
def getListFiles():
    try:
        fileInfos = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            fileInfos.append({
                "name": filename,
                "url": BASE_URL + filename,
            })

        return jsonify(fileInfos), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Unable to scan files!', 'error': str(e)}), 500


@app.route('/api/files/<string:filename>', methods=['GET'])
def download(filename):
    try:
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=filename, mimetype='image/jpeg')
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


@app.route('/api/emptyServer', methods=['DELETE'])
def deleteAllFiles():
    try:
        splits_path = './resources/static/assets/uploads_splits'
        shutil.rmtree(splits_path)
        print('deleted ' + splits_path)

        file_list = os.listdir(app.config['UPLOAD_FOLDER'])

        # Loop through the file list and delete each file
        for file_name in file_list:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            os.remove(file_path)
            print('deleted ' + file_path)

        return jsonify({'message': 'All files deleted.'}), 200
    except Exception as e:
        return jsonify({'message': 'Could not delete files. ' + str(e)}), 500


@app.route('/api/getSegmentedPage/<string:filename_directory>/<string:page>', methods=['GET'])
def getSegmentedPage(filename_directory, page):
    try:
        return send_from_directory(
            directory=app.config['UPLOAD_SPLITS_FOLDER'] + "\\" + filename_directory,
            path=page + ".jpg", as_attachment=True)
    except Exception as e:
        print("exception : " + str(e))
        print(app.config['UPLOAD_SPLITS_FOLDER'] + "\\" + filename_directory + "\\" + page + ".jpg")
        return jsonify({'message': 'Could not download the file. ' + str(e)}), 500

@app.route('/api/getQuestion/<string:dirname>/<string:filename>', methods=['GET'])
def getQuestion(dirname, filename):
    dirname = dirname.replace('!', '\\')
    try:
        return send_from_directory(
            directory=dirname,
            path=filename + '.jpg',
            mimetype='image/jpeg')
    except Exception as e:
        print("exception : " + str(e))
        print(dirname + "/" + filename)
        return jsonify({'message': 'Could not download the file. ' + str(e)}), 500