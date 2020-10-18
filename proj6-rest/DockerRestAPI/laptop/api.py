# Laptop Service

from flask import Flask, request, Response
from flask_restful import Resource, Api
from pymongo import MongoClient
import pymongo
import os
import csv
import flask
import json
# Instantiate the app
app = Flask(__name__)
api = Api(app)
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.tododb

class list_all(Resource):
    def get(self):

        openT = []
        closeT = []

        temp = request.args.get('top')
        if temp != None:
            top = int(temp)
            _items = db.tododb.find().limit(top)
        else:
            _items = db.tododb.find()

        items = [item for item in _items]
        
        for i in items:
            openT.append(i['opening'])
            closeT.append(i['closing'])

        results = {'opening':openT, 'closing':closeT}
#        return flask.jsonify(result= results)
        return results

class openOnly_json(Resource):
    def get(self):
        openT = []
        temp = request.args.get('top')
        if temp != None:
            top = int(temp)
            _items = db.tododb.find().limit(top)
        else:
            _items = db.tododb.find()

        items = [item for item in _items]

        for i in items:
            openT.append(i['opening'])
        results = {'open_times':openT}
        return results

class closeOnly_json(Resource):
    def get(self):
        closeT = []
        temp = request.args.get('top')
        if temp != None:
            top = int(temp)
            _items = db.tododb.find().limit(top)
        else:
            _items = db.tododb.find()

        items = [item for item in _items]

        for i in items:
            closeT.append(i['closing'])

        results = {'close_times':closeT}
        return results

class list_all_csv(Resource):
    def get(self):

        fileI = open('list.csv', 'w')
        fileO = csv.writer(fileI)
        temp = request.args.get('top')

        if temp != None:
            top = int(temp)
            _items = db.tododb.find().limit(top)

        else:
            _items = db.tododb.find()

        items = [item for item in _items]
        fileO.writerow(['km\t'+'Open Time\t'+ 'Close Time'])
        for i in items:
            fileO.writerow([i['kming']+ '\t' + i['opening'] + '\t' + i['closing']])

        fileR = open('list.csv', 'r')
        return Response(fileR, mimetype='text/csv' )

class openOnly_csv(Resource):
    def get(self):

        fileI = open('list.csv', 'w')
        fileO = csv.writer(fileI)
        temp = request.args.get('top')

        if temp != None:
            top = int(temp)
            _items = db.tododb.find().limit(top)

        else:
            _items = db.tododb.find()

        items = [item for item in _items]
        fileO.writerow(['km\t'+'Open Time\t'])
        for i in items:
            fileO.writerow([i['kming']+ '\t' + i['opening']])

        fileR = open('list.csv', 'r')
        return Response(fileR, mimetype='text/csv' )

class closeOnly_csv(Resource):
    def get(self):

        fileI = open('list.csv', 'w')
        fileO = csv.writer(fileI)
        temp = request.args.get('top')

        if temp != None:
            top = int(temp)
            _items = db.tododb.find().limit(top)

        else:
            _items = db.tododb.find()

        items = [item for item in _items]
        fileO.writerow(['km\t'+ 'Close Time'])
        for i in items:
            fileO.writerow([i['kming']+ '\t' + i['closing']])

        fileR = open('list.csv', 'r')
        return Response(fileR, mimetype='text/csv' )

api.add_resource(openOnly_json, '/listOpenOnly','/listOpenOnly/json')
api.add_resource(list_all, '/listAll','/listAll/json')
api.add_resource(closeOnly_json, '/listCloseOnly','/listCloseOnly/json')
api.add_resource(list_all_csv, '/listAll/csv')
api.add_resource(openOnly_csv,'/listOpenOnly/csv')
api.add_resource(closeOnly_csv,'/listCloseOnly/csv')
# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
