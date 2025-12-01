from ultralytics import YOLO

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
