import flask

import frontend.config
import frontend.controllers.healthcheck
import frontend.controllers.render
import frontend.controllers.upload


def create_app():
    """Initialize the core application."""

    app = flask.Flask(__name__, instance_relative_config=False)
    frontend.config.configure_app(app)

    with app.app_context():
        app.register_blueprint(
            frontend.controllers.healthcheck.bp,
            url_prefix="/healthcheck",
        )

        app.register_blueprint(
            frontend.controllers.render.v1,
            url_prefix="/v1/render",
        )

        app.register_blueprint(
            frontend.controllers.upload.v1,
            url_prefix="/v1/upload",
        )

        app.register_blueprint(
            frontend.controllers.upload.v1,
            url_prefix="/",
        )

        return app
