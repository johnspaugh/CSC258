banned_words = ["shit", "fuck", "ass", "cock", "pussy", "dick", "porn", "bitch", "slut", "whore"]

def filter_post(post):
    text = getattr(post.record, "text", "")
    tags = getattr(post.record, "tags", [])
    for word in banned_words:
        if word in text.lower() or any(word in tag.lower() for tag in tags):
            return False
    return True