# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 15:23:59 2018

@author: Adish
"""
import pandas as pd
import json
import re
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

#consumer key, consumer secret, access token, access secret.
ckey=  'tVIcrrTSV25b0L2KCRWsthbAZ'
csecret=  'SFJSQrCao5prmbqWSGcT5YFsfKX6FnYd2l7ZQBmhLT7g8sl7Hb'
atoken=  '1947267980-fX8uOOkVTm9GKQ6rmqR3cE27k3Z9W88waTSNxsR'
asecret=  '9nf4XXJUKx6URh9NQwOi77z8a0Mv8tUMYtQBRsi69OMPg'

tweetlist=[]

#Removes URL from tweets
def removeURL(tweet):               
        return re.sub(r'http\S+',' ',tweet)

 #Removes Non Alphabet Characters from Tweet
def removeNonAlpha(tweet):
        return re.sub('[^a-zA-Z]+',' ',tweet)
    
#Converts all words into their Root Words and remove stop words
def findRootWords(tweet1):
    tweet1 = tweet1.split()
    ps = PorterStemmer()
    tweet1 = [ps.stem(word) for word in tweet1 if not word in set(stopwords.words('english'))]
    return ' '.join(tweet1)


class listener(StreamListener):
    
    def __init__(self,count,total):
        pass

    def on_data(self, data):
        tweet=json.loads(data)
        tweet1=tweet['text'][3:]                    # extract tweet from json and remove RT from beginning of tweet
        tweet1=tweet1.encode('utf-8').decode('utf-8')   #convert byte type into string 
        tweet1 = removeURL(tweet1)
        tweet1 = removeNonAlpha(tweet1)
        tweet1 = tweet1.lower()
        tweet1 = findRootWords(tweet1)
        tweetlist.append(tweet1)
        
        global count
        global totaltweet
        
        count=count+1
        print("{}. {}".format(count,tweet1))
        if count == totaltweet:
            return False
        else:
            return True
        

    def on_error(self, status):
        print(status)
        

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
count = 0
totaltweet = int(input("Enter Total Number Of Tweets : "))
keyword=input("Enter Keyword : ")
twitterStream = Stream(auth, listener(count,totaltweet))
twitterStream.filter(track=[keyword])
df = pd.DataFrame(tweetlist, columns=['tweet'])
df.to_csv('tweets.csv', index=False)

'''
tw=pd.read_csv("tweets.csv")

for i,r in tw.iterrows():
    print(type(str(i)))
'''