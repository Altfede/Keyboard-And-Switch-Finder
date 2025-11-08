"""Entry point dell'applicazione Flask"""
from flask import Flask, render_template
from flask_cors import CORS
from .api.routes import api, load_products
import config


def create_app():
    """Factory function per creare l'app Flask"""
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')

    # Configurazione
    app.config.from_object(config)

    # CORS
    CORS(app)

    # Registra blueprint API
    app.register_blueprint(api, url_prefix='/api')

    # Carica prodotti all'avvio
    with app.app_context():
        load_products()

    # Route principale
    @app.route('/')
    def index():
        """Pagina principale"""
        return render_template('index.html')

    @app.route('/wizard')
    def wizard():
        """Wizard di ricerca"""
        return render_template('wizard.html')

    @app.route('/results')
    def results():
        """Pagina risultati"""
        return render_template('results.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
