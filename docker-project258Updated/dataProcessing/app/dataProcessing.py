import socket
import json

HOST = "0.0.0.0"
PORT = 5000

NEXT_HOST = "datarequest"
NEXT_PORT = 5000


def send_json(data, host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host, port))
            message = json.dumps(data)
            client.sendall(message.encode())
            print(f"[dataProcessing] Sent to {host}:{port}")
    except Exception as e:
        print(f"[dataProcessing] Error sending to {host}:{port}: {e}")


def receive_all(conn):
    chunks = []
    while True:
        data = conn.recv(4096)
        if not data:
            break
        chunks.append(data)
    return b"".join(chunks).decode()


def handle_incoming(conn, addr):
    try:
        raw_data = receive_all(conn)
        if not raw_data:
            return

        data = json.loads(raw_data)
        print(f"[dataProcessing] Received from {addr}")

        if "path" not in data:
            data["path"] = []

        data["path"].append("dataProcessing")
        data["status"] = "processed"
        data["processed_by"] = "dataProcessing"

        send_json(data, NEXT_HOST, NEXT_PORT)

    except Exception as e:
        print(f"[dataProcessing] Error handling message: {e}")
    finally:
        conn.close()


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[dataProcessing] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            handle_incoming(conn, addr)


if __name__ == "__main__":
    run_server()