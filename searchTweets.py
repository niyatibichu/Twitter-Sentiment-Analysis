import urllib3
urllib3.disable_warnings()
import json
import sys
from textblob import TextBlob 
from elasticsearch import Elasticsearch

es = Elasticsearch()

# mappings = {
#     "test4": {
#         "properties": {
#                      "location": {
#                          "type": "geo_point"
#                      }
#                  }
#              }
#         }
  
# es.index(index='location',doc_type="test4", body=mappings)


es_entries['location'] =[ data['latitude'],data['longitude']]
# es_entries['location'] = [data['latitude'],data['longitude']]}
# # ...
es.index(index="location", doc_type="test4", body=es_entries)

# search_body={"settings":{"index":{"analysis":{"query": {"filtered":{ 
# "filter":{"geo_distance":{"distance":"10m", "location": [44.865243, -93.4094629 ]}}}}}}},
# "mappings":{ "doc": {"properties": { "location": { "type": "geo_point"  }}} }}


# es.search(index='test4', body=search_body)
# print("Got %d Hits:" % res['hits']['total'])


# res=es.search(index="test1", body={"query": {"filtered":{ "query": {"match_all" : { }},"filter":{"geo_distance":{"distance":"100m", "coordinates": {"latitude": 51.512497,"longitude": -0.052098 }}}}}})
# search_body={"query": {"filtered":{"filter":{"geo_distance":{"distance" :"100m","location":[44.865243,-93.4094629]}}}}, "mappings": { "doc": {"properties": {"geo": {"properties": {"location": { "type": "geo_point" } } } } } } } 

# # search_body={"query": {"query_string" : {"query":"positive","fields":["sentiment"]}}}

# res=es.search(index="test4",body=search_body)
# print("Got %d Hits:" % res['hits']['total'])