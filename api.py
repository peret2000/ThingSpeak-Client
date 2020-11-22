# Simple API for Heroku deployment

from flask import Flask, jsonify, request,send_file
from flask_restful import Resource, Api,reqparse
from flask_cors import CORS
import pvcalc
from zipfile import ZipFile

app = Flask(__name__)
CORS(app)
api = Api(app)

'''     
 TODO: 
  - Flesh out the api 
   - Take more input fields (e.g. Start date and End Date)
   - Allow to download csvs directly
'''

class HelloWorld(Resource):
    def get(self):
        return jsonify(pvcalc.calc_energy());

'''
Download api params: 
    1. Start date 
    2. End Date 
'''

class Download(Resource): 
    def get(self): 
        parser = reqparse.RequestParser()
        parser.add_argument('start', type=str)
        parser.add_argument('end', type=str)
        args = parser.parse_args()
        # grab data 
        pvcalc.get_csv(args)
        # create zip archieve
        return send_file('./data.zip', as_attachment=True, attachment_filename='tsdata.zip')



api.add_resource(HelloWorld, '/')
api.add_resource(Download, '/download', endpoint='download');

if __name__ == '__main__':
    app.run(debug=False)
