import streamlit as st
import requests

st.title("🗺️ Shortest Path Finder - Yogyakarta")

# Input fields for origin and destination
origin = st.text_input("Masukkan lokasi asal (contoh: Tugu Jogja):")
destination = st.text_input("Masukkan lokasi tujuan (contoh: UGM):")

# Function to send user input to the FastAPI backend
def get_shortest_path(origin, destination):
    url = "http://127.0.0.1:8000/shortest-path"  # FastAPI backend URL
    response = requests.post(url, json={"origin": origin, "destination": destination})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error: {response.status_code} - {response.text}"}

# Display the shortest path
if origin and destination:
    result = get_shortest_path(origin, destination)
    if "error" in result:
        st.error(result["error"])
    else:
        route = " → ".join(result["route"])
        st.success(f"Rute terpendek: {route}")
        st.info(f"Total jarak: {result['distance']} km")