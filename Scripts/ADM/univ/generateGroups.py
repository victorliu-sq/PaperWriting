import pandas as pd
import csv

# Load the CSV file
file_path = '/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/ADM/app/Formatted_Expanded_Admission_Predict.csv'
df = pd.read_csv(file_path)

# Add a new column for studentID as integers from 0 to total number of students - 1
df['studentID'] = range(len(df))

# Sort by CGPA from highest to lowest
df = df.sort_values(by='CGPA', ascending=False)

# Create a dictionary to hold the groups
grouped = {}

# Function to determine the CGPA group
def get_cgpa_group(cgpa):
    return int(cgpa // 0.5) * 0.5

# Group by CGPA with a 0.5 difference
for index, row in df.iterrows():
    cgpa_group = get_cgpa_group(row['CGPA'])
    if cgpa_group not in grouped:
        grouped[cgpa_group] = []
    grouped[cgpa_group].append(int(row['studentID']))

# Write the groups to a new CSV file
output_file_path = 'Grouped_Students.csv'
with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(['CGPA Group', 'studentIDs'])
    for cgpa_group, student_ids in sorted(grouped.items(), reverse=True):
        # Convert the list of student IDs to a comma-separated string
        student_ids_str = ', '.join(map(str, student_ids))
        writer.writerow([cgpa_group, student_ids_str])

print(f'Grouped students have been written to {output_file_path}')
