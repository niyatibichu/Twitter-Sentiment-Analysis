import os
import tweepy
import json
import sys
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob 
from elasticsearch import Elasticsearch

access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")



es = Elasticsearch()

class StreamListener(tweepy.StreamListener): 
    def on_data(self, data):
        try:

            json_data = json.loads(data)
            if json_data.get('coordinates'):
                tweet = TextBlob(json_data["text"])
                # print tweet.sentiment.polarity

                if tweet.sentiment.polarity < 0:
                    sentiment = "negative"
                elif tweet.sentiment.polarity == 0:
                    sentiment = "neutral"
                else:
                    sentiment = "positive"

                               
                doc_body={
                                "ID":json_data["id"],
                                "text":json_data["text"],
                                "created_at":json_data["created_at"],
                                "longitude":json_data["coordinates"]["coordinates"][0],
                                "latitude":json_data["coordinates"]["coordinates"][1],
                                "sentiment":sentiment,
                                "polarity":tweet.sentiment.polarity,
                                "Country":json_data["place"]["country"],
                                "Country_Code":json_data["place"]["country_code"],
                                "Full_Name":json_data["place"].get('full_name'),
                                "Name":json_data["place"].get('name'),
                                "location":[json_data["coordinates"]["coordinates"][1],json_data["coordinates"]["coordinates"][0]],
                                "user":json_data["user"]
                            }   
  
                es.index(index="twitter1", doc_type="tweets", body=doc_body, ignore=400)
                # return True

        except Exception as e:
            print(e)


if __name__=='__main__':
    print("Started listening to tweets...")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    twitterStream=tweepy.Stream(auth,StreamListener())

    # coordinates covering the entire earth
    twitterStream.filter(locations=[-180,-90,180,90])  
