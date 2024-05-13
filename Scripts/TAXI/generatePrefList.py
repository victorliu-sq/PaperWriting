import pandas as pd

def process_taxi_data(file_path):
    # Load the Parquet file
    df = pd.read_parquet(file_path)

    # Add a new column for trip ID (0 to number of trips - 1)
    df['tripID'] = range(len(df))

    # Sort the DataFrame by fare amount in descending order
    df_sorted = df.sort_values(by='fare_amount', ascending=False)

    # Keep only the first 25,000 trips
    df_top_20000 = df_sorted.head(20000)

    # Print the tripIDs with their corresponding fare amount
    print(df_top_20000[['tripID', 'fare_amount']])

if __name__ == "__main__":
    # Provide the path to your Parquet file
    file_path = '/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/TAXI/yellow_tripdata_2024-01.parquet'
    process_taxi_data(file_path)
