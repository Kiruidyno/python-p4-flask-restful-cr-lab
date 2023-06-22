#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        return make_response([plant.to_dict() for plant in Plant.query.all()], 200)
    def post(self):
        new_record = Plant(
            name = request.get_json()['name'],
            image = request.get_json()['image'],
            price = request.get_json()['price']
        )
        db.session.add(new_record)
        db.session.commit()
        return make_response(new_record.to_dict(), 201)
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter(Plant.id == id).first()
        if plant:
            return make_response(plant.to_dict(), 200)
        else:
            return make_response("Plant not found", 404)

api.add_resource(PlantByID, '/plants/<int:id>')

        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
