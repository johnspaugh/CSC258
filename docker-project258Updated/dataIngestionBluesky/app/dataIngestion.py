from atproto import Client
import json
import asyncio

HOST = "0.0.0.0"
PORT = 5000

NEXT_HOST = "dataprocessing"
NEXT_PORT = 5000


async def send_json(data, host, port):
    try:
        reader, writer = await asyncio.open_connection(host, port)

        message = json.dumps(data)
        writer.write(message.encode())
        await writer.drain()

        writer.close()
        await writer.wait_closed()

        print(f"[dataIngestion] Sent to {host}:{port}")

    except Exception as e:
        print(f"[dataIngestion] Error sending to {host}:{port}: {e}")


def get_posts(query="fitness"):
    print("[dataInestion] Creating Bluesky client...")
    client = Client()

    print("[dataIngestion] Logging in...")
    client.login("fitnesstracker.bsky.social", "M+}5aj+C)5,^sU4")

    print("[dataIngestion] Searching posts...")
    response = client.app.bsky.feed.search_posts({
        "q": query,
        "tag": [query]
    })

    posts = response.posts
    print(f"[dataIngestion] Found {len(posts)} posts")

    results = []
    for post in posts:
        obj = {
            "text": getattr(post.record, "text", ""),
            "display_name": getattr(post.author, "display_name", ""),
            "handle": getattr(post.author, "handle", ""),
            "created_at": getattr(post.record, "created_at", ""),
            "tags": getattr(post.record, "tags", [])
        }
        results.append(obj)

    return results


async def handle_incoming(reader, writer):
    addr = writer.get_extra_info("peername")

    try:
        print(f"[dataIngestion] Connected by {addr}")

        print("[dataIngestion] Waiting for data...")
        raw_data = await reader.read(65536)
        raw_data = raw_data.decode()

        print(f"[dataIngestion] Raw data: {raw_data}")

        if not raw_data:
            print("[dataIngestion] No data received")
            return

        data = json.loads(raw_data)
        print(f"[dataIngestion] Parsed JSON: {data}")

        request = data.get("message", "")
        if len(request) == 0:
            request = "fitness"

        print("[dataIngestion] Request received, fetching posts...")

        # Bluesky client is blocking, so run it in another thread
        posts = await asyncio.to_thread(get_posts, request)

        outgoing = {
            "message": "ingested",
            "path": data.get("path", []) + ["dataIngestion"],
            "iterations": data.get("iterations", 1),
            "status": "ingested",
            "requestID": data.get("requestID"),
            "posts": posts
        }

        print("[dataIngestion] Forwarding to dataProcessing...")
        await send_json(outgoing, NEXT_HOST, NEXT_PORT)
        print("[dataIngestion] Forward complete")

    except Exception as e:
        print(f"[dataIngestion] Error: {e}")

    finally:
        writer.close()
        await writer.wait_closed()


async def run_server():
    server = await asyncio.start_server(handle_incoming, HOST, PORT)

    print("[dataIngestion] Listening...")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(run_server())