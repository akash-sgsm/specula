from ultralytics import YOLO
import numpy as np

class YOLOModel:
    def __init__(self, model_path, conf=0.35, iou=0.45):
        self.model = YOLO(model_path)
        self.conf = conf
        self.iou = iou

    def predict(self, frame):
        results = self.model.predict(source=frame, conf=self.conf, iou=self.iou, verbose=False)
        dets = []
        for r in results:
            for b in r.boxes:
                cls_id = int(b.cls)
                label = r.names[cls_id]
                conf = float(b.conf)
                x1, y1, x2, y2 = map(int, b.xyxy[0])
                dets.append({"label": label, "conf": conf, "bbox": (x1, y1, x2, y2)})
        return dets

class WeaponDetector:
    """Specialized weapon detection with enhanced confidence filtering for knife detection"""
    def __init__(self, model_path, conf=0.45, iou=0.5):
        self.model = YOLO(model_path)
        self.conf = conf
        self.iou = iou
        self.weapon_classes = ["knife", "gun", "sword", "axe", "firearm"]
        
    def predict(self, frame):
        results = self.model.predict(source=frame, conf=self.conf, iou=self.iou, verbose=False)
        dets = []
        for r in results:
            for b in r.boxes:
                cls_id = int(b.cls)
                label = r.names[cls_id]
                conf = float(b.conf)
                x1, y1, x2, y2 = map(int, b.xyxy[0])
                
                # Enhanced filtering for weapon detection
                if label.lower() in self.weapon_classes:
                    # Lower threshold for precise knife detection
                    if conf >= 0.4:  # Stricter threshold for weapons
                        dets.append({"label": label, "conf": conf, "bbox": (x1, y1, x2, y2), "weapon": True})
                else:
                    dets.append({"label": label, "conf": conf, "bbox": (x1, y1, x2, y2), "weapon": False})
        return dets
