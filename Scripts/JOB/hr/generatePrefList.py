# import pandas as pd

# def list_unique_values(file_path):
#     # Load the dataset
#     df = pd.read_csv(file_path)
    
#     # Columns of interest
#     columns_of_interest = ["relevent_experience", "enrolled_university", "education_level", "major_discipline"]
    
#     # Iterate over the columns and print unique values
#     for column in columns_of_interest:
#         unique_values = df[column].dropna().unique()  # Drop NA to only get actual entries
#         print(f"Unique values in '{column}': {unique_values}")

# if __name__ == "__main__":
#     # Specify the path to your CSV file
#     file_path = 'aug_train.csv'
    
#     # Call the function
#     list_unique_values(file_path)

# print all group names
# import pandas as pd

# def generate_group_names(file_path):
#     # Load the dataset
#     df = pd.read_csv(file_path)
    
#     # Initialize a set to store unique group names
#     group_names = set()

#     # Add non-STEM group name
#     group_names.add("Non-STEM Group")

#     # Filter for STEM group
#     stem_group = df[df['major_discipline'] == 'STEM']

#     # Generate group names for STEM based on education level and relevant experience
#     for education_level in stem_group['education_level'].dropna().unique():
#         for experience in stem_group['relevent_experience'].dropna().unique():
#             group_name = f"STEM - {education_level} - {experience}"
#             group_names.add(group_name)

#     # Print all group names
#     for name in sorted(group_names):
#         print(name)

# if __name__ == "__main__":
#     # Specify the path to your CSV file
#     file_path = 'aug_train.csv'
    
#     # Call the function
#     generate_group_names(file_path)

import pandas as pd

def categorize_and_sort_applicants(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Relabel enrollee_id to a sequence starting from 0
    df['new_enrollee_id'] = range(len(df))
    
    # Define the order of group names
    group_order = [
        "STEM - Phd - Has relevent experience",
        "STEM - Phd - No relevent experience",
        "STEM - Masters - Has relevent experience",
        "STEM - Masters - No relevent experience",
        "STEM - Graduate - Has relevent experience",
        "STEM - Graduate - No relevent experience",
        "Non-STEM Group"
    ]

    # Dictionary to hold enrollee_ids for each group
    groups = {name: [] for name in group_order}

    # Filter for STEM and non-STEM groups
    stem_group = df[df['major_discipline'] == 'STEM']
    non_stem_group = df[df['major_discipline'] != 'STEM']
    groups["Non-STEM Group"] = non_stem_group['new_enrollee_id'].tolist()

    # Populate groups for STEM disciplines
    for index, row in stem_group.iterrows():
        if pd.notna(row['education_level']) and pd.notna(row['relevent_experience']):
            group_name = f"STEM - {row['education_level']} - {row['relevent_experience']}"
            if group_name in groups:
                groups[group_name].append(row['new_enrollee_id'])

    # Print all group names and their corresponding enrollee_ids
    for name in group_order:
        print(f"{name}:")
        print(groups[name])
        print()  # Print a newline for better separation

    print("Total number of applicant is ", len(df))

if __name__ == "__main__":
    # Specify the path to your CSV file
    file_path = '/Users/jiaxinliu/Desktop/PaperWriting/DataSets/JOB/hr/aug_train.csv'
    
    # Call the function
    categorize_and_sort_applicants(file_path)
