# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(jsonify(body), 200)

@app.route('/earthquakes/<int:id>')
def index2(id):
    quake = Earthquake.query.get(id)

    if quake:
        return jsonify(quake.to_dict()), 200
    else:
        message = {'message': f'Earthquake {id} not found.'}
        return jsonify(message), 404

@app.route('/earthquakes/magnitude/<float:magnitude>')
def magnitude_route(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    quake_list = []
    for quake in quakes:
        quake_list.append({
            'id': quake.id,
            'location': quake.location,
            'magnitude': quake.magnitude,
            'year': quake.year
        })

    response_data = {
        'count': len(quake_list),
        'quakes': quake_list
    }

    return jsonify(response_data), 200
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)