"""Flask upload routes."""
import flask

import frontend.constants as constants


v1 = flask.Blueprint("upload_v1", __name__)


@v1.route("", methods=["GET"])
def upload():
    """ Endpoint to render html page to upload files. """
    flask.current_app.logger.info("request received by the 'upload' controller")
    return flask.render_template("upload.html")


@v1.route("", methods=["POST"])
def save():
    """ Endpoint to upload csv file in a html page. """
    flask.current_app.logger.info("request received by the 'upload' controller")
    if "file" not in flask.request.files:
        flask.current_app.logger.debug("no file in flask.request")
        return flask.render_template("upload.html")

    file = flask.request.files["file"]
    flask.current_app.logger.debug(f"file.filename={file.filename}")
    if file.filename == "":
        flask.current_app.logger.debug("no selected file")

    file.save(constants.REPORT_FILE_PATH)
    flask.current_app.logger.info("file saved")
    return flask.redirect(flask.url_for("render_v1.create"))
