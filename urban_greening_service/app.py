from flask import Flask, jsonify
from utils import *

app = Flask(__name__)

@app.route('/greening/locations', methods=['GET'])
def get_greening_locations() -> jsonify:
    df = fetch_onidata()
    if df is not None:
        processed_data = process_data(df)
        return jsonify(processed_data), 200
    return jsonify({'Error': "Cant fetch data"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)