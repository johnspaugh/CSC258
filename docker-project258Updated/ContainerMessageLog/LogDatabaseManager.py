import socket
import sqlite3
import json

HOST = "0.0.0.0"
PORT = 5000
DB = "/app/data/logs.db"


def setup_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_log(service, message):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO logs (service, message) VALUES (?, ?)",
        (service, message)
    )

    conn.commit()
    conn.close()


setup_db()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Log Database Manager Running...")

while True:
    conn, addr = server.accept()

    data = conn.recv(4096).decode()
    log = json.loads(data)

    save_log(log["service"], log["message"])

    print(log)

    conn.close()