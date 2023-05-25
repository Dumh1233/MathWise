from flask import Flask, request, jsonify, send_from_directory
from .model import image_segmentation
from .detect_equation import detect
from .calculator import parser_equation
from .pages_segmentation import split_equations
from werkzeug.utils import secure_filename
import os
import shutil

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
        return jsonify({'message': 'Correct'}), 200
    else:
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

                # Build list of images of the file's pages
                segmentedPages = []
                for path in os.listdir(segmented_pages_url):
                    # check if current path is a file
                    if os.path.isdir(os.path.join(segmented_pages_url, path)):
                        segmentedPages.append("http://localhost:5000/getSegmentedPage/" +
                                              filenameNoExtensions + "/" + path)

                # Build list of images of the file's equations
                segmentedEquations = []
                
                for path in next(os.walk(segmented_pages_url))[1]:
                    for subdir, dirs, files in os.walk(segmented_pages_url + '\\' + path + '\\' + 'equations\\' + 'crops\\'):
                        for dir in dirs:
                            pageEquationsPath = os.path.join(app.config['UPLOAD_SPLITS_FOLDER'], segmented_pages_url, path, 'equations', 'crops', dir)
                            segmentedEquationsPath = os.path.join(app.config['UPLOAD_SPLITS_FOLDER'], segmented_pages_url, path, 'equations', 'segmentations')

                            if os.path.isdir(pageEquationsPath):
                                for equation in os.listdir(pageEquationsPath):
                                    currentEquation = {}

                                    # Get equation image
                                    equation = equation.split('.')[0]
                                    pageEquationsPath = pageEquationsPath.replace("\\", "!") # Replace '/' with '!' in path to pass as parameter
                                    currentEquation['image'] = "http://localhost:5000/getSegmentedEquation/" + pageEquationsPath + "/" + equation

                                    # Get result for equation
                                    print(equation)
                                    equation = detect(os.path.join(segmentedEquationsPath, equation))
                                    print("equation: " + equation)
                                    try:
                                        equationAnswer = parser_equation(equation)
                                        studentAnswer = equation.split("=")[1]
                                        if equationAnswer == studentAnswer:
                                            currentEquation['result'] = 'Correct'
                                        else:
                                            currentEquation['result'] = 'Wrong'
                                    except Exception:
                                        print("could not parse")
                                    
                                    segmentedEquations.append(currentEquation)

                fileInfos.append({
                    "name": filename,
                    "url": BASE_URL + filename,
                    "segmentedPages": segmentedPages,
                    "segmentedEquations": segmentedEquations
                })
        return jsonify(fileInfos), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Unable to scan files!', 'error': str(e)}), 500


@app.route('/api/files/<string:filename>', methods=['GET'])
def download(filename):
    try:
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename, mimetype='image/jpeg')
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
            filename=page + ".jpg", as_attachment=True)
    except Exception as e:
        print("exception : " + str(e))
        print(app.config['UPLOAD_SPLITS_FOLDER'] + "\\" + filename_directory + "\\" + page + ".jpg")
        return jsonify({'message': 'Could not download the file. ' + str(e)}), 500

@app.route('/api/getSegmentedEquation/<string:dirname>/<string:filename>', methods=['GET'])
def getSegmentedEquation(dirname, filename):
    dirname = dirname.replace('!', '\\')
    try:
        return send_from_directory(
            directory=dirname,
            filename=filename + '.jpg',
            mimetype='image/jpeg')
    except Exception as e:
        print("exception : " + str(e))
        print(dirname + "/" + filename)
        return jsonify({'message': 'Could not download the file. ' + str(e)}), 500