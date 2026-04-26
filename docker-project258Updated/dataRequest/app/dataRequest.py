import socket
import json
import time

HOST = "0.0.0.0"
PORT = 5000

NEXT_HOST = "dataingestion"
NEXT_PORT = 5000


def send_json(data, host, port, retries=10, delay=1):
    """Send JSON data to another container with retry logic."""
    for attempt in range(1, retries + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((host, port))
                message = json.dumps(data)
                client.sendall(message.encode())
                print(f"[dataRequest] Sent to {host}:{port} -> {data}")
                return True
        except Exception as e:
            print(f"[dataRequest] Attempt {attempt}/{retries} failed: {e}")
            time.sleep(delay)

    print(f"[dataRequest] Failed to send to {host}:{port} after {retries} attempts")
    return False

def start_initial_message():
    data = {
        "message": "request",
        "path": ["dataRequest"],
        "iterations": 1,
        "status": "requested"
    }
    return data


def handle_incoming(conn, addr):
    """Handle message returning from dataProcessing."""
    try:
        raw_data = conn.recv(65536).decode()
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