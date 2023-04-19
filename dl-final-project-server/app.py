from flask import Flask
from flask_cors import CORS
from src.routes import routes
from src.detect_equation import load_model

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8081"}})
app.config['CORS_HEADERS'] = 'Content-Type'

routes(app)

if __name__ == '__main__':
    load_model(app.root_path)
    app.run(host='localhost', port=8080, debug=True)
