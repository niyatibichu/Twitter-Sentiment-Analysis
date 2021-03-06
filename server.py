import os, base64, re, logging
from flask import jsonify, request,Flask
from flask import render_template
from flask import Flask
from flask_elasticsearch import FlaskElasticsearch
from flask import jsonify
from elasticsearch import Elasticsearch
import certifi

# portnum=int(os.environ['PORT'])
# Log transport details (optional):
logging.basicConfig(level=logging.INFO)

# Parse the auth and host from env:
# bonsai = os.environ['BONSAI_URL']
# bonsai = "https://ej1hr91f:j84qb3g8x38stjt4@jasmine-7074319.us-east-1.bonsaisearch.net"
# auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
# host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

# Connect to cluster over SSL using auth for best security:
# es_header = [{
#   'host': host,
#   'port': 443,
#   'use_ssl': True,
#   'http_auth': (auth[0],auth[1])
# }]
#  ["*myaddress*.us-east-1.aws.found.io"],
#         port=9243,
#         http_auth="user:pass",
#         use_ssl=True,
#         verify_certs=True,
#         ca_certs=certifi.where()
# https://e869964a0826f7ed5b493155cbea3ac2.us-east-1.aws.found.io:9243/

app=Flask(__name__)
# app.config.update(
#     ELASTICSEARCH_HOST =host+':443'
# )
# es = FlaskElasticsearch(app)

es=Elasticsearch( ["https://e869964a0826f7ed5b493155cbea3ac2.us-east-1.aws.found.io:9243"],
        # port=9243,
        http_auth="elastic:nz0nxvrWuPkhZxwgnL09Cjpi",
        use_ssl=True,
        verify_certs=True,
        timeout=50,
        ca_certs=certifi.where())

es.ping()

# host = "http://localhost:9200"
indexName = "twitter1"

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/getdata",methods=['GET'])
def test():
    latitude=request.args.get('lat')
    longitude=request.args.get('lon') 
    radius=request.args.get('rad') 
    keyw=request.args.get('keyw')  
    # print(longitude)

    # elasticsearch query to get tweets
    query={"size": 250,  "sort" : [{ "created_at" : {"order" : "desc"}} ],"query": {"bool" : {"must" :[ {"match": { "text": keyw}},{"query_string" : {"query":"positive","fields":["sentiment"] }
            }],"filter" : {"geo_distance":{"distance":radius+'km',"location":[ float(latitude), float(longitude)]}}}}}

    # query={"query": {"bool":{"must":{"filter":{"query":{"geo_distance":{"distance":"10m","location":[ 40, -100]}}}}}}}
    print(query)
    results = es.search(index="twitter1", body=query)

    print("Number of results: ",results['hits']['total'])
    return jsonify(results['hits']['hits'])

if __name__=='__main__':
     app.run()

