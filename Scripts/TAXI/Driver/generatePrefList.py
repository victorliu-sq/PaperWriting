# import pandas as pd

# def process_taxi_data(file_path):
#     # Load the Parquet file
#     df = pd.read_parquet(file_path)

#     # Add a new column for trip ID (0 to number of trips - 1)
#     df['tripID'] = range(len(df))

#     # Sort the DataFrame by fare amount in descending order
#     df_sorted = df.sort_values(by='fare_amount', ascending=False)

#     # Keep only the first 25,000 trips
#     df_top_20000 = df_sorted.head(20000)

#     # Print the tripIDs with their corresponding fare amount
#     print(df_top_20000[['tripID', 'fare_amount']])

# if __name__ == "__main__":
#     # Provide the path to your Parquet file
#     file_path = '/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/TAXI/yellow_tripdata_2024-01.parquet'
#     process_taxi_data(file_path)

# import pandas as pd

# def process_taxi_data(file_path):
#     # Load the Parquet file
#     df = pd.read_parquet(file_path)
    
#     # Filter the top 20,000 trips by total_amount in descending order
#     df = df.nlargest(20000, 'total_amount')

#     # Sort by total_amount descending to make sure it's in the right order for grouping
#     df = df.sort_values(by='total_amount', ascending=False)

#     # Initialize the group ID and list for storing results
#     group_id = 0
#     groups = []
#     group_sizes = []

#     # Iterate through the DataFrame to group trips
#     for i in range(len(df)):
#         if i == 0:
#             # First entry always starts a new group
#             df.at[df.index[i], 'group_id'] = group_id
#             current_total = df.at[df.index[i], 'total_amount']
#             group_size = 1
#         else:
#             if abs(current_total - df.at[df.index[i], 'total_amount']) > 5:
#                 # Print the current group and its size before starting a new group
#                 print(f"Group {group_id}: Size {group_size}")
#                 groups.append(df[df['group_id'] == group_id])
#                 group_sizes.append(group_size)

#                 # Start new group
#                 group_id += 1
#                 group_size = 1
#                 current_total = df.at[df.index[i], 'total_amount']
#             else:
#                 # Continue in the same group
#                 group_size += 1
            
#             # Assign group ID
#             df.at[df.index[i], 'group_id'] = group_id

#     # Print the last group since it won't be included in the loop's condition
#     print(f"Group {group_id}: Size {group_size}")
#     groups.append(df[df['group_id'] == group_id])
#     group_sizes.append(group_size)

# if __name__ == "__main__":
#     # Provide the path to your Parquet file
#     file_path = '/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/TAXI/yellow_tripdata_2024-01.parquet'
#     process_taxi_data(file_path)

import pandas as pd

def process_taxi_data(file_path):
    # Load the Parquet file
    df = pd.read_parquet(file_path)
    
    # Filter the top 20,000 trips by total_amount in descending order
    df = df.nlargest(20000, 'total_amount')

    # Sort by total_amount descending to make sure it's in the right order for grouping
    df = df.sort_values(by='total_amount', ascending=False)

    # Add a tripID column
    df['tripID'] = range(len(df))

    # Initialize the group ID
    group_id = 0
    current_total = df.iloc[0]['total_amount']
    df['group_id'] = 0

    # Assign group IDs based on the grouping condition
    for i in range(1, len(df)):
        if abs(current_total - df.iloc[i]['total_amount']) > 5:
            group_id += 1
            current_total = df.iloc[i]['total_amount']
        df.at[df.index[i], 'group_id'] = group_id

    # Filter the DataFrame to only include tripID and group_id
    grouped_df = df[['tripID', 'group_id']]

    # Sort grouped DataFrame by group_id for clarity in the output
    grouped_df = grouped_df.sort_values(by='group_id')

    # Save to a single CSV file
    grouped_df.to_csv('grouped_tripIDs.csv', index=False)
    print("Grouped trip IDs have been written to 'grouped_tripIDs.csv'.")

if __name__ == "__main__":
    # Provide the path to your Parquet file
    # file_path = 'yellow_tripdata_2024-01.parquet'
    file_path = '/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/TAXI/yellow_tripdata_2024-01.parquet'
    process_taxi_data(file_path)
