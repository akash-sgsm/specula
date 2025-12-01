import os
import pickle
import numpy as np

class MLPSynthesizer:
    def __init__(self, model_path="models/mlp_fusion.pkl"):
        self.model = None
        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)

    def score(self, features):
        # If MLP not available, fall back to rule-based fusion
        if self.model is None:
            weapon_conf, people_count, avg_conf, motion, density = features
            base = 1.0 - np.exp(-weapon_conf * 3.0)
            crowd = min(people_count / 5.0, 1.0) * 0.2
            activity = motion * 0.2 + density * 0.1
            return float(np.clip(base + crowd + activity, 0.0, 1.0))
        else:
            s = self.model.predict_proba([features])[0][1]  # assume binary threat class
            return float(np.clip(s, 0.0, 1.0))
