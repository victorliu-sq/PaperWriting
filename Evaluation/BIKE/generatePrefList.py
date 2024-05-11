import pandas as pd
import numpy as np
from scipy.spatial import distance

# Load data
data = pd.read_csv("metro-trips-2024-q1.csv")

# Preprocess: Remove trips below 1 minute and cap at 24 hours
data = data[(data['duration'] >= 1) & (data['duration'] <= 1440)]

print("Number of Trips:", len(data))

# Check for and handle missing data in coordinates
data.dropna(subset=['start_lat', 'start_lon', 'end_lat', 'end_lon'], inplace=True)

# Alternatively, you could fill missing data if applicable
# data['start_lat'].fillna(value=your_value, inplace=True)
# data['start_lon'].fillna(value=your_value, inplace=True)
# data['end_lat'].fillna(value=your_value, inplace=True)
# data['end_lon'].fillna(value=your_value, inplace=True)

# Calculate Euclidean distances for each trip
data['distance'] = data.apply(lambda row: distance.euclidean(
    (row['start_lat'], row['start_lon']), (row['end_lat'], row['end_lon'])), axis=1)

# Assign uniformly distributed order values to each unique start station
unique_stations = data['start_station'].unique()
orders = np.random.uniform(low=0, high=1, size=len(unique_stations))
station_order = pd.Series(orders, index=unique_stations)

# Map these orders to trips
data['order_value'] = data['start_station'].map(station_order)

# Assuming 'n' is determined by the unique trips or stations (simplified assumption here)
n = min(len(data), len(unique_stations))

# Generate preference lists
# X side: Rank by closest distances
x_preferences = data.nsmallest(n, 'distance')['trip_id'].tolist()

# Y side: Rank by highest order values
y_preferences = data.nlargest(n, 'order_value')['trip_id'].tolist()

# Print or return the preference lists
print("X Preferences (based on distance):", x_preferences)
print("Y Preferences (based on order values):", y_preferences)
