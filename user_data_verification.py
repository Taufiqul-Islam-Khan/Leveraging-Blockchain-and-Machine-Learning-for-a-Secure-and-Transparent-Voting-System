# user_data_verification.py
import pandas as pd
from datetime import datetime

# Function to verify if provided details match the CSV record and check if the user is above 18 years
def verify_user_data(name, nid, dob, address, verified_image_folder, csv_file=r'VoterDAtabase\VoterDetails.csv'):
    # Load CSV with user data
    print (verified_image_folder)
    df = pd.read_csv(csv_file)
    # Convert necessary columns to string and strip extra spaces
    df['Name'] = df['Name'].astype(str).str.strip().str.lower()
    df['NID'] = df['NID'].astype(str).str.strip().str.lower()
    print ("------------------")
    # Normalize the input for comparison (strip spaces and lower case)
    name = name.strip().lower()
    nid = nid.strip().lower()
    print (name)
    print (nid)
    # if df['has_voted'] is True:
    #     print ("This voter Already Gave Vote")
    #     return False
    
    # Check if the user exists in the CSV file by matching name and NID
    matched_row = df[(df['Name'] == name) & (df['NID'] == nid)]
    print (matched_row)
    
    if not matched_row.empty:
        # Extract the stored details from the CSV
        stored_dob = matched_row['DOB'].values[0]
        stored_address = matched_row['Address'].values[0]
        stored_folder=matched_row['image_folder'].values[0]
        
        # Check if the address matches
        if stored_address.strip().lower() != address.strip().lower():
            print("Address does not match.")
            return False
        
        # Check if the age is 18 or older
        user_dob = datetime.strptime(dob, "%Y-%m-%d")
        current_date = datetime.today()
        age = current_date.year - user_dob.year - ((current_date.month, current_date.day) < (user_dob.month, user_dob.day))
        
        if age < 18:
            print("User is below 18 years old.")
            return False
        
        # Check if DOB matches (to ensure correctness)
        if stored_dob != dob:
            print("DOB does not match.")
            return False
        if verified_image_folder != stored_folder:
            print("You are giving another Person's data")
            return False
        print("All details match.")
        return True  # All checks passed
    
    
    print("No match found in CSV.")
    return False  # No match in CSV
