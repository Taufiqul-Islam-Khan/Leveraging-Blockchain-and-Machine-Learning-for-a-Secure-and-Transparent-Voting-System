import csv
import json
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import json
# Load candidate data from CSV
def load_candidates():
    candidates = []
    with open(r'C:\Users\taufi\OneDrive\Desktop\Blockchain\CandidateList\candidates_list.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            candidates.append(row)
    return candidates

# Display candidates to the voter
def display_candidates(candidates):
    print("Please choose your candidate by ID:")
    for candidate in candidates:
        print(f"ID: {candidate['id']}, Name: {candidate['name']}, Party: {candidate['party']}, Motto: {candidate['motto']}")

# Allow voter to vote
def cast_vote(candidates):
    vote = input("Enter the candidate ID to vote for: ")
    # Validate the vote
    valid_candidate = next((candidate for candidate in candidates if candidate["id"] == vote), None)
    
    if valid_candidate:
        print(f"Vote casted for {valid_candidate['name']} ({valid_candidate['party']})")
        # Here you should update the voting status and record the vote (in database or CSV)
        return vote
    else:
        print("Invalid candidate ID. Please try again.")
        return cast_vote(candidates)

# Example process flow
def voter_process(qr_code):
    # Simulate QR Code scanning and voter verification
    voter_data={}
    image = cv2.imread(qr_code)
    decoded_objects = decode(image)
    # qr_data = decoded_objects[0].data.decode("utf-8")
    # voter_data = json.loads(qr_data)
    # print("Decoded Voter Data:", voter_data)
    if decoded_objects:
        qr_data = decoded_objects[0].data.decode("utf-8")  # Extract the data as a string
        try:
            voter_data = json.loads(qr_data)  # Convert JSON string to a dictionary
            print("Decoded Voter Data:", voter_data)
        except :
            print("QR code does not contain valid JSON data:", qr_data)
    else:
        print("No QR code found in the image.")

    if voter_data["has_voted"] == False:
        print("Voter verified. Proceed to vote.")
        candidates = load_candidates()
        display_candidates(candidates)
        
        # Voter casts their vote
        selected_candidate_id = cast_vote(candidates)
        
        # Update the voter's status to 'hasVoted = True' (in database)
        voter_data["has_voted"] = True
        print(f"Vote successfully cast for candidate ID {selected_candidate_id}.")
        # Update the QR data to reflect the new status (or store this update in your database)
        
    else:
        print("This voter has already voted.")


