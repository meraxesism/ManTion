import sqlite3
from tabulate import tabulate

DB_FILE = "detections.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("SELECT id, timestamp, detection_type, clip_path FROM detections ORDER BY id DESC")
rows = cursor.fetchall()

if rows:
    print(tabulate(rows, headers=["ID", "Timestamp", "Type", "Clip Path"], tablefmt="grid"))
else:
    print("No detections found.")

conn.close()
