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
