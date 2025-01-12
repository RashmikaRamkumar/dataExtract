import pandas as pd

# Load the Excel file
file_path = r"E:\windy\weather_data_1.xlsx"  # Replace with your file path
df = pd.read_excel(file_path, header=None)


# Select the required rows (9, 10, 12, 13) while keeping the headers
filtered_df = df.iloc[[8, 9, 11, 12]]

# Save the filtered data to a new Excel file (optional)
filtered_file_path = "filtered_file_with_headers.xlsx"  # Replace with your desired output file name
filtered_df.to_excel(filtered_file_path, index=False)

print("Filtered rows with headers saved to", filtered_file_path)