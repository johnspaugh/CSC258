# This is the main FastAPI application for the web interface. It serves static files and provides an example API endpoint.
# python -m uvicorn web_main:app --reload
# Make sure to have a 'static' directory with an 'index.html' file in the same directory as this script for it to work properly.
# The example API endpoint can be accessed at http://localhost:8000/api/hello?name=YourName to see the greeting message.
#  http://127.0.0.1:8000   
#  perhaps needed install below packages:
# python -m pip install uvicorn
# python -m pip install fastapi uvicorn
# python -m venv venv
# pip show uvicorn
import json
import os
import socket
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# sys.path.append(str(ROOT / "docker-project258Updated" / "dataIngestionBluesky" / "bluesky"))
sys.path.append(str(ROOT))  # Add JSON_docker directory to path

from receiveList import get_processed_data_json, process_data
from models import CommandMessage
from dataclasses import asdict
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at root
@app.get("/")
def read_index():
    return FileResponse("static/index.html")

# Example API endpoint
@app.get("/api/hello")
def hello(name: str = "World"):
    return {"message": f"Hello, {name}!"}

# call on dataIngestion to get the processed data in JSON format
def _recv_posts(host, port, message_dict):
    chunks = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps(message_dict).encode("utf-8"))
        #socket.SHUT_WR closes only the sending side — 
        # the socket stays open for reading the response. 
        # This is the standard pattern for half-close: "I'm done sending, now I'll just listen."
        s.shutdown(socket.SHUT_WR)
        while True:
            data = s.recv(4096)
            if not data:
                break
            chunks.append(data.decode("utf-8"))
    full = "".join(chunks)
    if not full:
        return []
    posts = json.loads(full)
    return [json.dumps(post) for post in posts]

@app.get("/api/get-bluesky-data")
def get_bluesky_data(datapoint: str = "fitness"):
    HOST = os.environ.get("INGEST_Bluesky_HOST", "localhost")
    message = asdict(CommandMessage(message="bluesky"))
    return _recv_posts(HOST, 5000, message)

@app.get("/api/get-mastodon-data")
def get_mastodon_data(datapoint: str = "fitness"):
    HOST = os.environ.get("INGEST_Mastodon_HOST", "localhost")
    message = asdict(CommandMessage(message="mastodon"))
    return _recv_posts(HOST, 5000, message)
# {"message": "This endpoint will process Bluesky data and return the processed JSON. Implementation is in progress."}

@app.get("/api/process-data")
def get_process_data(datasource: str, typeDataSelected: str):
    """
    Process  posts data from Bluesky or Mastodon through the receiveList pipeline
    Returns the processed JSON data
    """
    try:
        
        raw_text_data = []
        if datasource == "mastodon":
            raw_text_data = get_mastodon_data(typeDataSelected)
        else: #elif datasource == "bluesky":
            raw_text_data = get_bluesky_data(typeDataSelected)
        
        if raw_text_data:
            
            json_data =process_data(raw_text_data)
            parsed = json.loads(json_data)
            if parsed:
                return {
                    "success": True,
                    "record_count": len(parsed),
                    "processed_data": parsed
                }
            else:
                return {"success": False, "error": "Failed to convert data to JSON"}
        else:
            return {"success": False, "error": "No posts retrieved from Bluesky"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

# once dataProcessing and dataIngestion are done, 
# we can call the get_processed_data_json function to retrieve the processed data in JSON format and return it through an API endpoint
@app.get("/api/processed-data")
def get_processed_data():
    json_data = get_processed_data_json()
    if json_data is not None:
        return {"processed_data": json.loads(json_data)}
    else:
        return {"error": "Processed data not available"}


