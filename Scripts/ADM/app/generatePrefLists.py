# import pandas as pd

# # Load the dataset
# data = pd.read_csv('/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/ADM/app/Formatted_Expanded_Admission_Predict.csv')

# # Assign IDs to each student
# data['Student ID'] = range(data.shape[0])

# # Sort data by University Rating (Descending)
# data_sorted_by_university = data.sort_values(by='University Rating', ascending=False)

# # Generate three kinds of preference lists within each University Rating group
# # Sorting by GRE Score
# sorted_by_GRE = data_sorted_by_university.groupby('University Rating').apply(
#     lambda x: x.sort_values('GRE Score', ascending=False)
# ).reset_index(drop=True)

# # Sorting by TOEFL Score
# sorted_by_TOEFL = data_sorted_by_university.groupby('University Rating').apply(
#     lambda x: x.sort_values('TOEFL Score', ascending=False)
# ).reset_index(drop=True)

# # Sorting by CGPA
# sorted_by_CGPA = data_sorted_by_university.groupby('University Rating').apply(
#     lambda x: x.sort_values('CGPA', ascending=False)
# ).reset_index(drop=True)

# # Extracting sorted lists of Student IDs
# gre_list = sorted_by_GRE[['University Rating', 'Student ID']].groupby('University Rating')['Student ID'].apply(list)
# toefl_list = sorted_by_TOEFL[['University Rating', 'Student ID']].groupby('University Rating')['Student ID'].apply(list)
# cgpa_list = sorted_by_CGPA[['University Rating', 'Student ID']].groupby('University Rating')['Student ID'].apply(list)

# # Print the sorted group of university ratings
# print("GRE Score Sorted List by University Rating:")
# print(gre_list)
# print("\nTOEFL Score Sorted List by University Rating:")
# print(toefl_list)
# print("\nCGPA Sorted List by University Rating:")
# print(cgpa_list)

# import pandas as pd

# # Load the dataset
# data = pd.read_csv('/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/ADM/app/Formatted_Expanded_Admission_Predict.csv')

# # Assign IDs to each student
# data['Student ID'] = range(data.shape[0])

# # Sort data by University Rating first, then by GRE, TOEFL, and CGPA
# sorted_by_GRE = data.sort_values(by=['University Rating', 'GRE Score'], ascending=[False, False])
# sorted_by_TOEFL = data.sort_values(by=['University Rating', 'TOEFL Score'], ascending=[False, False])
# sorted_by_CGPA = data.sort_values(by=['University Rating', 'CGPA'], ascending=[False, False])

# # Function to save sorted data into a single CSV, with sections for each University Rating
# def save_sorted_data(sorted_data, file_name):
#     with open(f"{file_name}.csv", 'w') as file:
#         for rating in sorted_data['University Rating'].unique():
#             # Filter data for the current University Rating
#             filtered_data = sorted_data[sorted_data['University Rating'] == rating]
#             # Write University Rating header
#             file.write(f"University Rating {rating}\n")
#             # Write the filtered data
#             filtered_data.to_csv(file, index=False, line_terminator='\n')
#             file.write('\n')  # Add a newline for spacing between groups

# # Save the data into different files
# save_sorted_data(sorted_by_GRE, 'Sorted_by_GRE')
# save_sorted_data(sorted_by_TOEFL, 'Sorted_by_TOEFL')
# save_sorted_data(sorted_by_CGPA, 'Sorted_by_CGPA')

# print("Data has been sorted and saved into files for each sorting criterion.")

import pandas as pd

# Load the dataset
data = pd.read_csv('/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/ADM/app/Formatted_Expanded_Admission_Predict.csv')

# Assign IDs to each student
data['Student ID'] = range(data.shape[0])

# Sort data by University Rating first, then by GRE, TOEFL, and CGPA
sorted_by_GRE = data.sort_values(by=['University Rating', 'GRE Score'], ascending=[False, False])
sorted_by_TOEFL = data.sort_values(by=['University Rating', 'TOEFL Score'], ascending=[False, False])
sorted_by_CGPA = data.sort_values(by=['University Rating', 'CGPA'], ascending=[False, False])

# Function to save sorted student IDs into a single CSV, with sections for each University Rating
def save_sorted_ids(sorted_data, file_name):
    with open(f"{file_name}.csv", 'w') as file:
        for rating in sorted_data['University Rating'].unique():
            # Filter data for the current University Rating
            filtered_data = sorted_data[sorted_data['University Rating'] == rating]
            # Write University Rating header
            file.write(f"University Rating {rating}\n")
            # Write the filtered student IDs
            filtered_ids = filtered_data['Student ID'].to_list()
            file.write(','.join(map(str, filtered_ids)) + '\n\n')

# Save the data into different files
save_sorted_ids(sorted_by_GRE, 'StudentIDs_Sorted_by_GRE')
save_sorted_ids(sorted_by_TOEFL, 'StudentIDs_Sorted_by_TOEFL')
save_sorted_ids(sorted_by_CGPA, 'StudentIDs_Sorted_by_CGPA')

print("Student IDs have been sorted and saved into files for each sorting criterion.")
