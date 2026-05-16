import requests
from bs4 import BeautifulSoup
import json
import asyncio
import time

HOST = "0.0.0.0"
PORT = 5000

NEXT_HOST = "dataprocessing"
NEXT_PORT = 5000

INSTANCE = "https://mastodon.world"

HASHTAG = "fitness"


async def recv_json(reader):
    chunks = []

    while True:
        chunk = await reader.read(4096)

        if not chunk:
            break

        chunks.append(chunk)

    raw_data = b"".join(chunks).decode("utf-8")
    return json.loads(raw_data)


async def send_json(data, host, port, retries=10, delay=1):
    for attempt in range(1, retries + 1):
        try:
            reader, writer = await asyncio.open_connection(host, port)

            message = json.dumps(data)
            writer.write(message.encode("utf-8"))

            await writer.drain()

            writer.close()
            await writer.wait_closed()

            print(f"[dataIngestionMastodon] Sent to {host}:{port}")
            return True

        except Exception as e:
            print(f"[dataIngestionMastodon] Attempt {attempt}/{retries} failed: {e}")
            await asyncio.sleep(delay)

    print(f"[dataIngestionMastodon] Failed to send to {host}:{port}")
    return False

<<<<<<< HEAD
#HASHTAG = "fitness"

def pull_mastodon_posts(limit=10, query = "fitness"):
    # Send Mastodon request
=======

def pull_mastodon_posts(limit=10):
>>>>>>> 016d7c4629e8ac2ffbd7122ef992c3ab1ddc1014
    response = requests.get(
        f"{INSTANCE}/api/v1/timelines/tag/{query}",
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


async def handle_incoming(reader, writer):
    addr = writer.get_extra_info("peername")

    try:
        print(f"[dataIngestionMastodon] Connected by {addr}")
        print("[dataIngestionMastodon] Waiting for data...")

        data = await recv_json(reader)

        print(f"[dataIngestionMastodon] Received: {data}")

        if data.get("message") != "mastodon":
            print("[dataIngestionMastodon] Message not for me. Ignoring.")
            return

        print("[dataIngestionMastodon] Starting Mastodon ingestion...")

        posts = await asyncio.to_thread(pull_mastodon_posts, 10)

        output = {
            "message": "mastodon_complete",
            "path": data.get("path", []) + ["dataIngestionMastodon"],
            "iterations": data.get("iterations", 1),
            "status": "ingested",
            "requestID": data.get("requestID"),
            "posts": posts
        }

        await send_json(output, NEXT_HOST, NEXT_PORT)
        print("[dataIngestionMastodon] Forward complete")

    except Exception as e:
        print(f"[dataIngestionMastodon] Error: {e}")

    finally:
        writer.close()
        await writer.wait_closed()


async def run_server():
    server = await asyncio.start_server(handle_incoming, HOST, PORT)

    print(f"[dataIngestionMastodon] Listening on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(run_server())