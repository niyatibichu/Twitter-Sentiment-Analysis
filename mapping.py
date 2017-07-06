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
      "test6":{  
         "properties":{  
            "location":{  
               "type":"geo_point"
            }
         }
      }
   }
}

es.indices.create(index="test6",body=mappings)
print "mapping done"
              
