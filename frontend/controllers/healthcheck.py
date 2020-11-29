"""Frontend healthcheck route."""

import flask


bp = flask.Blueprint("healthcheck", __name__)


@bp.route("healthcheck", methods=["GET"])
def healthcheck():
    """Endpoint to check the service's health."""
    flask.current_app.logger.info("request received by the 'healthcheck' controller")
    return flask.jsonify({"message": "Healthy"})
