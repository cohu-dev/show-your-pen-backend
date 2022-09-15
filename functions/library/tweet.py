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
        text = "🔔 新しいペンが投稿されました 🔔\n\n🔔 New pen photo is uploaded 🔔\n\nURL：https://pen.cohu.dev\n\n#文房具好きと繋がりたい"
        self.upload_base(file, text)

    def upload_random(self, file):
        text = "📷ランダムな写真をご紹介📷\n\n📷Display random pen photo📷\n\nURL：https://pen.cohu.dev\n\n#文房具好きと繋がりたい"
        self.upload_base(file, text)
