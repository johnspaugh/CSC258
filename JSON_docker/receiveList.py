# johnspaugh attempt at json code

import json
import re
import os
from pathlib import Path
from models import DataModelRetrieved, ReplyRef, Main
from dataclasses import asdict

# Global variable to store the JSON formatted data
processed_data_json = None

# list = []

#     for post in posts:
#         obj = {}
#         obj["text"] = post.record.text
#         obj["display_name"] = post.author.display_name
#         obj["handle"] = post.author.handle
#         obj["created_at"] = post.author.created_at
#         obj["tags"] = post.record.tags
#         list.append(json.dumps(obj))

#     return list
#not complete  

# Read data from MichealSampleData.md
def read_and_parse_sample_data(file_path):
    """
    Read MichealSampleData.md and parse it into raw text data
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

def extract_fields_from_text(raw_list_data):
    """
    Extract relevant a list of dictionaries from the raw Bluesky data text using regex patterns
    Returns a list in json format with extracted fields
    """
    extracted_data = []
    
    try:
        # Check if raw_list_data is a list and has at least one element
        if isinstance(raw_list_data, list) and len(raw_list_data) > 0:
            raw_data = raw_list_data[0]  # Assuming we want to extract from the first item in the list
            
            # Extract fields using regex or direct access
            display_name = raw_data.get("display_name", "")
            handle = raw_data.get("handle", "")
            text = raw_data.get("text", "")
            created_at = raw_data.get("created_at", "")
            indexed_at = raw_data.get("indexed_at", "")
            tags = raw_data.get("tags", [])
            reply_ref = raw_data.get("reply_ref", None)

            # Extract python_map (placeholder - set to empty string if not available)
            python_map = ""
            
            # Process reply_ref if it exists
            reply = None
            if reply_ref:
                parent_cid = reply_ref.get("parent", {}).get("cid", "")
                parent_uri = reply_ref.get("parent", {}).get("uri", "")
                parent = Main(cid=parent_cid, uri=parent_uri, py_type='com.atproto.repo.strongRef')
                
                root_cid = reply_ref.get("root", {}).get("cid", "")
                root_uri = reply_ref.get("root", {}).get("uri", "")
                root = Main(cid=root_cid, uri=root_uri, py_type='com.atproto.repo.strongRef')
                
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
            print("Error: raw_list_data is not a valid list or is empty.")
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
                tags=data['tags'] if data['tags'] is not None else "",
                indexed_at=data['indexed_at'],
                python_map=data['python_map']
            )
            filtered_data.append(data_model)
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
sample_data_path = current_dir.parent / "Bot_docker" / "MichealSampleData.md"

# Read and process data
raw_text_data = read_and_parse_sample_data(str(sample_data_path))

if raw_text_data:
    # Extract fields from raw text
    extracted_vars = extract_fields_from_text(raw_text_data)
    
    # Filter into DataModelRetrieved objects
    filtered_vars = filter_to_data_model(extracted_vars)
    
    # Convert to JSON and store in global variable
    json_data = convert_to_json(filtered_vars)
    
    print(f"Processed {len(filtered_vars)} records into DataModelRetrieved objects")
    print(f"Data converted to JSON format and stored in global variable")
    
    # Display first record if available
    if filtered_vars:
        print("\nFirst record:")
        print(f"  Handle: {filtered_vars[0].handle}")
        print(f"  Display Name: {filtered_vars[0].display_name}")
        print(f"  Text: {filtered_vars[0].text}")
        print(f"  Created At: {filtered_vars[0].created_at}")
        print(f"  Indexed At: {filtered_vars[0].indexed_at}")
        
        # Show a preview of the JSON
        if json_data:
            print("\nJSON preview (first 200 characters):")
            print(json_data[:200] + "..." if len(json_data) > 200 else json_data)

