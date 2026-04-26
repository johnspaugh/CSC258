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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "docker-project258Updated" / "dataIngestion" / "bluesky"))
sys.path.append(str(ROOT))  # Add JSON_docker directory to path

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

# Import functions from receiveList to process Bluesky data
try:
    from receiveList import (
        get_posts,
        extract_fields_from_text,
        filter_to_data_model,
        convert_to_json,
        get_processed_data_json
    )
except ImportError:
    # Fallback: import from parent directory
    import importlib.util
    spec = importlib.util.spec_from_file_location("receiveList", str(ROOT / "receiveList.py"))
    receiveList = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(receiveList)
    get_posts = receiveList.get_posts
    extract_fields_from_text = receiveList.extract_fields_from_text
    filter_to_data_model = receiveList.filter_to_data_model
    convert_to_json = receiveList.convert_to_json
    get_processed_data_json = receiveList.get_processed_data_json

@app.get("/api/process-bluesky-data")
def process_bluesky_data():
    """
    Process Bluesky posts data through the receiveList pipeline
    Returns the processed JSON data
    """
    try:
        # Get posts from Bluesky
        raw_text_data = get_posts()
        
        if raw_text_data:
            extracted_vars = []
            filtered_vars = []
            
            # Process each post
            for post in raw_text_data:
                # Extract fields from raw text
                extracted = extract_fields_from_text(post)
                extracted_vars.append(extracted)
                
                # Filter into DataModelRetrieved objects
                filtered_vars.extend(filter_to_data_model(extracted))
            
            # Convert to JSON and store in global variable
            json_data = convert_to_json(filtered_vars)
            
            if json_data:
                return {
                    "success": True,
                    "record_count": len(filtered_vars),
                    "processed_data": json.loads(json_data)
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