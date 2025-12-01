# Smart CCTV Surveillance with Real-Time Threat Detection

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
   git clone https://github.com/your-username/smart-cctv.git
   cd smart-cctv
