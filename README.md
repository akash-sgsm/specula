# Specula - Smart CCTV Surveillance with Real-Time Threat Detection

## 🚀 Overview
A web-based CCTV surveillance system that streams live video, detects threats (weapons, violence, burglary), computes a threat score using dual YOLOv8 + MLP fusion, and sends real-time alerts via SMS/email.

## ✨ Features
- Live CCTV/IP camera feed via Flask + OpenCV
- Dual YOLOv8 detection (fast + accurate models)
- Threat scoring with MLP fusion (or rule-based fallback)
- Automatic SMS/email alerts (Twilio + SMTP)
- SQLite logging with screenshots
- Web dashboard: live feed, logs, manual SOS

## 🛠️ Tech Stack
- **Frontend:** Flask, HTML/CSS
- **Backend:** Python, OpenCV
- **ML Models:** YOLOv8n + YOLOv8s
- **Fusion:** MLP (scikit-learn) or rule-based
- **Alerts:** Twilio SMS, SMTP email
- **Database:** SQLite

## 📂 Setup

1. Clone repo:
   ```bash
   git clone https://github.com/akash-sgsm/specula.git
   cd specula
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python download_models.py
   ```

3. Configure `app/config.py` with your camera URL, Twilio/SMTP credentials.

4. Run the app:
   ```bash
   python -m app.run
   ```

5. Open http://localhost:5000 in your browser.

## 📊 Project Structure
- `app/detection/` – YOLOv8 models, threat scoring, fusion
- `app/web/` – Flask routes, alerts, database
- `models/` – Trained YOLOv8 weights
- `tests/` – Unit tests
- `download_models.py` – Auto-download YOLO models

## 🧠 Threat Scoring
- **Fast Model (YOLOv8n):** Quick inference
- **Accurate Model (YOLOv8s):** High precision
- **MLP Fusion:** Combines both predictions for confidence
- **Alerts Triggered:** When threat score > threshold

## 🔐 Security & Credits

**Developer:** Akash SGSM  
**Repository:** https://github.com/akash-sgsm/specula.git

## 📝 License
MIT License – Feel free to modify and distribute.

## 📧 Support
For issues and contributions, visit the [GitHub repository](https://github.com/akash-sgsm/specula.git).

thank u...