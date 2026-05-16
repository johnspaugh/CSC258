
import asyncio
import json

HOST = "0.0.0.0"
PORT = 5000

NEXT_HOST = "musclebot"
NEXT_PORT = 5000


async def send_json(data, host, port):
    try:
        reader, writer = await asyncio.open_connection(host, port)

        message = json.dumps(data)
        writer.write(message.encode("utf-8"))

        await writer.drain()

        writer.close()
        await writer.wait_closed()

        print(f"[dataProcessing] Sent to {host}:{port}")

    except Exception as e:
        print(f"[dataProcessing] Error sending to {host}:{port}: {e}")


async def receive_all(reader):
    chunks = []

    while True:
        data = await reader.read(4096)

        if not data:
            break

        chunks.append(data)

    return b"".join(chunks).decode("utf-8")


async def handle_incoming(reader, writer):
    addr = writer.get_extra_info("peername")

    try:
        raw_data = await receive_all(reader)

        if not raw_data:
            return

        data = json.loads(raw_data)

        print(f"[dataProcessing] Received from {addr}, source={data.get('source', 'unknown')}")

        if "path" not in data:
            data["path"] = []

        data["path"].append("dataProcessing")
        data["status"] = "processed"
        data["processed_by"] = "dataProcessing"

        if "webinterface" in data["path"]:
            await send_json(data, "webinterface", NEXT_PORT)
        else:
            await send_json(data, "musclebot", NEXT_PORT)

    
    except Exception as e:
        print(f"[dataProcessing] Error handling message: {e}")

    finally:
        writer.close()
        await writer.wait_closed()


async def run_server():
    server = await asyncio.start_server(handle_incoming, HOST, PORT)

    print(f"[dataProcessing] Listening on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(run_server())


        

