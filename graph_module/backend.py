from fastapi import FastAPI
from pydantic import BaseModel
import networkx as nx

app = FastAPI()

# Define the graph
G = nx.Graph()
edges = [
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
    ("Monjali", "Bandara", 8)
]
G.add_weighted_edges_from(edges)

# Input model for shortest path
class ShortestPathInput(BaseModel):
    origin: str
    destination: str

@app.post("/shortest-path")
def get_shortest_path(input: ShortestPathInput):
    try:
        path = nx.dijkstra_path(G, input.origin, input.destination, weight="weight")
        distance = nx.dijkstra_path_length(G, input.origin, input.destination, weight="weight")
        return {"route": path, "distance": distance}
    except nx.NetworkXNoPath:
        return {"error": f"Tidak ada rute antara {input.origin} dan {input.destination}."}
    except nx.NodeNotFound:
        return {"error": f"Lokasi asal atau tujuan tidak ditemukan di graf."}

@app.get("/")
def read_root():
    return {"message": "FastAPI backend for shortest path is running!"}