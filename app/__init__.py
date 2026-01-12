"""Flask Application Factory"""
from flask import Flask
from flask_cors import CORS


def create_app(config_name='development', arm_controller=None):
    """Create and configure Flask app"""
    app = Flask(__name__)

    # Configuration
    if config_name == 'testing':
        app.config['TESTING'] = True

    app.config['JSON_SORT_KEYS'] = False

    # CORS
    CORS(app)

    # Inject arm controller
    app.arm_controller = arm_controller

    # Register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Error handlers
    from app.errors import ArmControllerError

    @app.errorhandler(ArmControllerError)
    def handle_arm_error(e):
        return {'error': e.user_message, 'code': e.code}, e.code

    @app.errorhandler(400)
    def bad_request(e):
        return {'error': 'Bad request'}, 400

    @app.errorhandler(503)
    def unavailable(e):
        return {'error': 'Arm not available'}, 503

    return app
