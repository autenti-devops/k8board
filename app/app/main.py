from flask import Flask


def create_app():
    from . import configuration
    configuration.set_logging_level()
    app_ = Flask(__name__)

    configuration.load_kubernetes_config()
    with app_.app_context():
        configuration.override_url_for()

    from . import controller
    app_.register_blueprint(controller.bp)
    app_.add_url_rule('/', endpoint='index')

    return app_


app = create_app()
