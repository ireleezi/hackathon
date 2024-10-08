from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__)

# Path to the static directory
STATIC_DIR = os.path.join(os.getcwd(), 'static')

# Example map generation function (replace this with your actual function)
def generate_tree_density_map(output_file_path):
    # Call your actual tree density map generation function here
    # For example:
    # generate_tree_density_map(...)

    # Simulate map generation and save it as an HTML file
    with open(output_file_path, 'w') as f:
        f.write("<html><body><h1>Map generated!</h1></body></html>")

@app.route('/generate-map', methods=['POST'])
def generate_map():
    # Get input data from frontend (if needed)
    data = request.json

    # Path to save the generated map inside the 'static' directory
    map_file_name = 'belfast_greenery_map.html'
    map_file_path = os.path.join(STATIC_DIR, map_file_name)

    # Call the function to generate the map and save it in the static directory
    generate_tree_density_map(map_file_path)

    # Return the URL/path to the generated map, which will be served via the static route
    return jsonify({'map_url': f'/static/{map_file_name}'})

# Serve static files from the 'static' folder
@app.route('/static/<path:filename>')
def serve_static_file(filename):
    return send_from_directory(STATIC_DIR, filename)

if __name__ == "__main__":
    # Ensure the static directory exists
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    app.run(debug=True)
