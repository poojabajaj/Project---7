
# coding: utf-8

# In[1]:


# Dependencies
import tweepy
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml


# In[2]:


TWITTER_CONFIG_FILE = 'auth.yaml'

with open(TWITTER_CONFIG_FILE, 'r') as config_file:
    config = yaml.load(config_file)
    
print(type(config))


# In[3]:


print(json.dumps(config, indent=4, sort_keys=True))


# In[4]:


access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']
consumer_key = config['twitter']['consumer_key']
consumer_secret = config['twitter']['consumer_secret']
print(access_token)
print(access_token_secret)
print(consumer_key)
print(consumer_secret)


# In[5]:


# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()


# In[6]:


# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


# In[7]:


# Add List to hold sentiment
compound_list = []
positive_list = []
negative_list = []
neutral_list = []

#creates a new dataframe that's empty
TweetDF = pd.DataFrame() 
#print(TweetDF)


# In[8]:


#target_user = "BBC"
Sentiment_list= []


# In[9]:


def newsmood(index, seq, target_user):
    public_tweets = api.user_timeline(id = target_user, count = 100, result_type = "recent")
    for tweet in public_tweets:
        # Run Vader Analysis on each tweet
        compound = analyzer.polarity_scores(tweet["text"])["compound"]
        pos = analyzer.polarity_scores(tweet["text"])["pos"]
        neu = analyzer.polarity_scores(tweet["text"])["neu"]
        neg = analyzer.polarity_scores(tweet["text"])["neg"]  
        #@TODO: YOUR CODE HERE
        compound_list.append(compound)
        positive_list.append(pos)
        negative_list.append(neg)
        neutral_list.append(neu)
        
        #Pull into a DataFrame the tweet's source acount, its text, its date, and its compound, positive, neutral, 
        #and negative sentiment scores.   
        # Get the specific column data
        #index = to_numeric(index)
        user_index= seq
        user_source = target_user
        user_text = tweet["text"]
        user_date = tweet["created_at"]
        user_comp = compound
        user_pos = pos
        user_neu = neu
        user_neg = neg
    
        # Replace the row information for each
        TweetDF.set_value(index, "Tweets ago",user_index)
        TweetDF.set_value(index, "Source", user_source)
        TweetDF.set_value(index, "Text", user_text)
        TweetDF.set_value(index, "Date", user_date)
        TweetDF.set_value(index, "Compound score", user_comp)
        TweetDF.set_value(index, "Positive score", user_pos)    
        TweetDF.set_value(index, "Neutral score", user_neu)   
        TweetDF.set_value(index, "Negative score", user_neg)   
 
        # Export the new CSV
        TweetDF.to_csv("Tweets.csv", index=False)
    
        #incrementating the index
        index = index+1   
        seq = seq+1
        
    Sentiment = {
        "Compound": compound_list,
        "Positive": positive_list,
        "Negative": negative_list,
        "Neutral": neutral_list
    }
     

    
    # View the DataFrame
    TweetDF.head()  
    
          
    
    Sentiment_list.append(Sentiment)
    return Sentiment_list 

#print(TweetDF)     
#print(type(public_tweets))
#print(type(public_tweets[0]))
#print(json.dumps(public_tweets[0], indent = 2))


# In[10]:


#Calling function definition on all major new outlets - BBC, CBS, CNN, Fox, and New York times
#int index
index=1
seq = 1
Sentiment_BBC= newsmood(index, seq, target_user="BBC")
Sentiment_CBS= newsmood(index+100, seq, target_user= "CBS")
Sentiment_CNN= newsmood(index+200, seq, target_user= "CNN")
Sentiment_FOX= newsmood(index+300, seq, target_user= "FOX")
Sentiment_NYTIMES= newsmood(index+400, seq, target_user= "nytimes")

#print(Sentiment_BBC)
#print("-----------------------------------------------------------------------------------------------------------")
#print(Sentiment_CBS)
#print("-----------------------------------------------------------------------------------------------------------")
#print(Sentiment_CNN)
#print("-----------------------------------------------------------------------------------------------------------")
#print(Sentiment_FOX)
#print("-----------------------------------------------------------------------------------------------------------")
#print(Sentiment_NYTIMES)


# In[11]:


print(TweetDF)


# In[12]:


#create dataframes based on the source
TweetDF_BBC = TweetDF.loc[(TweetDF["Source"] =="BBC")]
TweetDF_CBS = TweetDF.loc[(TweetDF["Source"] =="CBS")]
TweetDF_CNN = TweetDF.loc[(TweetDF["Source"] =="CNN")]
TweetDF_FOX = TweetDF.loc[(TweetDF["Source"] =="FOX")]
TweetDF_NYTIMES = TweetDF.loc[(TweetDF["Source"] =="nytimes")]


# In[13]:


print(TweetDF_NYTIMES)
#colors = ("LightBlue", "Green", "Red", "DarkBlue", "Yellow")
#print(x_axis)
#print(y_axis)


# In[14]:


def CreateGraph(df, source, graphcolor):
    
    #creating x axis and y axis variables
    x_axis = df["Tweets ago"]
    y_axis = df["Compound score"]

    #Scatterplot tweet polarity vs timestamp
    #TweetDF.plot(kind= "scatter", x= x_axis, y= y_axis, grid= True, figsize= (10,5), title = "Sentiment Analysis of media tweets (07/07/2018)")
    legend_handle = plt.scatter(x_axis, y_axis, color = graphcolor, label = source)
    #print(legend_handles)
    #fig = plt.figure()
    #fig.set_facecolor('Gray')
    
    plt.xlabel("Tweets ago")
    plt.ylabel("Tweet Polarity")
    plt.title("Sentiment Analysis of media tweets (07/07/2018)")
    
    # creating labels using mpatches
    #BBC_patch = mpatches.Patch(color='LightBlue', label='BBC')
    #CBS_patch = mpatches.Patch(color='Green', label='CBS')
    #CNN_patch = mpatches.Patch(color='Red', label='CNN')
    #FOX_patch = mpatches.Patch(color='DarkBlue', label='FOX')
    #NYTIMES_patch = mpatches.Patch(color='Yellow', label='NYTIMES')
    
    #plt.legend(handles=[BBC_patch])
    #plt.legend(handles=[CBS_patch])
    #plt.legend(handles=[CNN_patch])
    #plt.legend(handles=[FOX_patch])
    #plt.legend(handles=[NYTIMES_patch])
    plt.grid()
    return legend_handle
    


# In[15]:


Graph_BBC= CreateGraph(TweetDF_BBC, "BBC", "LightBlue")
Graph_CBS= CreateGraph(TweetDF_CBS, "CBS", "Green")
Graph_CNN= CreateGraph(TweetDF_CNN, "CNN", "Red")
Graph_FOX= CreateGraph(TweetDF_FOX, "FOX", "DarkBlue")
Graph_NYTIMES= CreateGraph(TweetDF_NYTIMES, "NYTIMES", "Yellow")


# In[16]:


#adding xlimit and y limit
plt.xlim(-10,150)
plt.ylim(-1, 1)


# In[17]:


# Adds a legend and sets its location to the lower right
list_handles = [Graph_BBC, Graph_CBS, Graph_CNN, Graph_FOX, Graph_NYTIMES]
plt.legend(handles=list_handles, loc="upper right")


# In[18]:


#plt.set_axis_bgcolor("lightslategray")
plt.savefig("Output_tweet_charts/Sentiment_Analysis_of_Media_Tweets.png")
plt.show()


# In[19]:


def CreateMean(df):
    y = df["Compound score"].mean()
    return y
   


# In[20]:


y_axis = []
for df in (TweetDF_BBC, TweetDF_CBS, TweetDF_CNN, TweetDF_FOX, TweetDF_NYTIMES):
    y_axis.append(CreateMean(df))
#print(type(y_axis))
#print(y_axis)


# In[21]:


source = ('BBC', 'CBS', 'CNN', 'FOX', 'NYTIMES')
x_axis = np.arange(5)


#for rect in bar1:
#    height = rect.get_height()
#    plt.text(((rect.get_x() + rect.get_width())/2.0), height, '%d' % height, ha='center', va='bottom')

fig, ax = plt.subplots()
for i, v in enumerate(y_axis,-1):
    if v>=0:
        ax.text(i+0.8, v+0.025, str(round(v,2)), color='black')
    else:
        ax.text(i+0.8, v-0.025, str(round(v,2)), color='black')
    
bar1= ax.bar(x_axis, y_axis, width = 1, align='center', alpha = 1)
BBC, CBS, CNN, FOX, NYTIMES = bar1

#Setting colors for each bar in bar chart
BBC.set_facecolor('LightBlue')
CBS.set_facecolor('Green')
CNN.set_facecolor('Red')
FOX.set_facecolor('DarkBlue')
NYTIMES.set_facecolor('Yellow')

plt.xticks(x_axis, source)
plt.ylabel('Tweet Polarity')
plt.title('Overall Media Sentiment Based On Twitter(01/07/2017)')
plt.xlim(-1,5)
plt.ylim(-0.2, 0.5)
plt.axhline(y=0, color = 'black', linestyle='-', linewidth = 0.8)
plt.tight_layout()


# In[22]:


plt.savefig("Output_tweet_charts/Overall_Media_Sentiment_Based_On_Twitter.png")
plt.show()


# In[23]:


#Conclusions:
#Looking at Sentiment analysis - 
#BBC seems to have moderately positive and negative sentiments expressed in the tweets.
#CBS has highly positive sentiments in tweets with a very few exception of moderately negative tweets.
#CNN has moderately positive sentiments but highly negative sentiments expressed.
#Fox is all over the map, with moderate as well as as highly positive and negative sentiments in the tweets.
#NYTIMES has highly negative tweets, a good # of neither positive nor negative tweets and some moderately positive tweets.

#overall sentiment polarity
#BBC - with a low but positive overall score
#CBS - with a good positive score, highest among the 5 channels analyzed here
#CNN - with a low but overall negative score
#Fox - with a minor but overall positive score
#NYTIMES - with a moderately negative and most negtaive overall score among the 5 channels analyzed here 

