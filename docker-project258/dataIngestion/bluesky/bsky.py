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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    posts = get_posts()

    for post in posts: 
        s.sendall(post.encode("utf-8"))
        data = s.recv(1024)