import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re



def calctime(a):
    return time.time()-a

class listener(StreamListener):
    
    def on_data(self,data):
        global initime
        t=int(calctime(initime))
        all_data=json.loads(data)
        tweet=all_data["text"].encode("utf-8")
        #username=all_data["user"]["screen_name"]
        tweet=" ".join(re.findall("[a-zA-Z]+", tweet.decode("utf-8")))
        blob=TextBlob(tweet)

        global positive
        global negative     
        global compound  
        global count
        
        count=count+1
        senti=0
        for sen in blob.sentences:
            senti=senti+sen.sentiment.polarity
            if sen.sentiment.polarity >= 0:
                positive=positive+sen.sentiment.polarity   
            else:
                negative=negative+sen.sentiment.polarity  
        compound=compound+senti        
        print(count)
        print(tweet)
        print(senti)
        print(t)
        print(str(positive) + ' ' + str(negative) + ' ' + str(compound))
        
    
        plt.axis([ 0, 70, -20,20])
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([t],[positive],'go',[t] ,[negative],'ro',[t],[compound],'bo')
        plt.show()
        plt.pause(0.0001)
        if count==200:
            return False
        else:
            return True
        
    def on_error(self,status):
        print(status)


positive=0
negative=0
compound=0

count=0
initime=time.time()
plt.ion()

ckey=  'tVIcrrTSV25b0L2KCRWsthbAZ'
csecret=  'SFJSQrCao5prmbqWSGcT5YFsfKX6FnYd2l7ZQBmhLT7g8sl7Hb'
atoken=  '1947267980-fX8uOOkVTm9GKQ6rmqR3cE27k3Z9W88waTSNxsR'
asecret=  '9nf4XXJUKx6URh9NQwOi77z8a0Mv8tUMYtQBRsi69OMPg'

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

twitterStream=  Stream(auth, listener(count))
twitterStream.filter(track=["Donald Trump","modi","putin"])
      
 

