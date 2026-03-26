import socket
import json
import time

HOST = "0.0.0.0"
PORT = 5000

NEXT_HOST = "dataingestion"
NEXT_PORT = 5000


def send_json(data, host, port):
    """Send JSON data to another container."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host, port))
            message = json.dumps(data)
            client.sendall(message.encode())
            print(f"[dataRequest] Sent to {host}:{port} -> {data}")
    except Exception as e:
        print(f"[dataRequest] Error sending to {host}:{port}: {e}")


def start_initial_message():
    """Create the starting JSON message."""
    data = {
        "message": "start",
        "path": ["dataRequest"],
        "iterations": 1,
        "status": "requested"
    }
    return data


def handle_incoming(conn, addr):
    """Handle message returning from dataProcessing."""
    try:
        raw_data = conn.recv(4096).decode()
        if not raw_data:
            return

        data = json.loads(raw_data)
        print(f"[dataRequest] Received: {data}")

        print("[dataRequest] Done. One full cycle complete.")

    finally:
        conn.close()

def run_server():
    """Listen for returning messages from dataProcessing."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[dataRequest] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            handle_incoming(conn, addr)


if __name__ == "__main__":
    # Give other containers time to start
    time.sleep(3)

    # Send first message into pipeline
    initial_data = start_initial_message()
    send_json(initial_data, NEXT_HOST, NEXT_PORT)

    # Then wait for processed message to come back
    run_server()