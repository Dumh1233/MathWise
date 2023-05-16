from .controller import getAnswer, upload, getListFiles, download, remove, getSegmentedPage, deleteAllFiles


def routes(app):
    @app.route('/upload', methods=['POST'])
    def upload_route():
        return upload()

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

    @app.route('/answer', methods=['GET'])
    def getAnswer_route():
        return getAnswer()

    @app.route('/getSegmentedPage/<string:filename>/<string:page>', methods=['GET'])
    def getSegmentedPage_route(filename, page):
        return getSegmentedPage(filename, page)
