import os
import sqlite3
import time
import cv2

class LogStore:
    def __init__(self, db_path=os.getenv("DATABASE_PATH", "smart_cctv.db")):
        self.db_path = db_path
        self._init()

    def _init(self):
        os.makedirs("data/screenshots", exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.execute("""CREATE TABLE IF NOT EXISTS events(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                labels TEXT,
                score REAL,
                image_path TEXT
            );""")

    def log_event(self, labels, score, frame):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        img_name = f"data/screenshots/{int(time.time()*1000)}.jpg"
        cv2.imwrite(img_name, frame)
        with sqlite3.connect(self.db_path) as con:
            con.execute("INSERT INTO events(timestamp, labels, score, image_path) VALUES(?,?,?,?)",
                        (ts, ",".join(labels), score, img_name))

    def get_events(self, limit=50):
        with sqlite3.connect(self.db_path) as con:
            cur = con.execute(
                "SELECT timestamp, labels, score, image_path FROM events ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            rows = cur.fetchall()
        return [{"timestamp": r[0], "labels": r[1], "score": r[2], "image_path": r[3]} for r in rows]
