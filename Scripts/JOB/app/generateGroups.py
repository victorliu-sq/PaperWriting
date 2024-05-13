# import pandas as pd
# import numpy as np
# import csv

# def duplicate_jobs_to_target(file_path, target_total):
#     # Load the CSV file into a DataFrame
#     data = pd.read_csv(file_path)

#     # Add a new column 'Relabeled Job ID' with sequential values starting from 0 up to the number of jobs minus one
#     data['Relabeled Job ID'] = range(data.shape[0])

#     # Extract the lower bound salary from the 'Salary Estimate' column
#     data['Salary Lower Bound'] = data['Salary Estimate'].apply(extract_lower_bound)

#     # Drop rows with NaN values (non-annual salaries like hourly rates)
#     data = data.dropna(subset=['Salary Lower Bound'])

#     # Convert the extracted salary lower bounds to integers for sorting
#     data['Salary Lower Bound'] = data['Salary Lower Bound'].astype(int)

#     # Determine the number of duplicates required
#     current_total = data.shape[0]
#     duplicates_needed = target_total - current_total

#     if duplicates_needed > 0:
#         # Calculate the base number of duplicates per job
#         duplicates_per_job = duplicates_needed // current_total

#         # Calculate any extra jobs needed to reach the exact target
#         extra_needed = duplicates_needed % current_total

#         # Create an array with the base number of duplicates for each job
#         duplication_array = np.full((current_total,), duplicates_per_job)

#         # Distribute the extra duplicates as evenly as possible
#         if extra_needed > 0:
#             duplication_array[:extra_needed] += 1

#         # Duplicate the jobs according to the duplication_array
#         data = data.loc[data.index.repeat(duplication_array + 1)]  # '+1' to include the original job

#     # Reassign 'Relabeled Job ID' to maintain unique IDs across duplicates
#     data.reset_index(drop=True, inplace=True)
#     data['Relabeled Job ID'] = range(data.shape[0])

#     # Sort data by the lower bound of the salary
#     sorted_data = data.sort_values(by='Salary Lower Bound')

#     # Group jobs by 10000 salary intervals
#     sorted_data['Salary Group'] = (sorted_data['Salary Lower Bound'] // 10000) * 10000

#     # Write groups to a single CSV file
#     with open('grouped_jobs.csv', 'w', newline='') as file:
#         writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
#         writer.writerow(['Salary Group', 'Job IDs'])

#         for group, group_data in sorted_data.groupby('Salary Group'):
#             job_ids = ", ".join(map(str, group_data['Relabeled Job ID'].tolist()))
#             writer.writerow([group, job_ids])

#     # Output total number of jobs
#     total_jobs = sorted_data.shape[0]

#     # Print each job ID sorted by the lower bound of the salary estimate
#     print("Sorted Job IDs by Salary Lower Bound:")
#     for index, row in sorted_data.iterrows():
#         print(f"Relabeled Job ID: {row['Relabeled Job ID']}, Salary Estimate: {row['Salary Estimate']}")

#     print(f"Total Number of Jobs: {total_jobs}")


# def extract_lower_bound(salary_estimate):
#     if 'Per Hour' in salary_estimate or 'Employer est.' in salary_estimate:
#         return float('nan')  # For non-annual salary formats
#     else:
#         lower_bound = salary_estimate.split('-')[0].replace('$', '').replace('K', '000')
#         return int(lower_bound)

# if __name__ == "__main__":
#     file_path = '/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/JOB/app/DataScientist.csv'  # Ensure the file path is correct
#     target_total = 20000  # Target total number of jobs
#     duplicate_jobs_to_target(file_path, target_total)

import pandas as pd
import numpy as np
import csv

def duplicate_jobs_to_target(file_path, target_total):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(file_path)

    # Add a new column 'Relabeled Job ID' with sequential values starting from 0 up to the number of jobs minus one
    data['Relabeled Job ID'] = range(data.shape[0])

    # Extract the lower bound salary from the 'Salary Estimate' column
    data['Salary Lower Bound'] = data['Salary Estimate'].apply(extract_lower_bound)

    # Drop rows with NaN values (non-annual salaries like hourly rates)
    data = data.dropna(subset=['Salary Lower Bound'])

    # Convert the extracted salary lower bounds to integers for sorting
    data['Salary Lower Bound'] = data['Salary Lower Bound'].astype(int)

    # Determine the number of duplicates required
    current_total = data.shape[0]
    duplicates_needed = target_total - current_total

    if duplicates_needed > 0:
        # Calculate the base number of duplicates per job
        duplicates_per_job = duplicates_needed // current_total

        # Calculate any extra jobs needed to reach the exact target
        extra_needed = duplicates_needed % current_total

        # Create an array with the base number of duplicates for each job
        duplication_array = np.full((current_total,), duplicates_per_job)

        # Distribute the extra duplicates as evenly as possible
        if extra_needed > 0:
            duplication_array[:extra_needed] += 1

        # Duplicate the jobs according to the duplication_array
        data = data.loc[data.index.repeat(duplication_array + 1)]  # '+1' to include the original job

    # Reassign 'Relabeled Job ID' to ensure IDs from 0 to 19999
    data.reset_index(drop=True, inplace=True)
    data['Relabeled Job ID'] = range(data.shape[0])

    # Ensure the total number of job IDs is exactly 20000
    if data.shape[0] > target_total:
        data = data.iloc[:target_total]

    # Sort data by the lower bound of the salary
    sorted_data = data.sort_values(by='Salary Lower Bound')

    # Group jobs by 10000 salary intervals
    sorted_data['Salary Group'] = (sorted_data['Salary Lower Bound'] // 10000) * 10000

    # Write groups to a single CSV file
    with open('grouped_jobs.csv', 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(['Salary Group', 'Job IDs'])

        for group, group_data in sorted_data.groupby('Salary Group'):
            job_ids = ", ".join(map(str, group_data['Relabeled Job ID'].tolist()))
            writer.writerow([group, job_ids])

    # Output total number of jobs
    total_jobs = sorted_data.shape[0]

    # Print each job ID sorted by the lower bound of the salary estimate
    print("Sorted Job IDs by Salary Lower Bound:")
    for index, row in sorted_data.iterrows():
        print(f"Relabeled Job ID: {row['Relabeled Job ID']}, Salary Estimate: {row['Salary Estimate']}")

    print(f"Total Number of Jobs: {total_jobs}")


def extract_lower_bound(salary_estimate):
    if 'Per Hour' in salary_estimate or 'Employer est.' in salary_estimate:
        return float('nan')  # For non-annual salary formats
    else:
        lower_bound = salary_estimate.split('-')[0].replace('$', '').replace('K', '000')
        return int(lower_bound)

if __name__ == "__main__":
    file_path = '/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/JOB/app/DataScientist.csv'  # Ensure the file path is correct
    target_total = 20000  # Target total number of jobs
    duplicate_jobs_to_target(file_path, target_total)
