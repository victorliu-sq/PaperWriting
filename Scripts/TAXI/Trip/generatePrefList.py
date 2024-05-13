# import pandas as pd
# import numpy as np

# # Read the CSV file
# data = pd.read_csv("/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/TAXI/Trip/uber_peru_2010.csv", delimiter=';', decimal=',',
#                    parse_dates=['start_at', 'end_at', 'arrived_at'])

# # Normalize driver_id
# unique_drivers = data['driver_id'].unique()
# driver_id_mapping = {driver: idx for idx, driver in enumerate(unique_drivers)}
# data['normalized_driver_id'] = data['driver_id'].map(driver_id_mapping)

# # Group by driver_score and get the size of each group
# grouped_by_driver_score = data.groupby('driver_score')
# group_sizes = grouped_by_driver_score.size()

# # Print the size of each group
# print(group_sizes)

# # Current total drivers
# # current_total_drivers = len(data['driver_id'].dropna().unique())
# current_total_drivers = sum(group_sizes)
# print("current_total_driver: ", current_total_drivers)

# # Target total drivers
# target_total_drivers = 20000

# # Calculating the required number of drivers per group
# proportions = group_sizes / current_total_drivers
# expanded_group_sizes = (proportions * target_total_drivers).round().astype(int)
# print("expanded_group_sizes: ",sum(expanded_group_sizes))

# # Adjust if the total is not exactly 20000
# if sum(expanded_group_sizes) != target_total_drivers:
#     difference = target_total_drivers - sum(expanded_group_sizes)
#     expanded_group_sizes[expanded_group_sizes.idxmax()] += difference  # Adjust the largest group

# print("adjusted expanded_group_sizes: ", sum(expanded_group_sizes))

# # Create an expanded list of driver IDs
# expanded_driver_ids = {}
# next_id_start = max(driver_id_mapping.values()) + 1
# for score, size in expanded_group_sizes.items():
#     original_ids = grouped_by_driver_score.get_group(score)['normalized_driver_id'].unique()
#     num_repeats = size // len(original_ids) + 1  # Ensure enough IDs are generated
#     repeated_ids = np.tile(original_ids, num_repeats)[:size]
#     new_ids_range = range(next_id_start, next_id_start + size - len(original_ids))
#     expanded_driver_ids[score] = np.concatenate([original_ids, new_ids_range])
#     next_id_start += size - len(original_ids)

# # Print expanded group sizes
# for score, ids in expanded_driver_ids.items():
#     print(f"Driver Score: {score}, Number of Drivers: {len(ids)}")

# # Optionally save expanded driver ids
# # Here we create a dataframe to save these results, modify as needed for specific output format
# # expanded_driver_scores_df = pd.DataFrame([
# #     {"Driver Score": score, "Driver IDs": ids}
# #     for score, ids in expanded_driver_ids.items()
# # ])

# # Prepare dataframe for output, sorted by driver score from highest to lowest
# expanded_driver_scores_df = pd.DataFrame([
#     {"Driver Score": score, "Driver IDs": ",".join(map(str, ids))}
#     for score, ids in sorted(expanded_driver_ids.items(), reverse=True, key=lambda x: x[0])
# ])


# expanded_driver_scores_df.to_csv("expanded_driver_groups_by_rating.csv", index=False)
# print("Expanded driver groups saved to 'expanded_driver_groups_by_rating.csv'.")

import pandas as pd
import numpy as np
import csv  # Import csv module for the quoting option

# Read the CSV file
data = pd.read_csv("/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/TAXI/Trip/uber_peru_2010.csv", delimiter=';', decimal=',',
                   parse_dates=['start_at', 'end_at', 'arrived_at'])

# Handle missing driver_score by setting defaults to 5
data['driver_score'].fillna(5, inplace=True)

# Normalize driver_id
unique_drivers = data['driver_id'].unique()
driver_id_mapping = {driver: idx for idx, driver in enumerate(unique_drivers)}
data['normalized_driver_id'] = data['driver_id'].map(driver_id_mapping)

# Calculate the average score for each driver
average_scores = data.groupby('driver_id')['driver_score'].mean().round(1)

# Create bins for every 0.2 score interval
score_bins = np.arange(start=average_scores.min(), stop=average_scores.max() + 0.2, step=0.2)
average_scores_binned = pd.cut(average_scores, bins=score_bins, right=False, labels=np.round(score_bins[:-1], 1))

# Map the normalized IDs back to their corresponding average score bins
data['avg_score_bin'] = data['driver_id'].map(average_scores_binned.to_dict())

# Group by these bins and create the expanded list
grouped_by_score_bin = data.groupby('avg_score_bin')['normalized_driver_id'].unique()

# Print and save the results
expanded_driver_scores_df = pd.DataFrame({
    "Average Score Bin": grouped_by_score_bin.index,
    "Driver IDs": [",".join(map(str, ids)) for ids in grouped_by_score_bin]
}).sort_index(ascending=False)

# Save to CSV without truncating any data, using the correct quoting option from the csv module
expanded_driver_scores_df.to_csv("grouped_driver_ids_by_average_score.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
print("Grouped driver IDs by average score saved to 'grouped_driver_ids_by_average_score.csv'.")
