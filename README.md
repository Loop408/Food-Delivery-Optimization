# Food Delivery Route Optimizer

## Overview
The Food Delivery Route Optimizer is a Python-based desktop application that calculates the shortest delivery route for multiple addresses in India. It helps delivery businesses save time and fuel by optimizing delivery paths and visualizing them on an interactive map.

## Features
- Add multiple delivery entries with customer name, phone number, and location
- Automatic geocoding using Geopy (Nominatim)
- Shortest route calculation using a greedy algorithm and OpenRouteService
- Interactive map visualization with Folium
- User-friendly Tkinter GUI
- Saves and opens the optimized route map in your browser

## Technologies Used
- Python 3
- Tkinter for GUI
- Geopy for geocoding
- OpenRouteService API for routing and distance calculation
- Folium for map visualization
- Webbrowser for opening the output map

## File Description
food.py
- Geocodes addresses into coordinates
- Calculates driving distances between delivery points
- Finds the shortest route using a greedy algorithm
- Plots the route on a Folium map with markers and distances
- Provides a Tkinter GUI to add deliveries and optimize the route
- Saves the route as optimized_route.html and opens it automatically

## Installation
1. Clone the repository:
   git clone https://github.com/your-username/food-delivery-route-optimizer.git
   cd food-delivery-route-optimizer
2. Install dependencies:
   pip install openrouteservice geopy folium
3. Get an OpenRouteService API key:
   - Sign up at https://openrouteservice.org/sign-up/
   - Replace the API_KEY value in food.py with your key

## Usage
1. Run the application:
   python food.py
2. Click "Add Delivery Entry" to add a new delivery
3. Fill in the name, phone number, and location (address in India)
4. Add as many deliveries as needed
5. Click "Optimize Route" to calculate and display the optimized route in your browser

## Output
- Interactive HTML map with numbered delivery stops
- Routes between stops with distance tooltips
- Displays total route distance on the map

## License
This project is licensed under the MIT License
