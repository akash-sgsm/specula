import cv2
import time
from app.detection.pipeline import DualYOLOPipeline
from app.web.db import LogStore
from app.web.alerts import AlertManager

class Streamer:
    def __init__(self, camera_source, threat_threshold):
        self.source = self._parse_source(camera_source)
        self.threshold = threat_threshold
        self.pipeline = DualYOLOPipeline()
        self.logger = LogStore()
        self.alerter = AlertManager()
        self._last_alert_ts = 0

    def _parse_source(self, src):
        try:
            return int(src)
        except ValueError:
            return src  # RTSP/http URL

    def frame_generator(self):
        cap = cv2.VideoCapture(self.source)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera source: {self.source}")

        while True:
            ok, frame = cap.read()
            if not ok:
                time.sleep(0.02)
                continue

            result = self.pipeline.process(frame)  # dict with dets, score, overlay, labels
            score = result["score"]
            overlay = result["overlay"]
            labels = result["labels"]

            if score >= self.threshold:
                self.logger.log_event(labels, score, overlay)
                now = time.time()
                if now - self._last_alert_ts > 30:  # rate-limit
                    self.alerter.send_auto_alert(score, labels)
                    self._last_alert_ts = now

            ret, buf = cv2.imencode(".jpg", overlay)
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buf.tobytes() + b"\r\n")
