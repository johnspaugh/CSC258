# johnspaugh attempt at json code

import json
import re
import os
from pathlib import Path
from models import DataModelRetrieved, ReplyRef, Main
from dataclasses import asdict

# Global variable to store the JSON formatted data
processed_data_json = None

# ?example?
# Reconstruct InspectionData if present
        # inspection_data = None
        # if asset_data.get('inspection_data'):
        #     inspection_data = InspectionData(**asset_data['inspection_data'])

#recieved data, then sort into DataModelRetrieved 

# Read data from MichealSampleData.md
def read_and_parse_sample_data(file_path):
    """
    Read MichealSampleData.md and parse it into raw text data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = f.read()
        return raw_data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

def extract_fields_from_text(raw_data):
    """
    Extract relevant fields from the raw Bluesky data text using regex patterns
    Returns a list of dictionaries with extracted fields
    """
    extracted_data = []
    
    # Extract display_name
    display_name_match = re.search(r"display_name='([^']*)'", raw_data)
    display_name = display_name_match.group(1) if display_name_match else ""
    
    # Extract handle
    handle_match = re.search(r"handle='([^']*)'", raw_data)
    handle = handle_match.group(1) if handle_match else ""
    
    # Extract text
    text_match = re.search(r"text='([^']*)'", raw_data)
    text = text_match.group(1) if text_match else ""
    
    # Extract created_at (from record)
    created_at_match = re.search(r"record=Record\(created_at='([^']*)'", raw_data)
    created_at = created_at_match.group(1) if created_at_match else ""
    
    # Extract indexed_at
    indexed_at_match = re.search(r"indexed_at='([^']*)'", raw_data)
    indexed_at = indexed_at_match.group(1) if indexed_at_match else ""
    
    # Extract tags (if exists, could be None)
    tags_match = re.search(r"tags=(None|'[^']*')", raw_data)
    tags = tags_match.group(1) if tags_match else "None"
    if tags == "None":
        tags = None
    else:
        tags = tags.strip("'")
    
    # Extract reply information
    reply = None
    reply_match = re.search(r"reply=ReplyRef\(parent=Main\(cid='([^']*)',\s*uri='([^']*)'", raw_data)
    if reply_match:
        parent_cid = reply_match.group(1)
        parent_uri = reply_match.group(2)
        parent = Main(cid=parent_cid, uri=parent_uri, py_type='com.atproto.repo.strongRef')
        
        root_match = re.search(r"root=Main\(cid='([^']*)',\s*uri='([^']*)'", raw_data)
        if root_match:
            root_cid = root_match.group(1)
            root_uri = root_match.group(2)
            root = Main(cid=root_cid, uri=root_uri, py_type='com.atproto.repo.strongRef')
            reply = ReplyRef(parent=parent, root=root)
    
    # Extract python_map (placeholder - set to empty string if not available)
    python_map = ""
    
    extracted_data.append({
        'display_name': display_name,
        'text': text,
        'created_at': created_at,
        'handle': handle,
        'reply': reply,
        'tags': tags,
        'indexed_at': indexed_at,
        'python_map': python_map
    })
    
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



# good things to pull when examining MichealSampleData file
# display_name
# text
# created_at
# handle
# reply (Maybe if its not wierd) ref
# tags (if not have then don't include)
# indexed_at
# python map
# 25 posts, looks like the most recent #

# INGEST: triceps
# while(true)
# {
#      Do stuff
# }
# ALLOWANCE: Bluesky
# caps the number of pulls can do
# INGEST: triceps 30
