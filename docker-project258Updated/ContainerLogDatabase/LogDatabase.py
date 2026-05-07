import socket
import sqlite3
import json

HOST = "0.0.0.0"
PORT = 5000
LOGDATABASE = "/app/data/logs.db"



def setup_db():
    conn = sqlite3.connect(LOGDATABASE)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT,
            username TEXT,
            poster TEXT,
            createdAt TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_log(service, username, poster, createdAt, message):
    conn = sqlite3.connect(LOGDATABASE)
    cur = conn.cursor()

    # Record the data
    cur.execute(
        "INSERT INTO logs (service, username, poster, createdAt, message) VALUES (?, ?, ?, ?, ?)",
        (service, username, poster, createdAt, message)
    )

    # Finish connection
    conn.commit()
    conn.close()

# Create database if it doesnt already exist
setup_db()

# Begin accepting connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Log Database Manager Running...")

# Keep running until app is closed
while True:
    conn, addr = server.accept()
    message = []

    # Continue to receive chunks until message is complete
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        message.append(chunk)

    # combine the chunks and deserialize into an object
    data = b"".join(message).decode()
    log = json.loads(data)

    # record in log
    save_log( log.get("service", ""), log.get("username", ""), log.get("poster", ""), log.get("createdAt", ""), log.get("message", ""))

    print(log)

    conn.close()