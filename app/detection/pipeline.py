import cv2
from app.detection.models import YOLOModel, WeaponDetector
from app.detection.features import extract_features, WEAPON_CLASSES
from app.detection.fusion import MLPSynthesizer

class DualYOLOPipeline:
    def __init__(self):
        # Two complementary models (speed + accuracy)
        self.fast = YOLOModel("models/yolov8n.pt", conf=0.35, iou=0.45)
        self.accurate = WeaponDetector("models/yolov8s.pt", conf=0.45, iou=0.5)  # Enhanced for weapons
        self.fuser = MLPSynthesizer()
        self.prev_gray = None

    def _ensemble(self, dets_a, dets_b):
        # Merge detections: union with confidence-weighted preference
        dets = dets_a + dets_b
        # Optional: NMS or bbox merge—kept simple for MVP
        return dets

    def _draw(self, frame, dets, score):
        for d in dets:
            x1, y1, x2, y2 = d["bbox"]
            label = d["label"]
            conf = d["conf"]
            color = (0, 0, 255) if label in WEAPON_CLASSES else (0, 200, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(frame, f"Threat: {score:.2f}", (18, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        return frame

    def process(self, frame):
        dets_fast = self.fast.predict(frame)
        dets_acc = self.accurate.predict(frame)
        dets = self._ensemble(dets_fast, dets_acc)

        features, gray = extract_features(dets, frame, self.prev_gray)
        self.prev_gray = gray
        score = self.fuser.score(features)
        labels = sorted(set(d["label"] for d in dets))
        overlay = self._draw(frame.copy(), dets, score)
        return {"dets": dets, "score": score, "overlay": overlay, "labels": labels}
