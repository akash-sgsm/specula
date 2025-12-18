import numpy as np

class ThreatScorer:
    def __init__(self, thresholds=None, buffer_size=5):
        # Per-class thresholds - KNIFE DETECTION OPTIMIZED
        self.thresholds = thresholds or {
            "person": 0.5,
            "knife": 0.4,      # Lower threshold for faster knife detection
            "gun": 0.5,
            "sword": 0.4,      # Also detect swords
            "firearm": 0.5,
            "fight": 0.7,
            "robbery": 0.7
        }
        self.frame_buffer = []
        self.buffer_size = buffer_size

    def score_frame(self, detections):
        """
        detections: list of dicts like
        [{"class":"person","conf":0.8,"bbox":(x,y,w,h)}, ...]
        """
        score = 0.0

        # Per-class confidence checks
        for det in detections:
            cls, conf = det.get("class") or det.get("label"), det["conf"]
            if cls in self.thresholds and conf > self.thresholds[cls]:
                # WEAPON BOOST: Increase score weight for weapons
                if cls.lower() in ["knife", "gun", "sword", "firearm"]:
                    score += conf * 1.5  # 50% boost for weapons
                else:
                    score += conf

        # Contextual boost: weapon + person nearby
        persons = [d for d in detections if d.get("class", d.get("label")) == "person"]
        weapons = [d for d in detections if d.get("class", d.get("label")).lower() in ["knife", "gun", "sword", "firearm"]]
        if persons and weapons:
            score += 0.8  # Increased from 0.5

        # Normalize score
        score = min(score, 1.0)

        # Temporal smoothing
        self.frame_buffer.append(score)
        if len(self.frame_buffer) > self.buffer_size:
            self.frame_buffer.pop(0)

        avg_score = np.mean(self.frame_buffer)
        return avg_score
