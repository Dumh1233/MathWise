from .controller import upload, getListFiles, download, remove


def routes(app):
    @app.route('/upload', methods=['POST'])
    def upload_route():
        return upload()

    @app.route('/files', methods=['GET'])
    def getListFiles_route():
        return getListFiles()

    @app.route('/files/<string:name>', methods=['GET'])
    def download_route(name):
        return download(name)

    @app.route('/files/<string:name>', methods=['DELETE'])
    def remove_route(name):
        return remove(name)
