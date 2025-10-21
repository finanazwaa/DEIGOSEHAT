from flask import Flask, request, jsonify
from flask_cors import CORS
from graph_module import find_shortest_path  # Import the shortest path function

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Endpoint for route calculation
@app.route('/api/route', methods=['POST'])
def get_route():
    print("Received request on /api/route")  # Debugging log
    data = request.json
    start = data.get('start')
    end = data.get('end')

    if not start or not end:
        print("Missing start or end in request")  # Debugging log
        return jsonify({'error': 'start and end required'}), 400

    # Calculate the shortest path
    result = find_shortest_path(start, end)
    print(f"Calculated route: {result}")  # Debugging log
    return jsonify(result)

# Endpoint for chatbot
@app.post("/chatbot")
def chatbot_endpoint(request: ChatbotRequest):
    user_input = request.user_input
    origin, destination = parse_input(user_input)

    if not origin or not destination:
        return {"response": "Maaf, saya tidak mengenali lokasi asal atau tujuanmu. Mohon sebutkan dengan jelas."}

    result = find_shortest_path(G, origin, destination)
    if not result["route"]:
        return {"response": f"Tidak ada rute antara {origin} dan {destination}."}

    route_text = " → ".join(result["route"])
    return {"response": f"Rute terpendek adalah {route_text} dengan total jarak {result['distance']} km."}

if __name__ == '__main__':
    print("Starting Flask server...")  # Debugging log
    app.run(debug=True)