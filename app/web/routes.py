from flask import Blueprint, render_template, Response, current_app
from app.web.stream import Streamer
from app.web.db import LogStore
from app.web.alerts import AlertManager

web_bp = Blueprint("web", __name__)
_logger = LogStore()
_alerter = AlertManager()
_streamer = None

@web_bp.route("/")
def index():
    return render_template("index.html")

@web_bp.route("/video")
def video():
    global _streamer
    if _streamer is None:
        _streamer = Streamer(current_app.config["CAMERA_SOURCE"],
                             current_app.config["THREAT_THRESHOLD"])
    return Response(_streamer.frame_generator(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@web_bp.route("/logs")
def logs():
    events = _logger.get_events(limit=50)
    return render_template("logs.html", events=events)

@web_bp.route("/sos")
def sos():
    _alerter.send_manual_sos("Manual SOS triggered from dashboard.")
    return "SOS sent", 200
