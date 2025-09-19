"""
Sistema de Gestión de Créditos
Aplicación Flask para registro y análisis de créditos bancarios
"""

from flask import Flask, render_template, jsonify
from extensions import db
from models import Credito
from routes import creditos_bp

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuración adicional para producción
    app.config['SECRET_KEY'] = 'clave'
    
    # Inicializar extensiones
    db.init_app(app)

    # Crear tablas
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada correctamente")

    # Registrar blueprints
    app.register_blueprint(creditos_bp)

    # Rutas principales
    @app.route('/')
    def home():
        """Página de inicio de la API"""
        return jsonify({
            "mensaje": "API de Gestión de Créditos - Delta Data Consulting",
            "version": "1.0",
            "endpoints": {
                "frontend": "/frontend",
                "creditos": "/creditos",
                "estadisticas": "/creditos/estadisticas"
            }
        })

    @app.route('/frontend')
    def frontend():
        """Interfaz web del sistema"""
        return render_template("index.html")
    
    # Manejo de errores básico
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Página no encontrada"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    print("Iniciando servidor de desarrollo...")
    print("Frontend disponible en: http://127.0.0.1:5000/frontend")
    app.run(debug=True, host='127.0.0.1', port=5000)