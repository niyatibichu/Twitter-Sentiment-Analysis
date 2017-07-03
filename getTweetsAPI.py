import tweepy
import json
import sys
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob 
from elasticsearch import Elasticsearch

access_token = "95379124-oMzTvqi22DAXT1ME1HIKKvsdUJnkW6nCrK1QtBi0H"
access_token_secret = "5ABoRwhAJQGdlg7yaZbcLTvzbNYAQK8EAGjzHRl27pwp1"
consumer_key = "uRFTxTPfso3PJK8qfUhvZL9va"
consumer_secret = "7WLYa526I316f2jddfs14UrGM6rtLXfbHZKo2xEYwEqqxCbf8s"

es = Elasticsearch()

class StreamListener(tweepy.StreamListener): 
    
    # def __init__(self):
    #     # print("Initialising instance...")
    #     self.count=0
        
    def on_data(self, data):
        
        try:
            json_data = json.loads(data);
            if json_data.get('coordinates'):
                
                tweet = TextBlob(json_data["text"])
                # print tweet.sentiment.polarity

                if tweet.sentiment.polarity < 0:
                    sentiment = "negative"
                elif tweet.sentiment.polarity == 0:
                    sentiment = "neutral"
                else:
                    sentiment = "positive"

                # print sentiment
                #json_data["sentiment"]=sentiment
                # print "Text: "+ json_data["text"].encode("utf-8")
                # print json_data["created_at"]
                # self.count+=1
                # print "Coordinates: ",json_data["coordinates"].get('coordinates')
                # print "Country: ",json_data["place"]["country"]
                # print "Country_Code: ", json_data["place"]["country_code"]
                # print "Full_Name: ",json_data["place"].get('full_name')
                # print "Name: ",json_data["place"].get('name') 
                # if self.count%1000==0:
                #     print "Created AT: "+json_data.get("created_at")
                #     print self.count
                #     print "--------------------------------------------------"           

                es.index(index="test2",
                        doc_type="test2",
                        body={
                            "ID":json_data["id"],
                            "text":json_data["text"],
                            "date":json_data["created_at"],
                            "longitude":json_data["coordinates"]["coordinates"][0],
                            "latitude":json_data["coordinates"]["coordinates"][1],
                            "sentiment":sentiment,
                            "polarity":tweet.sentiment.polarity,
                            "Country":json_data["place"]["country"],
                            "Country_Code":json_data["place"]["country_code"],
                            "Full_Name":json_data["place"].get('full_name'),
                            "Name":json_data["place"].get('name')

                        }
                        )

        except Exception, e:
            print e


if __name__=='__main__':
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    print "Started listening to tweets..."
                
    twitterStream=Stream(auth,StreamListener())

    twitterStream.filter(locations=[-180,-90,180,90])  
