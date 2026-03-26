import socket
import json
import threading
import time

HOST = "0.0.0.0"
PORT = 5000

NEXT_HOST = "dataprocessing"
NEXT_PORT = 5000


def send_json(data, host, port):
    """Send JSON data to the next container."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host, port))
            message = json.dumps(data)
            client.sendall(message.encode())
            print(f"[dataIngestion] Sent to {host}:{port} -> {data}")
    except Exception as e:
        print(f"[dataIngestion] Error sending to {host}:{port}: {e}")


def handle_incoming(conn, addr):
    """Receive JSON, append ingestion data, and forward it."""
    try:
        raw_data = conn.recv(4096).decode()
        if not raw_data:
            return

        data = json.loads(raw_data)
        print(f"[dataIngestion] Received from {addr}: {data}")

        # Append this service to the path
        data["path"].append("dataIngestion")
        data["status"] = "ingested"
        data["ingested_by"] = "dataIngestion"
        data["ingested_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

        print("[dataIngestion] Forwarding to dataProcessing...")
        send_json(data, NEXT_HOST, NEXT_PORT)

    except Exception as e:
        print(f"[dataIngestion] Error handling incoming message: {e}")
    finally:
        conn.close()


def run_server():
    """Listen for incoming messages from dataRequest."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[dataIngestion] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_incoming, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    run_server()