import pyarrow.parquet as pq

def read_parquet_with_pyarrow(file_path):
    # Reading the Parquet file into an Arrow Table
    table = pq.read_table(file_path)
    
    # Convert the Arrow Table to a pandas DataFrame
    df = table.to_pandas()
    
    # Display the first few rows of the DataFrame
    print(df.head())

if __name__ == "__main__":
    # Specify the path to your Parquet file
    file_path = '/Users/jiaxinliu/Desktop/PaperWriting/DataSets/TAXI/yellow_tripdata_2024-01.parquet'
    
    # Call the function to read and display the data
    read_parquet_with_pyarrow(file_path)
