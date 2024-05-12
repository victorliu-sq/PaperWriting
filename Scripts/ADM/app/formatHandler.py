import pandas as pd

# Define the file path
file_path = '/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/ADM/app/Expanded_Admission.csv'

# Load the dataset
data = pd.read_csv(file_path)

# List of columns that should be integers
int_cols = ['GRE Score', 'TOEFL Score', 'University Rating', 'Research']

# Apply integer conversion and rounding where necessary
for col in int_cols:
    data[col] = data[col].round().astype(int)

# Rounding CGPA and Chance of Admit to two decimal places
data['CGPA'] = data['CGPA'].round(2)
data['Chance of Admit '] = data['Chance of Admit '].round(2)

data['University Rating']=data['University Rating'].round(1)
data['SOP']=data['SOP'].round(1)
data['LOR ']=data['LOR '].round(1)

# Save the cleaned data back to CSV
data.to_csv('Formatted_Expanded_Admission_Predict.csv', index=False)

print("Data has been formatted and saved successfully.")
