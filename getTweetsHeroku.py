import tweepy
import json
import sys
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob 
import os, base64, re, logging
from elasticsearch import Elasticsearch

access_token = "95379124-oMzTvqi22DAXT1ME1HIKKvsdUJnkW6nCrK1QtBi0H"
access_token_secret = "5ABoRwhAJQGdlg7yaZbcLTvzbNYAQK8EAGjzHRl27pwp1"
consumer_key = "uRFTxTPfso3PJK8qfUhvZL9va"
consumer_secret = "7WLYa526I316f2jddfs14UrGM6rtLXfbHZKo2xEYwEqqxCbf8s"


# Log transport details (optional):
logging.basicConfig(level=logging.INFO)

# Parse the auth and host from env:
# bonsai = 'https://ej1hr91f:j84qb3g8x38stjt4@jasmine-7074319.us-east-1.bonsaisearch.net'
bonsai='https://12a754cb8ed901b20827cdcefffad337.us-east-1.aws.found.io:9243'
auth = re.search('https\:\/\/(.*)', bonsai).group(1).split(':')
host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

# Connect to cluster over SSL using auth for best security:
es_header = [{
  'host': host,
  'port': 443,
  'use_ssl': True,
  'http_auth': (auth[0],auth[1])
}]

# Instantiate the new Elasticsearch connection:
es = Elasticsearch(es_header)

# Verify that Python can talk to Bonsai (optional):
es.ping()



# es = Elasticsearch()

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
                # mappings={"test6": {
                #     "properties": {
                #                  "location": {
                #                     "type": "geo_point"
                #                              }
                #                           }
                #                 }
                #                   }
                # es.index(index="test6", doc_type="test6",body=mappings)                
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
                # print doc_body        
               
                es.index(index="twitter1", doc_type="tweets", body=doc_body,ignore=400)


        except Exception as e:
            print(e)


if __name__=='__main__':
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    print("Started listening to tweets...")
                
    twitterStream=Stream(auth,StreamListener())

    # coordinates covering the entire earth
    twitterStream.filter(locations=[-180,-90,180,90])  
