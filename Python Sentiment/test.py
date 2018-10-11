import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re

class listener(StreamListener):
    
    def on_data(self,data):
        
        all_data=json.loads(data)
        tweet=all_data["text"].encode("utf-8")
        tweet=" ".join(re.findall("[a-zA-Z]+", tweet.decode("utf-8")))
        print(tweet)

    def on_error(self,status):
        print(status)



ckey=  'tVIcrrTSV25b0L2KCRWsthbAZ'
csecret=  'SFJSQrCao5prmbqWSGcT5YFsfKX6FnYd2l7ZQBmhLT7g8sl7Hb'
atoken=  '1947267980-fX8uOOkVTm9GKQ6rmqR3cE27k3Z9W88waTSNxsR'
asecret=  '9nf4XXJUKx6URh9NQwOi77z8a0Mv8tUMYtQBRsi69OMPg'

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

twitterStream=  Stream(auth, listener())
twitterStream.filter(track=["Donald Trump"])