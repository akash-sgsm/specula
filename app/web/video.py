import cv2
import time
from app.detection.yolo import Detector
from app.detection.fusion import ThreatScorer
from app.web.db import LogStore

detector = Detector()
scorer = ThreatScorer()
logger = LogStore()

def get_camera_source(src):
    try:
        return int(src)
    except ValueError:
        return src  # IP cam URL

def frames(camera_source, threat_threshold):
    cap = cv2.VideoCapture(get_camera_source(camera_source))
    if not cap.isOpened():
        raise RuntimeError("Cannot open camera source")

    while True:
        ok, frame = cap.read()
        if not ok:
            time.sleep(0.05)
            continue

        dets = detector.detect(frame)
        score, labels = scorer.score(dets)
        overlay = detector.draw(frame.copy(), dets, score)

        if score >= threat_threshold:
            logger.log_event(labels, score, overlay)

        ret, buffer = cv2.imencode('.jpg', overlay)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
