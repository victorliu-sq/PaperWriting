import pandas as pd
import numpy as np

# Sample data: Load your existing DataFrame here.
data = {
    "VendorID": [2, 1, 1, 1, 1],
    "tpep_pickup_datetime": ["2024-01-01 00:57:55", "2024-01-01 00:03:00", "2024-01-01 00:17:06", "2024-01-01 00:36:38", "2024-01-01 00:46:51"],
    "trip_distance": [1.72, 1.80, 4.70, 1.40, 0.80],
    # Add other fields as necessary
}
df = pd.DataFrame(data)

# Define the range for random distances
min_distance = 0.1  # minimum distance in miles
max_distance = 5.0  # maximum distance in miles

# Generate random distances between passengers and drivers
np.random.seed(42)  # for reproducibility
df['distance_to_passenger'] = np.random.uniform(min_distance, max_distance, df.shape[0])

print(df)
