import networkx as nx
import re

# =======================
# 🔹 GRAPH DATA
# =======================
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

# Bangun graf
G = nx.Graph()
for src, dest, dist in edges:
    G.add_edge(src.lower(), dest.lower(), weight=dist)  # ubah jadi lowercase semua

# Mapping alias biar fleksibel
aliases = {
    "ugm": "ugm",
    "kampus ugm": "ugm",
    "universitas gadjah mada": "ugm",
    "tugu": "tugu jogja",
    "tugu jogja": "tugu jogja",
    "monjali": "monjali",
    "malioboro": "malioboro",
    "stasiun tugu": "stasiun tugu",
    "keraton": "keraton",
    "alun alun kidul": "alun-alun kidul",
    "alun-alun kidul": "alun-alun kidul",
    "bandara": "bandara",
}


# =======================
# 🔹 Fungsi Shortest Path
# =======================
def find_shortest_path(start, end):
    try:
        path = nx.dijkstra_path(G, start, end, weight="weight")
        distance = nx.dijkstra_path_length(G, start, end, weight="weight")
        return {"route": path, "distance": distance}
    except nx.NodeNotFound:
        return {"error": f"⚠️ Saya tidak mengenali destinasi tersebut. Coba sebutkan dua lokasi."}
    except nx.NetworkXNoPath:
        return {"error": f"⚠️ Tidak ada rute antara {start.title()} dan {end.title()}."}


# =======================
# 🔹 Chatbot Utama
# =======================
def get_response(user_input):
    """Chatbot sederhana untuk sapaan + perhitungan rute."""
    user_input = user_input.lower().strip()

    # Respons umum
    if user_input == "" or user_input in ["hai", "halo", "hey"]:
        return "Halo! 👋 Aku asisten rute Jogja kamu. Coba ketik 'dari UGM ke Bandara' untuk cari jalur tercepat!"
    elif "tugu" in user_input and "dari" not in user_input:
        return "Kamu mau ke Tugu Jogja ya?"
    elif "terima kasih" in user_input:
        return "Sama-sama! Senang bisa membantu 😊"
    elif "apa kabar" in user_input:
        return "Aku baik-baik aja! Siap bantu kamu cari rute hari ini 😄"

    # Deteksi format: "dari [A] ke [B]"
    match = re.search(r"dari\s+([\w\s\-]+)\s+ke\s+([\w\s\-]+)", user_input)
    if match:
        start_raw = match.group(1).strip()
        end_raw = match.group(2).strip()

        # Coba cocokin dengan alias
        start = aliases.get(start_raw, start_raw.lower())
        end = aliases.get(end_raw, end_raw.lower())

        result = find_shortest_path(start, end)
        if "error" in result:
            return result["error"]

        route = " → ".join([loc.title() for loc in result["route"]])
        return f"🚗 Rute tercepat dari {start_raw.title()} ke {end_raw.title()} adalah:\n{route}\n🛣️ Jarak total: {result['distance']} km"

    # Kalau input tidak dikenali
    return "Maaf, aku belum paham maksudmu 😅. Coba ketik 'dari UGM ke Bandara' untuk contoh perhitungan rute!"
