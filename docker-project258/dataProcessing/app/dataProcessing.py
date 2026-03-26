import socket
import json
import threading
import time

HOST = "0.0.0.0"
PORT = 5000

NEXT_HOST = "datarequest"
NEXT_PORT = 5000


def send_json(data, host, port):
    """Send JSON data to the next container."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host, port))
            message = json.dumps(data)
            client.sendall(message.encode())
            print(f"[dataProcessing] Sent to {host}:{port} -> {data}")
    except Exception as e:
        print(f"[dataProcessing] Error sending to {host}:{port}: {e}")


def handle_incoming(conn, addr):
    """Receive JSON, append processing data, and send back to dataRequest."""
    try:
        raw_data = conn.recv(4096).decode()
        if not raw_data:
            return

        data = json.loads(raw_data)
        print(f"[dataProcessing] Received from {addr}: {data}")

        data["path"].append("dataProcessing")
        data["status"] = "processed"
        data["processed_by"] = "dataProcessing"
        data["processed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

        print("[dataProcessing] Sending back to dataRequest...")
        send_json(data, NEXT_HOST, NEXT_PORT)

    except Exception as e:
        print(f"[dataProcessing] Error handling incoming message: {e}")
    finally:
        conn.close()


def run_server():
    """Listen for incoming messages from dataIngestion."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[dataProcessing] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_incoming, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    run_server()