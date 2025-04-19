import csv

# Sample candidate data with party names
candidates = [
    {"id": 1, "name": "John Doe", "party": "Democratic Party", "age": 45, "gender": "Male", "experience": "10 years", "motto": "For a better future"},
    {"id": 2, "name": "Jane Smith", "party": "Republican Party", "age": 38, "gender": "Female", "experience": "8 years", "motto": "Together for progress"},
    {"id": 3, "name": "Robert Brown", "party": "Green Party", "age": 50, "gender": "Male", "experience": "15 years", "motto": "Leadership for all"},
    {"id": 4, "name": "Emily White", "party": "Libertarian Party", "age": 42, "gender": "Female", "experience": "12 years", "motto": "Change for betterment"},
    {"id": 5, "name": "Michael Johnson", "party": "Socialist Party", "age": 47, "gender": "Male", "experience": "18 years", "motto": "Power to the people"},
    {"id": 6, "name": "Sarah Lee", "party": "Progressive Party", "age": 34, "gender": "Female", "experience": "6 years", "motto": "Innovation for growth"},
]

# Define the CSV file path
csv_file = r"C:\Users\taufi\OneDrive\Desktop\Blockchain\CandidateList\candidates_list.csv"

# Write candidate data to CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["id", "name", "party", "age", "gender", "experience", "motto"])
    writer.writeheader()  # Write the header row
    for candidate in candidates:
        writer.writerow(candidate)

print(f"CSV file '{csv_file}' has been created with candidate data.")
