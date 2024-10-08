import random

from flask import Flask, jsonify, send_file, request

from hackathon.GreenThumBotPollutionGuide import generate_pollution_tree_map
from hackathon.GreenThumBotTreeGuide import generateMap
from utils import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # this is very bad code and kinda dangerous but fuck it - it works


@app.route('/greening/locations', methods=['GET'])
def get_greening_locations() -> jsonify:
    df = fetch_onidata()
    if df is not None:
        processed_data = process_data(df)
        return jsonify(processed_data), 200
    return jsonify({'Error': "Cant fetch data"}), 500


@app.route('/generate-map')
def generate_map():
    map_param = request.args.get('param', type=int)
    # Use default value if no value is given
    if map_param is None:
        map_param = 10
    # Call the generateMap function to create the map
    map_path = generateMap(map_param)
    # Serve the generated HTML map file
    return send_file(map_path)


@app.route('/dashboard-data', methods=['GET'])
def get_dashboard_data():
    # Replace this with real data logic, for now it is just a mock response
    data = {
        "total_trees": random.randint(1, 100000),
        "pollution_level": random.randint(1, 100000),
        "greening_areas": random.randint(1, 100000),
        "water_bodies_count": random.randint(1, 100000),
        "plots": random.randint(1, 100000)
    }
    return jsonify(data), 200

@app.route('/generate-pollution-map')
def generate_pollution_map():
    # map_param = request.args.get('param', type=int)
    # if map_param is None:
    #     return jsonify({'error': 'Parameter is required'}), 400
    # Call the generateMap function to create the map
    map_path = generate_pollution_tree_map()
    # Serve the generated HTML map file
    return send_file(map_path)

if __name__ == '__main__':
    app.run(debug=True)
