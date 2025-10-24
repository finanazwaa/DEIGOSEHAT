import networkx as nx
import json

# Buat graph dari data edge
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

print("✅ Data edges berhasil dibuat.")

# Simpan ke file JSON
with open("graph_data.json", "w") as f:
    json.dump(edges, f)

print("✅ Data edges berhasil disimpan ke dalam file graph_data.json")

# Bangun graf dari edges
G = nx.Graph()
for src, dest, dist in edges:
    G.add_edge(src, dest, weight=dist)

print(f"Total Nodes: {G.number_of_nodes()}")
print(f"Total Edges: {G.number_of_edges()}")
for u, v, d in G.edges(data=True):
    print(f"{u} ↔ {v} = {d['weight']} km")


# ✅ Fungsi utama yang akan dipanggil Flask backend
def find_shortest_path(start, end):
    try:
        path = nx.dijkstra_path(G, start, end, weight='weight')
        distance = nx.dijkstra_path_length(G, start, end, weight='weight')
        return {
            "route": path,
            "distance": distance
        }
    except nx.NodeNotFound as e:
        return {"error": f"Node tidak ditemukan: {e}"}
    except nx.NetworkXNoPath:
        return {"error": f"Tidak ada rute antara {start} dan {end}"}
