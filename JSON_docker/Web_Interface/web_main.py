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


