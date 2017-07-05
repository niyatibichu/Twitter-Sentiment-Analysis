from flask import jsonify, request,Flask
from flask import render_template
app=Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')

@app.route('/getdata',methods=['GET'])
def test():
    latitude=request.args.get('lat')
    longitude=request.args.get('long') 
    radius=request.args.get('rad')   
    print latitude," ",longitude," ",radius
    return latitude
    


if __name__=='__main__':
     app.run(debug=True,port=8080)

