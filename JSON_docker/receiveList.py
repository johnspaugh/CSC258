# johnspaugh attempt at json code

import json
from modulefinder import test
import re
import os
from pathlib import Path
from models import DataModelRetrieved, ReplyRef, Main
from dataclasses import asdict

# from dataIngestion.app.test import get_posts
# from dataIngestion.bluesky.bsky import get_posts
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "docker-project258Updated" / "dataIngestion" / "bluesky"))
from bsky import get_posts

# Global variable to store the JSON formatted data
processed_data_json = None

# ------------------------------------------------
#list = get_posts() is stolen from bsky.py, create and will read from M2SampleData.md
# from atproto import Client, client_utils
# # import json
# # import socket
# # HOST = "127.0.0.1"  # "0.0.0.0"
# # PORT = 5000
# def get_posts():
#     client = Client()
#     client.login('fitnesstracker.bsky.social', 'M+}5aj+C)5,^sU4')
#     posts = client.app.bsky.feed.search_posts({"q": "fitness", "tag": ["fitness"]})
#     posts = posts.posts

#     list = []

#     for post in posts:
#         obj = {}
#         obj["text"] = post.record.text
#         obj["display_name"] = post.author.display_name
#         obj["handle"] = post.author.handle
#         obj["created_at"] = post.author.created_at
#         obj["tags"] = post.record.tags
#         list.append(json.dumps(obj))

#     print(f"Extracted {len(list)} posts")
#     print(list)
#     print("Finished extracting posts")
#     print("first post: ", list[0])
#     return list
#used as a reference for the above code, will be used to read from M2SampleData.md instead of bluesky
#------------------------------------------------

# Read data from MichealSampleData.md or M2SampleData.md depend on the file_path provided
def read_and_parse_sample_data(file_path):
    """
    Read MichealSampleData.md or M2SampleData.md and parse it into raw text data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = f.read()
        return raw_data
        # list = []

        # for post in raw_data:
        #     obj = {}
        #     obj["text"] = post.record.text
        #     obj["display_name"] = post.author.display_name
        #     obj["handle"] = post.author.handle
        #     obj["created_at"] = post.author.created_at
        #     obj["tags"] = post.record.tags
        #     list.append(json.dumps(obj))

        # return list
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

def extract_fields_from_text(raw_data):
    """
    Extract relevant a list of dictionaries from the raw Bluesky data text using regex patterns
    Returns a list in json format with extracted fields
    """
    extracted_data = []
    # print("first post: ", raw_list_data[0])
    # print("------------------------")

    try:
        # Check if raw_list_data is a list and has at least one element
        # if isinstance(raw_list_data, list) and len(raw_list_data) > 0:
        if raw_data and isinstance(raw_data, str):
            # raw_data = raw_list_data[0]  # Assuming we want to extract from the first item in the list
            raw_data = json.loads(raw_data)  # Add this line to convert the JSON string back to a dictionary
            #then we can extract fields from the dictionary using get() method to avoid KeyError if the key is missing

            # Extract fields using regex or direct access
            # display_name = raw_data["display_name"] if "display_name" in raw_data else ""
            # handle = raw_data["handle"] if "handle" in raw_data else ""
            # text = raw_data["text"] if "text" in raw_data else ""
            # created_at = raw_data["created_at"] if "created_at" in raw_data else ""
            # indexed_at = raw_data["indexed_at"] if "indexed_at" in raw_data else ""
            # tags = raw_data["tags"] if "tags" in raw_data else []
            # reply_ref = raw_data.get("reply_ref", None)
            display_name = raw_data.get("display_name", "")
            handle = raw_data.get("handle", "")
            text = raw_data.get("text", "")
            created_at = raw_data.get("created_at", "")
            indexed_at = raw_data.get("indexed_at", "")
            tags = raw_data.get("tags", []) #"None" ) 
            # if tags == "None":
            #     tags = None
            # else:
            #     tags = tags.strip("'")
            reply_ref = raw_data.get("reply_ref", None)

            # Extract python_map (placeholder - set to empty string if not available)
            python_map = ""
            
            # Process reply_ref if it exists
            reply = None
            if reply_ref:
                parent_cid = reply_ref.get("parent", {}).get("cid", "")
                parent_uri = reply_ref.get("parent", {}).get("uri", "")
                parent = Main(cid=parent_cid, uri=parent_uri, py_type='com.atproto.repo.strongRef')
                # parent = reply_ref["parent"] if "parent" in reply_ref else ""
                # parent_cid = ""
                # parent_uri = ""
                # if parent:
                #     parent_cid = parent["cid"] if "cid" in parent else ""
                #     parent_uri = parent["uri"] if "uri" in parent else ""
                # parent = Main(cid=parent_cid, uri=parent_uri, py_type='com.atproto.repo.strongRef')

                root_cid = reply_ref.get("root", {}).get("cid", "")
                root_uri = reply_ref.get("root", {}).get("uri", "")
                root = Main(cid=root_cid, uri=root_uri, py_type='com.atproto.repo.strongRef')
                # root = reply_ref["root"] if "root" in reply_ref else ""
                # root_cid = ""
                # root_uri = ""
                # if root:
                #     root_cid = root["cid"] if "cid" in root else ""
                #     root_uri = root["uri"] if "uri" in root else ""
                # root = Main(cid=root_cid, uri=root_uri, py_type='com.atproto.repo.strongRef')
                
                reply = ReplyRef(parent=parent, root=root)
            
            # Create a dictionary with the extracted fields
            extracted_dict = {
                "display_name": display_name,
                'text': text,
                'created_at': created_at,
                'handle': handle,
                'reply': reply,
                'tags': tags,
                'indexed_at': indexed_at,
                'python_map': python_map
            }
            extracted_data.append(extracted_dict)
        else:
            print("Error: raw_data is not a valid list or is empty.")
    except Exception as e:
        print(f"Error extracting fields: {e}")

    return extracted_data   

def filter_to_data_model(extracted_data):
    """
    Filter and convert extracted data into DataModelRetrieved objects
    """
    filtered_data = []
    
    for data in extracted_data:
        try:
            # Create DataModelRetrieved object from extracted data
            data_model = DataModelRetrieved(
                    display_name=data['display_name'],
                    text=data['text'],
                    created_at=data['created_at'],
                    handle=data['handle'],
                    reply=data['reply'],
                    tags=json.dumps(data['tags']) if data['tags'] is not None else "",  # Convert list to JSON string
                    indexed_at=data['indexed_at'],
                    python_map=data['python_map']
            )
            filtered_data.append(data_model)
            # filtered_data.extend(data_model)
        except Exception as e:
            print(f"Error creating DataModelRetrieved: {e}")
            continue
    
    return filtered_data

def convert_to_json(filtered_data):
    """
    Convert DataModelRetrieved objects to JSON format and store in global variable
    """
    global processed_data_json
    
    try:
        # Convert dataclasses to dictionaries for JSON serialization
        json_data = []
        for data_model in filtered_data:
            data_dict = asdict(data_model)
            json_data.append(data_dict)
        
        # Convert to JSON string
        processed_data_json = json.dumps(json_data, indent=2, default=str)
        return processed_data_json
    except Exception as e:
        print(f"Error converting to JSON: {e}")
        processed_data_json = None
        return None
    
def get_processed_data_json():
    """
    Function for other files to retrieve the processed data in JSON format
    Returns the JSON string or None if not available
    """
    global processed_data_json
    return processed_data_json

# Main execution
# Construct path to MichealSampleData.md
current_dir = Path(__file__).parent
# sample_data_path = current_dir.parent / "JSON_docker" / "MichealSampleData.md"
sample_data_path = current_dir.parent / "JSON_docker" / "M2SampleData.md"

# Read and process data
# raw_text_data = read_and_parse_sample_data(str(sample_data_path))
#when we incoprate bsky.py, we can replace the above line with raw_text_data = get_posts() to read from bluesky instead of M2SampleData.md
raw_text_data = get_posts()

if raw_text_data:
    extracted_vars = []
    filtered_vars = []
    for post in raw_text_data:
        # Extract fields from raw text
        extracted = extract_fields_from_text(post)
        extracted_vars.append(extracted)
        
        # Filter into DataModelRetrieved objects
        # filtered_vars.append(filter_to_data_model(extracted))
        filtered_vars.extend(filter_to_data_model(extracted))
    
    # Convert to JSON and store in global variable
    json_data = convert_to_json(filtered_vars)    
    # json_data = convert_to_json(extracted_vars)
    
    print(f"Processed {len(filtered_vars)} records into DataModelRetrieved objects")
    print(f"Data converted to JSON format and stored in global variable")
    
    # Display first record if available
    if filtered_vars:
        print("\nFirst record:")
        # print(f"  Handle: {filtered_vars[0].handle}")
        # print(f"  Display Name: {filtered_vars[0].display_name}")
        # print(f"  Text: {filtered_vars[0].text}")
        # print(f"  Created At: {filtered_vars[0].created_at}")
        # print(f"  Indexed At: {filtered_vars[0].indexed_at}")
        
        # Show a preview of the JSON
        if json_data:
            print("\nJSON preview (first 200 characters):")
            print(json_data[:200] + "..." if len(json_data) > 200 else json_data)

        print("\nFinished processing data.")
        print(extracted_vars[0])
        print(filtered_vars[0])
        # print(json_data)
        # To verify the JSON structure, we can parse it back to a Python object and print the first item
        parsed = json.loads(json_data)
        print(parsed[0]["display_name"])
        print(parsed[0])
