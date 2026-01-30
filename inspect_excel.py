import pandas as pd
import os

file_path = "schedule.xlsx"
print(f"Checking {file_path}...")

if not os.path.exists(file_path):
    print("File not found!")
    exit(1)

try:
    # Load the Excel file
    df = pd.read_excel(file_path)
    
    print("--- Excel File Inspection ---")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    for col in df.columns:
        print(f"- {str(col)}")
        
    print("\nFirst 5 rows:")
    print(df.head().to_string())
    
except Exception as e:
    print(f"Error reading Excel file: {e}")
