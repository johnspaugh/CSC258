# This is the main FastAPI application for the web interface. It serves static files and provides an example API endpoint.
# python -m uvicorn web_main:app --reload
# Make sure to have a 'static' directory with an 'index.html' file in the same directory as this script for it to work properly.
# The example API endpoint can be accessed at http://localhost:8000/api/hello?name=YourName to see the greeting message.
#  http://127.0.0.1:8000   
#  perhaps needed install below packages:
# python -m pip install uvicorn
# python -m pip install fastapi uvicorn
# python -m venv venv
# pip show uvicorn
import json
import os
import queue as queue_mod
import socket
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from receiveList import get_processed_data_json, process_data
from models import CommandMessage
from dataclasses import asdict
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

#serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the index.html at the root path, which will be the main entry point for the web interface. 
@app.get("/")
def read_index():
    return FileResponse("static/index.html")

# Example API endpoint to demonstrate functionality. Which was used in a test button in the frontend to verify the API is working.
@app.get("/api/hello")
def hello(name: str = "World"):
    return {"message": f"Hello, {name}!"}


# ── Callback socket server (port 5000) ───────────────────────────────────────
# dataProcessing connects here when it sees "webinterface" in the message path.
# Each HTTP request registers a Queue keyed by requestID; the socket thread
# deposits the payload so the HTTP handler can pick it up.

_pending: dict = {}
_req_counter = 0
_counter_lock = threading.Lock()


def _next_req_id() -> int:
    global _req_counter
    with _counter_lock:
        _req_counter += 1
        return _req_counter


def _handle_callback(conn: socket.socket):
    chunks = []
    try:
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
    finally:
        conn.close()
    if not chunks:
        return
    try:
        data = json.loads(b"".join(chunks).decode())
        req_id = data.get("requestID")
        if req_id in _pending:
            _pending[req_id].put(data)
    except Exception as e:
        print(f"[webinterface] Callback error: {e}")


def _socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("0.0.0.0", 5000))
        srv.listen()
        print("[webinterface] Callback listener on port 5000")
        while True:
            conn, _ = srv.accept()
            threading.Thread(target=_handle_callback, args=(conn,), daemon=True).start()


threading.Thread(target=_socket_server, daemon=True).start()
# ─────────────────────────────────────────────────────────────────────────────

# API endpoint to trigger data processing. It sends a command message to the appropriate service (Mastodon or Bluesky) and waits for the response via the callback socket.
@app.get("/api/process-data")
def get_process_data(datasource: str, typeDataSelected: str):
    req_id = _next_req_id()
    q: queue_mod.Queue = queue_mod.Queue()
    _pending[req_id] = q

    try:
        if datasource == "mastodon":
            HOST = os.environ.get("INGEST_Mastodon_HOST", "localhost")
            msg = "mastodon"
        else:
            HOST = os.environ.get("INGEST_Bluesky_HOST", "localhost")
            msg = typeDataSelected or "fitness"

        message = asdict(CommandMessage(message=msg, requestID=req_id, path=["webinterface"]))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, 5000))
            s.sendall(json.dumps(message).encode("utf-8"))
            s.shutdown(socket.SHUT_WR)

        try:
            data = q.get(timeout=30)
        except queue_mod.Empty:
            return {"success": False, "error": "Timeout: pipeline did not respond"}

        posts = data.get("posts", [])
        if not posts:
            return {"success": False, "error": f"No posts retrieved from {datasource}"}

        raw_text_data = [json.dumps(post) for post in posts]
        json_data = process_data(raw_text_data)
        parsed = json.loads(json_data)
        if parsed:
            return {"success": True, "record_count": len(parsed), "processed_data": parsed}
        else:
            return {"success": False, "error": "No data after processing"}

    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        _pending.pop(req_id, None)


# Example API endpoint to retrieve processed data (for demonstration purposes) in global state already, else return error.
@app.get("/api/processed-data")
def get_processed_data():
    json_data = get_processed_data_json()
    if json_data is not None:
        return {"processed_data": json.loads(json_data)}
    else:
        return {"error": "Processed data not available"}
