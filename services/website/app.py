from flask import Flask, render_template, jsonify, request, abort
import os
app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template('index.html')

@app.route("/searchflight", methods = ["POST"])
def searchflights():
    print("test1")
    if request.method == "POST":
        print("test2")
        value = request.get_json()
        print(value)
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


#@app.route("/listing",methods = ['GET'])
#def listing():
#    if request.method == 'GET':
#        list ={'listelements': [{'string':'first element', "number":1},{"string": 'fifth element',"number":5},{"string": 'twentyfirst',"number":21}]}
#        return jsonify(list)


@app.route("/teapot")
def teapot():
    return abort(418)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
