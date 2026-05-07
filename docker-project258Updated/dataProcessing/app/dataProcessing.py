import socket
import json
import struct

HOST = "0.0.0.0"
PORT = 5000

NEXT_HOST = "musclebot"
NEXT_PORT = 5000



def send_json(data, host, port, chunk_size=4096):
    try:
        # Connect with receiver
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host, port))
            message = json.dumps(data).encode()

            total_sent = 0
            
            # Continue sending chunks until message is complete
            for i in range(0, len(message), chunk_size):
                chunk = message[i:i + chunk_size]
                client.sendall(chunk)
                total_sent += len(chunk)

            # Notify receiver message has been completely sent
            client.shutdown(socket.SHUT_WR)

            print(f"[dataProcessing] Sent {total_sent}/{len(message)} bytes to {host}:{port}")

    except Exception as e:
        print(f"[dataProcessing] Error sending to {host}:{port}: {e}")


def receive_all(conn):
    chunks = []
    # Continue receiving chunks until message is complete
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
        
        # Digest incoming data
        data = json.loads(raw_data)
        print(f"[dataProcessing] Received from {addr}")

        if "path" not in data:
            data["path"] = []
        
        # Update log data
        data["path"].append("dataProcessing")
        data["status"] = "processed"
        data["processed_by"] = "dataProcessing"
        
        send_json(data, NEXT_HOST, NEXT_PORT)

    except Exception as e:
        print(f"[dataProcessing] Error handling message: {e}")
    finally:
        conn.close()


def run_server():
    # Set up and run service
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[dataProcessing] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            handle_incoming(conn, addr)


if __name__ == "__main__":
    run_server()