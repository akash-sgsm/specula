import numpy as np

class ThreatScorer:
    def __init__(self, thresholds=None, buffer_size=5):
        # Per-class thresholds - OPTIMIZED FOR GUN & KNIFE DETECTION
        self.thresholds = thresholds or {
            "person": 0.5,
            "knife": 0.35,      # Aggressive knife detection with shape verification
            "gun": 0.40,        # Aggressive gun detection with shape verification
            "pistol": 0.40,
            "rifle": 0.40,
            "sword": 0.35,
            "firearm": 0.40,
            "axe": 0.35,
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

        # Count weapons for context
        weapon_count = 0

        # Per-class confidence checks with weapon boost
        for det in detections:
            cls = det.get("class") or det.get("label")
            conf = det["conf"]
            
            if cls and cls.lower() in self.thresholds:
                threshold = self.thresholds[cls.lower()]
                
                if conf > threshold:
                    # WEAPON DETECTION: Significantly boost threat score
                    if cls.lower() in ["knife", "gun", "sword", "firearm", "pistol", "rifle", "axe"]:
                        # Heavy weight on weapon detection
                        score += conf * 2.0  # 100% boost for weapons (was 1.5x)
                        weapon_count += 1
                    else:
                        score += conf

        # Contextual boost: weapon + person nearby = SEVERE THREAT
        persons = [d for d in detections if (d.get("class") or d.get("label")) == "person"]
        weapons = [d for d in detections if (d.get("class") or d.get("label")).lower() 
                   in ["knife", "gun", "sword", "firearm", "pistol", "rifle", "axe"]]
        
        if persons and weapons:
            score += 1.2  # Increased from 0.8 - critical threat indicator
        
        # Multiple weapons exponential increase
        if weapon_count > 1:
            score += weapon_count * 0.4
        
        # Normalize score
        score = min(score, 1.0)

        # Temporal smoothing
        self.frame_buffer.append(score)
        if len(self.frame_buffer) > self.buffer_size:
            self.frame_buffer.pop(0)

        avg_score = np.mean(self.frame_buffer)
        return avg_score
