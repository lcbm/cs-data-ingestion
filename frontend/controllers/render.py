"""Flask renderer routes."""
import os

import flask
import pandas as pd

import frontend.constants as constants
import frontend.interactors.plot as plot


v1 = flask.Blueprint("render_v1", __name__)


@v1.route("images", methods=["GET"])
def images():
    """ Endpoint to display images in a static html page. """
    flask.current_app.logger.info("request received by the 'render.images' controller")
    images = [
        image
        for image in os.listdir(constants.STATIC_DIR_PATH)
        if image.endswith(".png") or image.endswith(".gif")
    ]
    flask.current_app.logger.debug(f"{images}")
    return flask.render_template("images.html", images=images)


@v1.route("create", methods=["GET"])
def create():
    """ Endpoint to generate images. """
    flask.current_app.logger.info("request received by the 'render.create' controller")

    df = pd.read_csv(constants.REPORT_FILE_PATH)
    flask.current_app.logger.info(f"df={df}")

    unique_sessions = df[constants.REPORT_COLUMN_SESSION].unique()
    for session in unique_sessions:
        plot.genered_2d_line_graph_png(df, constants.REPORT_COLUMN_SESSION, session)

    return flask.redirect(flask.url_for("render_v1.images"))
