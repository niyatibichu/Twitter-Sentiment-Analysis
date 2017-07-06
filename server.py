from flask import jsonify, request,Flask
from flask import render_template
from flask import Flask
from flask_elasticsearch import FlaskElasticsearch
app=Flask(__name__)
es = FlaskElasticsearch(app)

host = "http://localhost:9200"
indexName = "test6"

@app.route("/")
def root():
    return render_template('index.html')

@app.route('/getdata',methods=['GET'])
def test():
    latitude=request.args.get('lat')
    longitude=request.args.get('lon') 
    radius=request.args.get('rad')   
    # print longitude

    # elasticsearch query to get  tweets
    query={"query": {"bool" : {"must" : {"query_string" : {"query":"neutral","fields":["sentiment"] }
            },"filter" : {"geo_distance":{"distance":radius.encode("utf-8")+'m',"location":[ float(latitude.encode("utf-8")), float(longitude.encode("utf-8"))]}}}}}

    # query={"query": {"bool":{"must":{"filter":{"query":{"geo_distance":{"distance":"10m","location":[ 40, -100]}}}}}}}
    print query
    results = es.search(index="test6", body=query)
    print "Number of results: ",results
    return results

if __name__=='__main__':
     app.run(debug=True,port=8080)

