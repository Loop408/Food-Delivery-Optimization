import openrouteservice
from geopy.geocoders import Nominatim
import tkinter as tk
from tkinter import messagebox
import folium
import webbrowser

# === Configuration ===
API_KEY = '5b3ce3597851110001cf624823beb7c433c148f499316888948e7093'
geolocator = Nominatim(user_agent="food_delivery_route_optimizer")
client = openrouteservice.Client(key=API_KEY)

# === Utility Functions ===
def validate_coordinates(lat, lon):
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValueError(f"Invalid coordinates: ({lat}, {lon}) out of bounds.")
    return lat, lon

def geocode(location):
    try:
        loc = geolocator.geocode(location + ", India", country_codes='IN')
        if loc is None:
            raise ValueError(f"Location '{location}' not found in India.")
        return validate_coordinates(loc.latitude, loc.longitude)
    except Exception as e:
        messagebox.showerror("Geocoding Error", f"Error geocoding '{location}': {str(e)}")
        raise

def calculate_distance_matrix(coordinates):
    try:
        coords = [[lon, lat] for lat, lon in coordinates]
        response = client.distance_matrix(
            locations=coords,
            profile='driving-car',
            metrics=['distance']
        )
        if 'distances' not in response:
            raise ValueError("Invalid response from distance matrix API.")
        return response['distances']
    except Exception as e:
        messagebox.showerror("API Error", f"Error calculating distance matrix: {str(e)}")
        raise

def find_shortest_route(coordinates):
    distance_matrix = calculate_distance_matrix(coordinates)
    n = len(coordinates)
    visited = [False] * n
    route = [0]
    visited[0] = True
    current = 0

    for _ in range(1, n):
        next_city = min(
            (i for i in range(n) if not visited[i]),
            key=lambda i: distance_matrix[current][i],
            default=None
        )
        if next_city is None:
            break
        visited[next_city] = True
        route.append(next_city)
        current = next_city

    return route

def plot_route(deliveries, coordinates, route):
    try:
        start_latlon = coordinates[route[0]]
        map_obj = folium.Map(location=start_latlon, zoom_start=6)
        total_distance = 0
        points = [coordinates[i] for i in route]

        for idx, i in enumerate(route):
            lat, lon = coordinates[i]
            name = deliveries[i][0]
            folium.map.Marker(
                [lat, lon],
                popup=f"{name}",
                icon=folium.DivIcon(
                    html=f"""<div style='font-size: 16px; color: white; background: red; border-radius: 50%; width: 30px; height: 30px; text-align: center; line-height: 30px;'>{idx+1}</div>"""
                )
            ).add_to(map_obj)

        for i in range(len(points) - 1):
            start, end = points[i], points[i + 1]
            route_response = client.directions(
                coordinates=[[start[1], start[0]], [end[1], end[0]]],
                profile='driving-car',
                format='geojson'
            )
            geometry = route_response['features'][0]['geometry']['coordinates']
            distance = route_response['features'][0]['properties']['segments'][0]['distance'] / 1000
            total_distance += distance

            folium.PolyLine(
                [list(reversed(coord)) for coord in geometry],
                color="blue",
                weight=3,
                opacity=0.8,
                tooltip=f"{distance:.2f} km"
            ).add_to(map_obj)

        folium.Marker(
            start_latlon,
            popup=f"Total Route Distance: {total_distance:.2f} km",
            icon=folium.Icon(color='green')
        ).add_to(map_obj)

        map_obj.save("optimized_route.html")
        webbrowser.open("optimized_route.html")
        messagebox.showinfo("Success", "Optimized route saved and opened in browser!")
    except Exception as e:
        messagebox.showerror("Routing Error", f"Error plotting route: {str(e)}")
        raise

# === GUI Functions ===
def add_delivery_entry():
    row = tk.Frame(frame_inputs, bg="#f0f0f0")
    row.pack(pady=5)

    name_entry = tk.Entry(row, width=20)
    name_entry.pack(side="left", padx=5)

    phone_entry = tk.Entry(row, width=15)
    phone_entry.pack(side="left", padx=5)

    location_entry = tk.Entry(row, width=30)
    location_entry.pack(side="left", padx=5)

    entries.append((name_entry, phone_entry, location_entry))

def on_optimize_route():
    deliveries = []
    coordinates = []
    for name_entry, phone_entry, loc_entry in entries:
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        loc = loc_entry.get().strip()
        if not (name and phone and loc):
            messagebox.showerror("Input Error", "All fields must be filled.")
            return
        try:
            coord = geocode(loc)
            deliveries.append((name, phone, loc))
            coordinates.append(coord)
        except Exception:
            return

    try:
        route = find_shortest_route(coordinates)
        plot_route(deliveries, coordinates, route)
    except Exception as e:
        print(f"Error: {e}")

# === GUI Setup ===
root = tk.Tk()
root.title("Food Delivery Route Optimizer")
root.geometry("700x700")
root.configure(bg="#f0f0f0")

tk.Label(
    root,
    text="Food Delivery Management",
    font=("Arial", 18, "bold"),
    bg="#f0f0f0"
).pack(pady=20)

frame_inputs = tk.Frame(root, bg="#f0f0f0")
frame_inputs.pack(pady=20)

entries = []

btn_add = tk.Button(
    root,
    text="Add Delivery Entry",
    command=add_delivery_entry,
    bg="blue",
    fg="white",
    font=("Arial", 14),
    width=20
)
btn_add.pack(pady=10)

btn_optimize = tk.Button(
    root,
    text="Optimize Route",
    command=on_optimize_route,
    bg="green",
    fg="white",
    font=("Arial", 14),
    width=20
)
btn_optimize.pack(pady=10)

root.mainloop()
