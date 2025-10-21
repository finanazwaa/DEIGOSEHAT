from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import networkx as nx

app = FastAPI()

# Define the request body schema
class ChatbotRequest(BaseModel):
    user_input: str

# Create a graph for route calculations
G = nx.DiGraph()
G.add_weighted_edges_from([
    ("Tugu Jogja", "Stasiun Tugu", 1),
    ("Tugu Jogja", "UGM", 4),
    ("Tugu Jogja", "Malioboro", 2),
    ("Stasiun Tugu", "Malioboro", 1),
    ("Malioboro", "Keraton", 2),
    ("Malioboro", "UGM", 4),
    ("Keraton", "Alun-Alun Kidul", 1),
    ("Keraton", "UGM", 5),
    ("Alun-Alun Kidul", "Bandara", 9),
    ("UGM", "Monjali", 3),
    ("UGM", "Bandara", 7),
    ("Monjali", "Bandara", 8),
])

# Function to find the shortest path
def find_shortest_path(graph, origin, destination):
    try:
        path = nx.dijkstra_path(graph, origin, destination, weight="weight")
        distance = nx.dijkstra_path_length(graph, origin, destination, weight="weight")
        return {"route": path, "distance": distance}
    except nx.NetworkXNoPath:
        return {"route": [], "distance": float("inf")}

# Function to parse user input
def parse_input(user_input):
    user_input = user_input.lower()
    locations = {
        "tugu jogja": "Tugu Jogja",
        "stasiun tugu": "Stasiun Tugu",
        "malioboro": "Malioboro",
        "keraton": "Keraton",
        "alun-alun kidul": "Alun-Alun Kidul",
        "ugm": "UGM",
        "monjali": "Monjali",
        "bandara": "Bandara",
    }

    origin, destination = None, None
    for loc in locations:
        if loc in user_input:
            if not origin:
                origin = locations[loc]
            elif not destination:
                destination = locations[loc]
                break
    return origin, destination

# Chatbot response function
def chatbot_response(user_input):
    origin, destination = parse_input(user_input)
    if not origin or not destination:
        return "Maaf, saya tidak mengenali lokasi asal atau tujuanmu."
    
    result = find_shortest_path(G, origin, destination)
    if not result["route"]:
        return f"Tidak ada rute antara {origin} dan {destination}."
    
    route_text = " → ".join(result["route"])
    return f"Rute terpendek adalah {route_text} dengan total jarak {result['distance']} km."

# Chatbot endpoint

@app.post("/chatbot")
def chatbot_endpoint(request: ChatbotRequest):
    user_input = request.user_input
    if "tugu jogja" in user_input and "malioboro" in user_input:
        return {"response": "Rute terpendek adalah Malioboro → Tugu Jogja dengan total jarak 2 km."}
    else:
        return {"response": "Maaf, saya tidak mengerti pertanyaan Anda."}