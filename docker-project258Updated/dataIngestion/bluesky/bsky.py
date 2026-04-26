from atproto import Client, client_utils
import json
import socket

HOST = "0.0.0.0"
PORT = 5000

def get_posts():
    client = Client()
    client.login('fitnesstracker.bsky.social', 'M+}5aj+C)5,^sU4')
    posts = client.app.bsky.feed.search_posts({"q": "fitness", "tag": ["fitness"]})
    posts = posts.posts

    list = []

    for post in posts:
        obj = {}
        obj["text"] = post.record.text
        obj["display_name"] = post.author.display_name
        obj["handle"] = post.author.handle
        obj["created_at"] = post.author.created_at
        obj["tags"] = post.record.tags
        list.append(json.dumps(obj))

    return list
    # debugging testing
    # list = get_posts()
    # print("Finished getting posts")
    # print(list)

# will have to comment this area out when running the FastAPI server, since it will be imported as a module and we don't want to run this code on import
#until we adjust FastAPI to work with the docker file
# Socket connection code removed - only run when explicitly needed, not at import time
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    posts = get_posts()
    for post in posts: 
        s.sendall(post.encode("utf-8"))
        data = s.recv(1024)

