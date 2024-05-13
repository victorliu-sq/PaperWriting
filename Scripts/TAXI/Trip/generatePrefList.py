# import pandas as pd

# # Step 1: Read the CSV file
# data = pd.read_csv("/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/TAXI/Trip/uber_peru_2010.csv", delimiter=';', decimal=',',
#                    parse_dates=['start_at', 'end_at', 'arrived_at'])

# # Step 2: Normalize driver_id
# unique_drivers = data['driver_id'].unique()
# driver_id_mapping = {driver: idx for idx, driver in enumerate(unique_drivers)}
# data['normalized_driver_id'] = data['driver_id'].map(driver_id_mapping)

# # Step 3: Group by driver_score and get the size of each group
# grouped_by_driver_score = data.groupby('driver_score')
# group_sizes = grouped_by_driver_score.size()

# # Step 4: Print the size of each group
# print(group_sizes)

# # Creating a dataframe from the group to save to file
# driver_groups = grouped_by_driver_score['normalized_driver_id'].unique().sort_index(ascending=False)
# driver_scores = pd.DataFrame({
#     'Driver Score': driver_groups.index,
#     'Normalized Driver IDs': driver_groups.values
# })

# # Saving the groups and driver ratings from highest to lowest rating into a new CSV file
# driver_scores.to_csv("driver_groups_by_rating.csv", index=False)
# print("Driver groups saved to 'driver_groups_by_rating.csv'.")

import pandas as pd
import numpy as np

# Read the CSV file
data = pd.read_csv("/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/TAXI/Trip/uber_peru_2010.csv", delimiter=';', decimal=',',
                   parse_dates=['start_at', 'end_at', 'arrived_at'])

# Normalize driver_id
unique_drivers = data['driver_id'].unique()
driver_id_mapping = {driver: idx for idx, driver in enumerate(unique_drivers)}
data['normalized_driver_id'] = data['driver_id'].map(driver_id_mapping)

# Group by driver_score and get the size of each group
grouped_by_driver_score = data.groupby('driver_score')
group_sizes = grouped_by_driver_score.size()

# Print the size of each group
print(group_sizes)

# Current total drivers
# current_total_drivers = len(data['driver_id'].dropna().unique())
current_total_drivers = sum(group_sizes)
print("current_total_driver: ", current_total_drivers)

# Target total drivers
target_total_drivers = 20000

# Calculating the required number of drivers per group
proportions = group_sizes / current_total_drivers
expanded_group_sizes = (proportions * target_total_drivers).round().astype(int)
print("expanded_group_sizes: ",sum(expanded_group_sizes))

# Adjust if the total is not exactly 20000
if sum(expanded_group_sizes) != target_total_drivers:
    difference = target_total_drivers - sum(expanded_group_sizes)
    expanded_group_sizes[expanded_group_sizes.idxmax()] += difference  # Adjust the largest group

print("adjusted expanded_group_sizes: ", sum(expanded_group_sizes))

# Create an expanded list of driver IDs
expanded_driver_ids = {}
next_id_start = max(driver_id_mapping.values()) + 1
for score, size in expanded_group_sizes.items():
    original_ids = grouped_by_driver_score.get_group(score)['normalized_driver_id'].unique()
    num_repeats = size // len(original_ids) + 1  # Ensure enough IDs are generated
    repeated_ids = np.tile(original_ids, num_repeats)[:size]
    new_ids_range = range(next_id_start, next_id_start + size - len(original_ids))
    expanded_driver_ids[score] = np.concatenate([original_ids, new_ids_range])
    next_id_start += size - len(original_ids)

# Print expanded group sizes
for score, ids in expanded_driver_ids.items():
    print(f"Driver Score: {score}, Number of Drivers: {len(ids)}")

# Optionally save expanded driver ids
# Here we create a dataframe to save these results, modify as needed for specific output format
expanded_driver_scores_df = pd.DataFrame([
    {"Driver Score": score, "Driver IDs": ids}
    for score, ids in expanded_driver_ids.items()
])
expanded_driver_scores_df.to_csv("expanded_driver_groups_by_rating.csv", index=False)
print("Expanded driver groups saved to 'expanded_driver_groups_by_rating.csv'.")
