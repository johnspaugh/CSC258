import socket
import sqlite3
import json
import asyncio

HOST = "0.0.0.0"
PORT = 5000
LOGDATABASE = "/app/data/logs.db"


### Connect to and create the log database if not already made
def SetupDatabase():
    # Connect to sql database
    conn = sqlite3.connect(LOGDATABASE)
    cur = conn.cursor()

    print("Creating new log database if necessary...")

    # create database if it doesnt already exist
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

     # Finish and close connection to database
    conn.commit()
    conn.close()

### Save and record Logs
def SaveLog(service, username, poster, createdAt, message):
    # Connect to sql database
    conn = sqlite3.connect(LOGDATABASE)
    cur = conn.cursor()

    # Record the data
    cur.execute(
        "INSERT INTO logs (service, username, poster, createdAt, message) VALUES (?, ?, ?, ?, ?)",
        (service, username, poster, createdAt, message)
    )

    # Finish and close connection to database
    conn.commit()
    conn.close()


### Receives and handles requests from clients
async def HandleRequests(reader, writer):
    try:
        message = []

        # continue to receive chunks until the full message comple
        while True:
            chunk = await reader.read(4096)
            if not chunk:
                break
            message.append(chunk)

        # continue to receive chunks until the full message comple
        data = b"".join(message).decode()
        log = json.loads(data)

        # save the log and write to sql database
        SaveLog(
            log.get("service", ""),
            log.get("username", ""),
            log.get("poster", ""),
            log.get("createdAt", ""),
            log.get("message", "")
        )

        print(log)
        print("Log Saved")

    # Finish the request
    finally:
        writer.close()
        await writer.wait_closed()


async def RunLogDatabaseManager():
    SetupDatabase()

    LogManager = await asyncio.start_server(HandleRequests, HOST, PORT)

    print("Log Database Manager Running...")

    async with LogManager:
        await LogManager.serve_forever()



asyncio.run(RunLogDatabaseManager())





