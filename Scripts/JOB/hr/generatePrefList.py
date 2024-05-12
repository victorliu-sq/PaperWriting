import pandas as pd

# Load the dataset
data = pd.read_csv('Formatted_Expanded_Admission_Predict.csv')

# Assign IDs to each student
data['Student ID'] = range(data.shape[0])

# Sort data by University Rating first, then by GRE, TOEFL, and CGPA
sorted_by_GRE = data.sort_values(by=['University Rating', 'GRE Score'], ascending=[False, False])
sorted_by_TOEFL = data.sort_values(by=['University Rating', 'TOEFL Score'], ascending=[False, False])
sorted_by_CGPA = data.sort_values(by=['University Rating', 'CGPA'], ascending=[False, False])

# Function to save sorted data into a single CSV, with sections for each University Rating
def save_sorted_data(sorted_data, file_name):
    with open(f"{file_name}.csv", 'w') as file:
        for rating in sorted_data['University Rating'].unique():
            # Filter data for the current University Rating
            filtered_data = sorted_data[sorted_data['University Rating'] == rating]
            # Write University Rating header
            file.write(f"University Rating {rating}\n")
            # Write the filtered data
            filtered_data.to_csv(file, index=False, line_terminator='\n')
            file.write('\n')  # Add a newline for spacing between groups

# Save the data into different files
save_sorted_data(sorted_by_GRE, 'Sorted_by_GRE')
save_sorted_data(sorted_by_TOEFL, 'Sorted_by_TOEFL')
save_sorted_data(sorted_by_CGPA, 'Sorted_by_CGPA')

print("Data has been sorted and saved into files for each sorting criterion.")
