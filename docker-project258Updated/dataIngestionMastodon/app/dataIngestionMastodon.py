import requests
from bs4 import BeautifulSoup
import json
import socket
import time

HOST = "0.0.0.0"
PORT = 5000

NEXT_HOST = "dataprocessing"
NEXT_PORT = 5000

INSTANCE = "https://mastodon.world"


def recv_json(conn):
    chunks = []

    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)

    raw_data = b"".join(chunks).decode("utf-8")
    return json.loads(raw_data)


def send_json(data, host, port, retries=10, delay=1):
    for attempt in range(1, retries + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((host, port))
                message = json.dumps(data)
                client.sendall(message.encode("utf-8"))
                print(f"[dataIngestionMastodon] Sent to {host}:{port}")
                return True
        except Exception as e:
            print(f"[dataIngestionMastodon] Attempt {attempt}/{retries} failed: {e}")
            time.sleep(delay)

    print(f"[dataIngestionMastodon] Failed to send to {host}:{port}")
    return False

HASHTAG = "fitness"

def pull_mastodon_posts(limit=10):
    response = requests.get(
        f"{INSTANCE}/api/v1/timelines/tag/{HASHTAG}",
        params={"limit": limit},
        timeout=10
    )

    response.raise_for_status()
    posts = response.json()

    normalized_posts = []

    for post in posts:
        clean_text = BeautifulSoup(
            post["content"],
            "html.parser"
        ).get_text(" ", strip=True)

        normalized_posts.append({
            "text": clean_text,
            "display_name": post["account"].get("display_name", ""),
            "handle": post["account"].get("acct", ""),
            "created_at": post.get("created_at", ""),
            "tags": [tag["name"] for tag in post.get("tags", [])]
        })

    
    print(f"[dataIngestionMastodon] Found {len(normalized_posts)} posts")


    return normalized_posts


def handle_incoming(conn, addr):
    try:
        print("[dataIngestionMastodon] Waiting for data...")
        data = recv_json(conn)

        print(f"[dataIngestionMastodon] Received: {data}")

        if data.get("message") != "mastodon":
            print("[dataIngestionMastodon] Message not for me. Ignoring.")
            return

        print("[dataIngestionMastodon] Starting Mastodon ingestion...")

        posts = pull_mastodon_posts(limit=10)

        output = {
            "message": "mastodon_complete",
            "path": data.get("path", []) + ["dataIngestionMastodon"],
            "iterations": data.get("iterations", 1),
            "status": "ingested",
            "requestID": data.get("requestID"),
            "posts": posts
        }

        send_json(output, NEXT_HOST, NEXT_PORT)

        print("[dataIngestionMastodon] Forward complete")

    except Exception as e:
        print(f"[dataIngestionMastodon] Error: {e}")

    finally:
        conn.close()


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[dataIngestionMastodon] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            handle_incoming(conn, addr)


if __name__ == "__main__":
    run_server()
