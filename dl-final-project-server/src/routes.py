from .controller import upload, getFilePages, getQuestionsData, getListFiles, download, remove, getSegmentedPage, deleteAllFiles, getQuestion


def routes(app):
    @app.route('/upload', methods=['POST'])
    def upload_route():
        return upload()

    @app.route('/pages/<string:filename>', methods=['GET'])
    def getFilePages_route(filename):
        return getFilePages(filename)

    @app.route('/questions/<string:filename>', methods=['GET'])
    def getQuestionsData_route(filename):
        return getQuestionsData(filename)

    @app.route('/files', methods=['GET'])
    def getListFiles_route():
        return getListFiles()

    @app.route('/emptyServer', methods=['DELETE'])
    def emptyServer():
        return deleteAllFiles()

    @app.route('/files/<string:name>', methods=['GET'])
    def download_route(name):
        return download(name)

    @app.route('/files/<string:name>', methods=['DELETE'])
    def remove_route(name):
        return remove(name)

    @app.route('/getSegmentedPage/<string:filename>/<string:page>', methods=['GET'])
    def getSegmentedPage_route(filename, page):
        return getSegmentedPage(filename, page)

    @app.route('/getQuestion/<string:dirname>/<string:filename>', methods=['GET'])
    def getQuestion_route(dirname, filename):
        return getQuestion(dirname, filename)
