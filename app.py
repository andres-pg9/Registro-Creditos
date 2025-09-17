from flask import Flask
from extensions import db
from models import Credito
from routes import creditos_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Registrar rutas
    app.register_blueprint(creditos_bp)

    @app.route('/')
    def home():
        return "Creación de API de créditos con Flask"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
