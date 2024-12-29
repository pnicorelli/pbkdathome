from flask import Flask, send_from_directory
from routes.hash_routes import hash_routes
from routes.crypto_routes import crypto_routes
from config import Config

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(hash_routes)
    app.register_blueprint(crypto_routes)
    
    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('static', path)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)