from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import networkx as nx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a graph for route calculations
G = nx.Graph()  # Mengubah graph menjadi undirected
G.add_weighted_edges_from([
    ("Tugu Jogja", "Stasiun Tugu", 1),
    ("Tugu Jogja", "UGM", 4),
    ("Tugu Jogja", "Malioboro", 2),
    ("Malioboro", "Tugu Jogja", 2),  # Tambahkan koneksi sebaliknya
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

# Model for route request
class RouteRequest(BaseModel):
    start: str
    end: str

# Model for chatbot request
class ChatbotRequest(BaseModel):
    user_input: str

# Endpoint for calculating the shortest route
@app.post("/api/route")
def get_route(request: RouteRequest):
    start = request.start
    end = request.end

    if start not in G.nodes or end not in G.nodes:
        raise HTTPException(status_code=400, detail="Invalid start or end location")

    try:
        path = nx.shortest_path(G, source=start, target=end, weight="weight")
        distance = nx.shortest_path_length(G, source=start, target=end, weight="weight")
        return {"route": path, "distance": distance}
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No path found between the locations")

# List of places
places = ["Tugu Jogja", "Stasiun Tugu", "Malioboro", "Keraton",
          "Alun-Alun Kidul", "UGM", "Monjali", "Bandara"]

# Function to parse user input
def parse_input(user_input):
    origin, destination = None, None
    user_input_lower = user_input.lower()

    # Prioritize matching with "dari" and "ke"
    for p in places:
        p_lower = p.lower()
        if f"dari {p_lower}" in user_input_lower:
            origin = p
        if f"ke {p_lower}" in user_input_lower:
            destination = p

    # If not found with "dari" and "ke", try matching just the place names
    if not origin and not destination:
        found = [p for p in places if p.lower() in user_input_lower]
        if len(found) >= 2:
            destination, origin = found[0], found[1]
        elif len(found) == 1:
            return None, None  # Indicate that both are not found

    # If one is found with keyword and the other is not, try to find the other without keyword
    if origin and not destination:
        found = [p for p in places if p.lower() in user_input_lower and p != origin]
        if found:
            destination = found[0]
    elif destination and not origin:
        found = [p for p in places if p.lower() in user_input_lower and p != destination]
        if found:
            origin = found[0]

    return origin, destination

# Function to find the shortest path
def find_shortest_path(graph, origin, destination):
    try:
        path = nx.dijkstra_path(graph, origin, destination, weight="weight")
        distance = nx.dijkstra_path_length(graph, origin, destination, weight="weight")
        return {"route": path, "distance": distance}
    except nx.NetworkXNoPath:
        return {"route": [], "distance": float("inf")}

# Endpoint for chatbot
@app.post("/chatbot")
def chatbot_endpoint(request: ChatbotRequest):
    user_input = request.user_input.lower()

    # Extract origin and destination from user input
    origin, destination = None, None
    for place in places:
        if f"dari {place.lower()}" in user_input:
            origin = place
        if f"ke {place.lower()}" in user_input:
            destination = place

    if not origin or not destination:
        return {"response": "Maaf, saya tidak mengenali lokasi asal atau tujuanmu. Mohon sebutkan dengan jelas."}

    if origin not in G.nodes or destination not in G.nodes:
        return {"response": f"Lokasi asal atau tujuan tidak valid: {origin}, {destination}"}

    try:
        path = nx.shortest_path(G, source=origin, target=destination, weight="weight")
        distance = nx.shortest_path_length(G, source=origin, target=destination, weight="weight")
        route_text = " → ".join(path)
        return {"response": f"Rute terpendek adalah {route_text} dengan total jarak {distance} km."}
    except nx.NetworkXNoPath:
        return {"response": f"Tidak ada rute antara {origin} dan {destination}."}