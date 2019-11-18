from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import pvcalc

app = Flask(__name__)
CORS(app)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return jsonify(pvcalc.calc_energy()); 

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=False)