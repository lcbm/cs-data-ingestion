"""Flask App configuration file."""

import logging
import os

import dotenv

import frontend.constants as constants


dotenv.load_dotenv(os.path.join(constants.BASEDIR, "frontend.env"))


class Base:
    """Configuration class used as base for all environments."""

    DEBUG = False
    TESTING = False

    LOGGING_FORMAT = "[%(asctime)s] %(levelname)s in %(message)s"
    LOGGING_LOCATION = "frontend.log"
    LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", logging.DEBUG)


class Development(Base):
    """Configuration class for development environment.

    Parameters
    ----------
    Base: base configuration object.
    """

    DEBUG = True
    TESTING = False
    ENV = "dev"


class Staging(Base):
    """Configuration class for development staging environment.

    Parameters
    ----------
    Base: base configuration object.
    """

    DEBUG = False
    TESTING = True
    ENV = "staging"


class Production(Base):
    """Configuration class for development production environment.

    Parameters
    ----------
    Base: base configuration object.
    """

    DEBUG = False
    TESTING = False
    ENV = "prod"


config = {
    "development": "frontend.config.Development",
    "staging": "frontend.config.Staging",
    "production": "frontend.config.Production",
    "default": "frontend.config.Development",
}


def configure_app(app):
    """Configures the Flask app according to the FLASK_ENV
    envar. In case FLASK_ENV is not defined, then use the
    'default' configuration.

    Parameters
    ----------
    app: flask.Flask
        Flask app Module.
    """

    # Configure app
    config_name = os.environ.get("FLASK_ENV", "default")
    app.config.from_object(config[config_name])

    # Configure logging
    handler = logging.FileHandler(app.config["LOGGING_LOCATION"])
    handler.setLevel(app.config["LOGGING_LEVEL"])
    formatter = logging.Formatter(app.config["LOGGING_FORMAT"])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
