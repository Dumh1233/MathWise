from .controller import upload, get_file_pages, get_questions_data, get_list_files, download, remove, \
    get_segmented_page, delete_all_files, get_question


def routes(app):
    @app.route('/upload', methods=['POST'])
    def upload_route():
        return upload()

    @app.route('/pages/<string:filename>', methods=['GET'])
    def get_file_pages_route(filename):
        return get_file_pages(filename)

    @app.route('/questions/<string:filename>', methods=['GET'])
    def get_questions_data_route(filename):
        return get_questions_data(filename)

    @app.route('/files', methods=['GET'])
    def get_list_files_route():
        return get_list_files()

    @app.route('/emptyServer', methods=['DELETE'])
    def empty_server():
        return delete_all_files()

    @app.route('/files/<string:name>', methods=['GET'])
    def download_route(name):
        return download(name)

    @app.route('/files/<string:name>', methods=['DELETE'])
    def remove_route(name):
        return remove(name)

    @app.route('/getSegmentedPage/<string:filename>/<string:page>', methods=['GET'])
    def get_segmented_page_route(filename, page):
        return get_segmented_page(filename, page)

    @app.route('/getQuestion/<string:dir_name>/<string:filename>', methods=['GET'])
    def get_question_route(dir_name, filename):
        return get_question(dir_name, filename)
