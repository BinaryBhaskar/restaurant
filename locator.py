from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2

def distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Radius of the Earth (mean value), approximately 6,371 kilometers
    earth_radius = 6371.0

    # Calculate the distance
    distance = earth_radius * c

    return distance

# Initialize the geocoder
geolocator = Nominatim(user_agent="distance_calculator")

# User-provided address
user_address = "Mukta, Chhattisgarh, 495692"

# Geocode the user's address
user_location = geolocator.geocode(user_address)

if __name__ == "__main__":
    if user_location:
        # Coordinates for Chandrapur, Chhattisgarh (You can replace these with actual coordinates)
        chandrapur_lat = 21.7067
        chandrapur_lon = 83.2325

        # Extract user's latitude and longitude
        user_lat = user_location.latitude
        user_lon = user_location.longitude

        # Calculate the distance
        distance_km = distance(chandrapur_lat, chandrapur_lon, user_lat, user_lon)

        print(f"The straight-line distance between {user_address} and Chandrapur, Chhattisgarh is {distance_km:.2f} kilometers.")
    else:
        print(f"Could not find coordinates for {user_address}. Please provide a valid address.")
