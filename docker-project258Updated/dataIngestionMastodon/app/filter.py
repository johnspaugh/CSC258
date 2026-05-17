from bs4 import BeautifulSoup

#Again, pardon the language. The implementation is slightly different than the one in Bluesky because the structure of the post is different.
banned_words = ["shit", "fuck", "ass", "cock", "pussy", "dick", "porn", "bitch", "slut", "whore", "nsfw"]

def filter_post(post):
    text = BeautifulSoup(
            post["content"],
            "html.parser"
        ).get_text(" ", strip=True)
    for word in banned_words:
        if word in text.lower():
            return False
    return True