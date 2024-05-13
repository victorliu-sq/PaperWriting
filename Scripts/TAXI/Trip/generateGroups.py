# import pandas as pd
# import numpy as np
# import csv  # Import csv module for the quoting option

# # Read the CSV file
# data = pd.read_csv("/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/TAXI/Trip/uber_peru_2010.csv", delimiter=';', decimal=',',
#                    parse_dates=['start_at', 'end_at', 'arrived_at'])

# # Handle missing driver_score by setting defaults to 5
# data['driver_score'].fillna(5, inplace=True)

# # Normalize driver_id
# unique_drivers = data['driver_id'].unique()
# driver_id_mapping = {driver: idx for idx, driver in enumerate(unique_drivers)}
# data['normalized_driver_id'] = data['driver_id'].map(driver_id_mapping)

# # Calculate the average score for each driver
# average_scores = data.groupby('driver_id')['driver_score'].mean().round(1)

# # Create bins for every 0.2 score interval
# score_bins = np.arange(start=average_scores.min(), stop=average_scores.max() + 0.2, step=0.2)
# average_scores_binned = pd.cut(average_scores, bins=score_bins, right=False, labels=np.round(score_bins[:-1], 1))

# # Map the normalized IDs back to their corresponding average score bins
# data['avg_score_bin'] = data['driver_id'].map(average_scores_binned.to_dict())

# # Group by these bins and create the expanded list
# grouped_by_score_bin = data.groupby('avg_score_bin')['normalized_driver_id'].unique()

# # Print and save the results
# expanded_driver_scores_df = pd.DataFrame({
#     "Average Score Bin": grouped_by_score_bin.index,
#     "Driver IDs": [",".join(map(str, ids)) for ids in grouped_by_score_bin]
# }).sort_index(ascending=False)

# # Save to CSV without truncating any data, using the correct quoting option from the csv module
# expanded_driver_scores_df.to_csv("grouped_driver_ids_by_average_score.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
# print("Grouped driver IDs by average score saved to 'grouped_driver_ids_by_average_score.csv'.")

import pandas as pd
import numpy as np
import csv

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

# Calculate original group sizes
original_group_sizes = grouped_by_score_bin.apply(len)

# Target total drivers
target_total_drivers = 20000

# Inverse the sizes to create a new proportional scale
inverse_sizes = 1 / original_group_sizes
normalized_inverse_sizes = inverse_sizes / inverse_sizes.sum()  # Normalize the inverse sizes

# Calculate the number of drivers each group should have to reach 20,000 drivers
target_group_sizes = (normalized_inverse_sizes * target_total_drivers).round().astype(int)

# Adjust the total to exactly 20,000 in case of rounding differences
difference = target_total_drivers - target_group_sizes.sum()
target_group_sizes[target_group_sizes.idxmax()] += difference

# Reset ID assignment to ensure range 0-19999
all_driver_ids = np.arange(target_total_drivers)  # Create an array of 20,000 IDs
np.random.shuffle(all_driver_ids)  # Shuffle to randomize distribution

# Allocate these shuffled IDs to each group
start_index = 0
expanded_driver_ids_inverse = {}
for bin_label, size in target_group_sizes.items():
    expanded_driver_ids_inverse[bin_label] = all_driver_ids[start_index:start_index + size]
    start_index += size

# Prepare dataframe for output, sorted by driver score from highest to lowest
expanded_driver_scores_inverse_df = pd.DataFrame({
    "Average Score Bin": [bin_label for bin_label in sorted(expanded_driver_ids_inverse.keys(), reverse=True)],
    "Driver IDs": [",".join(map(str, expanded_driver_ids_inverse[bin_label])) for bin_label in sorted(expanded_driver_ids_inverse.keys(), reverse=True)]
})

# Save to CSV without truncating any data
expanded_driver_scores_inverse_df.to_csv("inverse_expanded_driver_groups_by_average_score.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
print("Inverse expanded driver groups saved to 'inverse_expanded_driver_groups_by_average_score.csv'.")

# Check if the total number of drivers sums up to 20000
total_drivers = sum(len(ids) for ids in expanded_driver_ids_inverse.values())
print(f"Total number of drivers after expansion: {total_drivers}")
