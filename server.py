from flask import jsonify, request,Flask
from flask import render_template
from flask import Flask
from flask_elasticsearch import FlaskElasticsearch
from flask import jsonify
app=Flask(__name__)
es = FlaskElasticsearch(app)

host = "http://localhost:9200"
indexName = "twitter1"

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route('/getdata',methods=['GET'])
def test():
    latitude=request.args.get('lat')
    longitude=request.args.get('lon') 
    radius=request.args.get('rad')   
    # print longitude

    # elasticsearch query to get tweets
    query={"size": 250,  "sort" : [{ "created_at" : {"order" : "desc"}} ],"query": {"bool" : {"must" : {"query_string" : {"query":"positive","fields":["sentiment"] }
            },"filter" : {"geo_distance":{"distance":radius.encode("utf-8")+'km',"location":[ float(latitude.encode("utf-8")), float(longitude.encode("utf-8"))]}}}}}

    # query={"query": {"bool":{"must":{"filter":{"query":{"geo_distance":{"distance":"10m","location":[ 40, -100]}}}}}}}
    print query
    results = es.search(index="twitter1", body=query)

    print "Number of results: ",results['hits']['total']
    return jsonify(results['hits']['hits'])

if __name__=='__main__':
     app.run(debug=True,port=8080)

