banned_words = ["shit", "fuck", "ass", "cock", "pussy", "dick", "porn", "bitch", "slut", "whore"]

def filter_post(post):
    text = getattr(post.record, "text", "")
    for word in banned_words:
        if word in text.lower():
            return False
    return True