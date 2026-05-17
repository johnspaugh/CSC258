#Pardon the language, but we need to filter out posts with these words in them. We make this list and then check the text of the post for these words.
banned_words = ["shit", "fuck", "ass", "cock", "pussy", "dick", "porn", "bitch", "slut", "whore", "nsfw"]

def filter_post(post):
    text = getattr(post.record, "text", "")
    for word in banned_words:
        if word in text.lower():
            return False
    return True