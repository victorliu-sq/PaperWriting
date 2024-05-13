import pandas as pd

def categorize_and_sort_applicants(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Calculate how many more rows are needed
    total_required = 20000
    current_count = len(df)
    if current_count < total_required:
        rows_to_add = total_required - current_count
        duplicates = df.tail(rows_to_add).copy()
        df = pd.concat([df, duplicates], ignore_index=True)
    
    # Relabel enrollee_id to a sequence starting from 0
    df['new_enrollee_id'] = range(len(df))
    
    # Ensure all enrollee IDs from 0 to 19999 are present
    assert df['new_enrollee_id'].nunique() == total_required, "Not all IDs from 0 to 19999 are present"
    assert len(df) == total_required, "Total number of rows is not 20000"
    
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

    # Write the groups to a CSV file
    with open('grouped_applicants.csv', 'w') as file:
        file.write('"Group Name","Enrollee IDs"\n')
        for name in group_order:
            enrollee_ids = ",".join(map(str, groups[name]))
            file.write(f'"{name}","{enrollee_ids}"\n')

if __name__ == "__main__":
    # Specify the path to your CSV file
    file_path = '/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/JOB/hr/aug_train.csv'
    
    # Call the function
    categorize_and_sort_applicants(file_path)
