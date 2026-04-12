from atproto import Client
import json
import socket

HOST = "0.0.0.0"
PORT = 5000

NEXT_HOST = "dataProcessing"
NEXT_PORT = 5000

def send_json(data, host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host, port))
            message = json.dumps(data)
            client.sendall(message.encode())
            print(f"[dataIngestion] Sent to {host}:{port}")
    except Exception as e:
        print(f"[dataIngestion] Error sending to {host}:{port}: {e}")

def get_posts():
    print("[dataIngestion] Creating Bluesky client...")
    client = Client()

    print("[dataIngestion] Logging in...")
    client.login('fitnesstracker.bsky.social', 'M+}5aj+C)5,^sU4')

    print("[dataIngestion] Searching posts...")
    response = client.app.bsky.feed.search_posts({
        "q": "fitness",
        "tag": ["fitness"]
    })

    posts = response.posts
    print(f"[dataIngestion] Found {len(posts)} posts")

    results = []
    for post in posts:
        obj = {
            "text": getattr(post.record, "text", ""),
            "display_name": getattr(post.author, "display_name", ""),
            "handle": getattr(post.author, "handle", ""),
            "created_at": getattr(post.author, "created_at", ""),
            "tags": getattr(post.record, "tags", [])
        }
        results.append(obj)

    return results

def handle_incoming(conn, addr):
    try:
        print(f"[dataIngestion] Connected by {addr}")

        print("[dataIngestion] Waiting for data...")
        raw_data = conn.recv(65536).decode()

        print(f"[dataIngestion] Raw data: {raw_data}")

        if not raw_data:
            print("[dataIngestion] No data received")
            return

        data = json.loads(raw_data)
        print(f"[dataIngestion] Parsed JSON: {data}")

        if data.get("message") == "request":
            print("[dataIngestion] Request received, fetching posts...")
            posts = get_posts()

            outgoing = {
                "message": "ingested",
                "path": data.get("path", []) + ["dataIngestion"],
                "iterations": data.get("iterations", 1),
                "status": "ingested",
                "posts": posts
            }

            print("[dataIngestion] Forwarding to dataProcessing...")
            send_json(outgoing, NEXT_HOST, NEXT_PORT)
            print("[dataIngestion] Forward complete")
        else:
            print("[dataIngestion] Message was not 'request'")

    except Exception as e:
        print(f"[dataIngestion] Error: {e}")
    finally:
        conn.close()

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print("[dataIngestion] Listening...")

        while True:
            conn, addr = server.accept()
            handle_incoming(conn, addr)

if __name__ == "__main__":
    run_server()