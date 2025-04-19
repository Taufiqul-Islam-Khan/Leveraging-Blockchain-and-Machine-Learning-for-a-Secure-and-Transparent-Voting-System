import pandas as pd
import random
from faker import Faker

# Initialize Faker for generating random data
fake = Faker()

# Load your CSV file
df = pd.read_csv(r"C:\Users\taufi\OneDrive\Desktop\Blockchain\VoterDAtabase\VoterDetails.csv")  # replace with your actual CSV filename

# Convert 'NID' column to string to avoid dtype mismatch issues
df['NID'] = df['NID'].astype(str)

# Replace 'nan' strings (from float conversion) with actual NaNs
df['NID'].replace('nan', pd.NA, inplace=True)
df['DOB'].replace('nan', pd.NA, inplace=True)
df['Address'].replace('nan', pd.NA, inplace=True)

# Replace underscores with spaces in names
df['Name'] = df['Name'].str.replace('_', ' ')

# Fill missing fields
for index, row in df.iterrows():
    if pd.isna(row['NID']) or not row['NID'].strip():
        df.at[index, 'NID'] = str(random.randint(111111111, 999999999))
    if pd.isna(row['DOB']) or not str(row['DOB']).strip():
        df.at[index, 'DOB'] = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%d/%m/%Y')
    if pd.isna(row['Address']) or not str(row['Address']).strip():
        df.at[index, 'Address'] = fake.address().replace('\n', ', ')


# Save to new CSV
df.to_csv(r"C:\Users\taufi\OneDrive\Desktop\Blockchain\VoterDAtabase\Finalized_systhetic_dataset.csv", index=False)
