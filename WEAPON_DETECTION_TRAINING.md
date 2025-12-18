# Custom Weapon Detection Model Training Guide

## Problem
Your generic YOLOv8 models aren't optimized for knife detection. Solution: Train a custom model.

## Option 1: Quick Fix - Use Pre-trained Weapon Models (Recommended First)

### Best Pre-trained Models Available:
1. **YOLOv8 Weapon Detection** - Roboflow
   ```bash
   pip install roboflow
   ```
   Download from: https://universe.roboflow.com/search?q=weapon%20detection

2. **YOLOv8 Knife Detection Dataset**
   - Search "knife detection" on Roboflow Universe
   - Download in YOLOv8 format
   - Extract to `models/` directory

### Quick Integration:
```python
# In pipeline.py, replace model path:
self.accurate = WeaponDetector("path/to/weapon-detection-model.pt", conf=0.45, iou=0.5)
```

---

## Option 2: Train Your Own Custom Model (Best Results)

### Step 1: Prepare Dataset
1. Collect knife images from:
   - Movie clips/video frames
   - Surveillance footage (public datasets)
   - Roboflow: https://universe.roboflow.com/workspace
   
2. Annotate using CVAT or Roboflow tools
   - Create YOLO format labels (txt files with bbox coordinates)
   - Recommended: 500-1000 knife images minimum

### Step 2: Structure Dataset
```
dataset/
├── images/
│   ├── train/   (60% of images)
│   ├── val/     (20% of images)
│   └── test/    (20% of images)
├── labels/
│   ├── train/
│   ├── val/
│   └── test/
└── data.yaml
```

### Step 3: Create data.yaml
```yaml
path: /path/to/dataset
train: images/train
val: images/val
test: images/test

nc: 3  # number of classes
names: ['knife', 'person', 'hand']  # class names
```

### Step 4: Training Script
Create `train_weapon_model.py`:
```python
from ultralytics import YOLO

# Load base model (nano for speed, small for accuracy)
model = YOLO('yolov8m.pt')  # Medium model for weapons

# Train
results = model.train(
    data='dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    patience=20,  # Early stopping
    device=0,  # GPU device
    conf=0.45,
    iou=0.5,
    optimizer='SGD',
    lr0=0.01,
    momentum=0.9
)

# Validate and test
metrics = model.val()
print(metrics)

# Export trained model
model.export(format='pt')  # Save as .pt file
```

Run training:
```bash
python train_weapon_model.py
```

### Step 5: Use Trained Model
```python
# In models.py
self.accurate = WeaponDetector("runs/detect/train/weights/best.pt", conf=0.45, iou=0.5)
```

---

## Option 3: Use Roboflow Pre-trained Models (Fastest)

### Steps:
1. Go to: https://universe.roboflow.com/workspace
2. Search: "weapon detection" or "knife detection"
3. Find a model with >100 images trained
4. Download YOLOv8 format
5. Place in `models/` folder
6. Update pipeline.py path

**Recommended Models:**
- `Weapon Detection v1` - Good general performance
- `Knife Detection` - Specialized for knives

---

## Hyperparameter Tuning for Better Knife Detection

### For Faster Detection (Lower Latency):
```python
# Use nano model
WeaponDetector("models/yolov8n-weapon.pt", conf=0.4, iou=0.45)
```

### For Higher Precision (Better Accuracy):
```python
# Use medium/large model
WeaponDetector("models/yolov8m-weapon.pt", conf=0.5, iou=0.5)
```

### Confidence Threshold Tuning:
- **Lower conf (0.3-0.4):** Catch more knives (higher recall)
- **Higher conf (0.5-0.6):** Fewer false positives (higher precision)

### Recommended for Knife Detection:
```python
conf=0.45,  # Balanced - catches most knives with minimal false positives
iou=0.5     # Prevents duplicate detections
```

---

## Validation Checklist

After deployment:
- [ ] Test with knife videos in different lighting
- [ ] Test with hand gestures (to avoid false positives)
- [ ] Test with kitchen knives, pocket knives, large knives
- [ ] Measure FPS performance
- [ ] Check false positive rate
- [ ] Monitor alert accuracy in logs

---

## Troubleshooting

### Issue: Still missing knives
- **Solution 1:** Lower confidence threshold to 0.3
- **Solution 2:** Train custom model with your surveillance footage
- **Solution 3:** Ensemble with multiple models

### Issue: Too many false positives
- **Solution 1:** Increase confidence threshold to 0.6
- **Solution 2:** Add hard-negative mining (images without knives)
- **Solution 3:** Improve fusion logic in threat_scorer.py

### Issue: Slow detection
- **Solution:** Switch to nano or tiny model (yolov8n, yolov8t)

---

## Testing Script

```python
import cv2
from app.detection.pipeline import DualYOLOPipeline

# Load your enhanced pipeline
pipeline = DualYOLOPipeline()

# Test on video
cap = cv2.VideoCapture('test_knife_video.mp4')
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    result = pipeline.process(frame)
    
    # Check knife detection
    knife_detections = [d for d in result['dets'] if d['label'].lower() == 'knife']
    print(f"Knife detections: {len(knife_detections)}, Threat Score: {result['score']:.2f}")
    
    cv2.imshow('Detection', result['overlay'])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Resources

- **Roboflow:** https://roboflow.com/ (Pre-labeled datasets)
- **YOLOv8 Docs:** https://docs.ultralytics.com/
- **Weapon Detection Datasets:**
  - https://universe.roboflow.com/workspace
  - Search: "weapon", "knife", "gun", "firearm"
