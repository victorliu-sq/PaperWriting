import pandas as pd
import csv

# Load the data from the CSV file
file_path = '/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/ADM/univ/cwurData.csv'
data = pd.read_csv(file_path)

# Filter the universities that are in the USA
usa_universities = data[data['country'] == 'USA']

# Replace commas with hyphens in the institution names
usa_universities['institution'] = usa_universities['institution'].str.replace(',', '-')

# Keep only the top-50 universities in the USA
top_usa_universities = usa_universities.head(50)

# Get the number of top USA universities
num_top_usa_universities = len(top_usa_universities)

# Calculate the number of integers to be assigned to each university
total_integers = 20000
integers_per_university = total_integers // num_top_usa_universities
remaining_integers = total_integers % num_top_usa_universities

# Create a list to hold the range of integers for each university
integer_ranges = []

start = 0
for i in range(num_top_usa_universities):
    end = start + integers_per_university
    # Distribute the remaining integers
    if remaining_integers > 0:
        end += 1
        remaining_integers -= 1
    integer_range = list(range(start, end))
    integer_ranges.append(",".join(map(str, integer_range)))
    start = end

# Assign the integer ranges to the top USA universities
top_usa_universities = top_usa_universities.reset_index(drop=True)
top_usa_universities['integer_range'] = integer_ranges

# Write the grouped data to a new CSV file
output_file_path = 'grouped_school.csv'
top_usa_universities.to_csv(output_file_path, columns=['institution', 'integer_range'], quoting=csv.QUOTE_NONNUMERIC, index=False)

print(f'Grouped data written to {output_file_path}')
