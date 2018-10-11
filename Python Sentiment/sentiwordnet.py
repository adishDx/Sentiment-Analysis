import nltk
from nltk.corpus import sentiwordnet as swn
import pandas as pd
import matplotlib.pyplot as plt
positive=0
neutral=0
negative=0

df = pd.read_csv("tweets.csv")
for index,row in df.iterrows():
    tweet=row['tweet']
    #doc="Nice and friendly place with excellent food and friendly and helpful staff. You need a car though. The children wants to go back! Playground and animals entertained them and they felt like at home. I also recommend the dinner! Great value for the price!"
    sentences = nltk.sent_tokenize(tweet)
    stokens = [nltk.word_tokenize(sent) for sent in sentences]
    taggedlist=[]
    for stoken in stokens:        
         taggedlist.append(nltk.pos_tag(stoken))
    wnl = nltk.WordNetLemmatizer()
    
    score_list=[]
    for idx,taggedsent in enumerate(taggedlist):
        score_list.append([])
        for idx2,t in enumerate(taggedsent):
            newtag=''
            lemmatized=wnl.lemmatize(t[0])
            if t[1].startswith('NN'):
                newtag='n'
            elif t[1].startswith('JJ'):
                newtag='a'
            elif t[1].startswith('V'):
                newtag='v'
            elif t[1].startswith('R'):
                newtag='r'
            else:
                newtag=''       
            if(newtag!=''):    
                synsets = list(swn.senti_synsets(lemmatized, newtag))
                #Getting average of all possible sentiments, as you requested        
                score=0
                if(len(synsets)>0):
                    for syn in synsets:
                        score+=syn.pos_score()-syn.neg_score()
                    score_list[idx].append(score/len(synsets))
                
    print(score_list)
    sentence_sentiment=[]
    
    for score_sent in score_list:
        sentence_sentiment.append(sum([word_score for word_score in score_sent])/len(score_sent))
    print("Sentiment for Tweet : "+str(index))
   
 
    
    if float(format(sentence_sentiment[0],'.2f'))<0.0:
        negative=negative+1
    elif float(format(sentence_sentiment[0],'.2f'))>0.0:
        positive=positive+1
    else:
        neutral=neutral+1

positive = 100 * positive/20
negative = 100 * negative/20
neutral = 100* neutral/20


labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]','Negative [' + str(negative) + '%]']
sizes = [positive,  neutral, negative]
colors = ['yellowgreen','gold','red']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title('How people are reacting on MODI by analyzing  20 Tweets.')
plt.axis('equal')
plt.tight_layout()
plt.show()

