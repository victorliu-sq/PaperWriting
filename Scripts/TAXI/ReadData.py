import pandas as pd

def load_and_display_parquet(file_path):
    # Load the Parquet file
    df = pd.read_parquet(file_path)

    # Display the columns of the DataFrame
    print("Columns in the dataset:")
    print(df.columns.tolist())

    # Display the first few records
    print("\nFirst few records:")
    print(df.head())

if __name__ == "__main__":
    # Specify the path to your Parquet file
    file_path = "/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/TAXI/yellow_tripdata_2024-01.parquet"
    
    # Call the function to load and display the data
    load_and_display_parquet(file_path)
