from fastapi import FastAPI
import networkx as nx

app = FastAPI()

# Initialize the FastAPI application

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}

@app.post("/shortest-path")
def get_shortest_path(origin: str, destination: str):
    # Example logic for shortest path
    return {"route": ["Tugu Jogja", "Malioboro", "UGM"], "distance": 6}

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

print("Data edges berhasil dibuat.")

import json

with open("graph_data.json", "w") as f:
    json.dump(edges, f)

print("Data edges berhasil disimpan ke dalam file graph_data.json")
G = nx.Graph()

for src, dest, dist in edges:
    G.add_edge(src, dest, weight=dist)

print("Total Nodes:", G.number_of_nodes())
print("Total Edges:", G.number_of_edges())

nx.is_connected(G)
list(G.nodes)

for u, v, d in G.edges(data=True):
    print(f"{u} ↔ {v} = {d['weight']} km")

origin = input("Masukkan lokasi awal (origin): ")
destination = input("Masukkan lokasi tujuan (destination): ")

try:
    path = nx.dijkstra_path(G, origin, destination, weight='weight')
    distance = nx.dijkstra_path_length(G, origin, destination, weight='weight')
except nx.NetworkXNoPath:
    path = None
    distance = None
except nx.NodeNotFound as e:
    print(f"Error: Node tidak ditemukan: {e}")
    path = None
    distance = None

    if path:
        print("Rute:", " → ".join(path))
        print("Total jarak:", distance, "km")
else:
    print("Tidak ada rute yang ditemukan antara", origin, "dan", destination)