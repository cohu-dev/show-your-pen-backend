import tweepy
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


class TwitterAPI:
    def __init__(self):
        self.CK = os.environ.get("CK")
        self.CS = os.environ.get("CS")
        self.AK = os.environ.get("AK")
        self.AS = os.environ.get("AS")

    def upload_base(self, file, text):
        auth = tweepy.OAuthHandler(self.CK, self.CS)
        auth.set_access_token(self.AK, self.AS)
        api = tweepy.API(auth)
        api.update_status_with_media(text, file)

    def upload_realtime(self, file):
        text = "ð æ°ãããã³ãæç¨¿ããã¾ãã ð\n\nð New pen photo is uploaded ð\n\nURLï¼https://pen.cohu.dev\n\n#ææ¿å·å¥½ãã¨ç¹ãããã"
        self.upload_base(file, text)

    def upload_random(self, file):
        text = "ð·ã©ã³ãã ãªåçããç´¹ä»ð·\n\nð·Display random pen photoð·\n\nURLï¼https://pen.cohu.dev\n\n#ææ¿å·å¥½ãã¨ç¹ãããã"
        self.upload_base(file, text)
