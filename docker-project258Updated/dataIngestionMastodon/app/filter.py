from bs4 import BeautifulSoup
banned_words = ["shit", "fuck", "ass", "cock", "pussy", "dick", "porn", "bitch", "slut", "whore"]

def filter_post(post):
    text = BeautifulSoup(
            post["content"],
            "html.parser"
        ).get_text(" ", strip=True)
    for word in banned_words:
        if word in text.lower():
            return False
    return True