# mapping.py creates a mapping for the tweets collection
from elasticsearch import Elasticsearch

es = Elasticsearch()

mappings={  
   "settings":{  
       "index" : {
            "number_of_shards" : 3,
            "number_of_replicas" : 2
        }
   },
   "mappings":{  
      "tweets":{  
         "properties":{  
            "location":{  
               "type":"geo_point"
            },
             "created_at": {
                "type":   "date",
                "format": "EEE MMM dd HH:mm:ss Z YYYY"
        }
         }
      }
   }
}

es.indices.create(index="twitter1",body=mappings)
print ("Mapping Complete")
              
