import atexit
import csv
import os
import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_from_directory
from web3 import Web3
import json
from solcx import compile_standard
from web3.exceptions import Web3RPCError
from FaceVerification import is_same_person, capture_image
from user_data_verification import verify_user_data
from generate_qr_code import generate_qr_code
from DisplayCandidate import voter_process
from werkzeug.utils import secure_filename
from pyzbar.pyzbar import decode
from PIL import Image
from Admin import deploy_contract
import threading
verified_image_folder=''
lock = threading.Lock()


app = Flask(__name__)
app.secret_key = 'my_super_secret_key' 

# Connect to local Ganache Ethereum network
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))
assert w3.is_connected(), "Unable to connect to Ganache."


admin_address = "0xF0A861D698FEFffB3681FA5256cB0F24d061f47B"
private_key = "0x2520c26702aef34c6206ef44516ae3b48d8e97a3e9e15624248523ce52594c44"

if not os.path.exists('deployed_contract.json'):
        # Deploy the contract
        deployed_contract_address = deploy_contract()
else:
        print("Deployed contract details found.")

# Load the deployed contract's ABI and address
with open('deployed_contract.json', 'r') as f:
    contract_details = json.load(f)

contract_address = contract_details['address']
abi = contract_details['abi']

contract = w3.eth.contract(address=contract_address, abi=abi)

# Admin login functionality
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'adminpassword':  # Admin credentials
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('admin_login.html')


# Admin dashboard to manage the election
@app.route('/admin/dashboard')
def admin_dashboard():
    candidates = contract.functions.getCandidateList().call()
    return render_template('admin_dashboard.html', candidates=candidates)

def append_to_csv(candidate_data):
    file_name = "CandidateList/candidates_list.csv"
    
    # Get the last ID from the CSV file and increment it
    try:
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            last_row = list(reader)[-1]  # Get the last row of the CSV
            last_id = int(last_row[0])  # Assuming ID is the first column
            new_id = last_id + 1  # Increment the ID for the new candidate
    except (FileNotFoundError, IndexError):
        # If the file doesn't exist or is empty, start with ID = 1
        new_id = 1

    # Prepare the data to append, including the new ID
    candidate_data_with_id = [new_id] + candidate_data

    # Append the candidate data to the CSV file
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the candidate data
        writer.writerow(candidate_data_with_id)

        
@app.route('/admin/add_candidate', methods=['POST'])
def add_candidate():
    try:
        # Get the data from the form
        candidate_name = request.form['candidate_name']
        candidate_age = int(request.form['candidate_age'])  # Convert age to integer
        candidate_gender = request.form['candidate_gender']
        candidate_party = request.form['candidate_party']
        candidate_experience = request.form['candidate_experience']
        candidate_motto = request.form['candidate_motto']

        # Build the transaction for adding a candidate
        add_candidate_txn = contract.functions.addCandidate(
            candidate_name, 
            candidate_age, 
            candidate_gender, 
            candidate_party,
            candidate_experience, 
            candidate_motto
        ).build_transaction({
            'from': admin_address,
            'gas': 200000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': w3.eth.get_transaction_count(admin_address)
        })

        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(add_candidate_txn, private_key)

        # Send the transaction
        txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Flash success message
        flash(f'Candidate "{candidate_name}" has been successfully added!', 'success')
                # Candidate data to be appended
        candidate_data = [
            candidate_name,
            candidate_party, 
            candidate_age, 
            candidate_gender, 
            candidate_experience, 
            candidate_motto
        ]

        # Append candidate data to the CSV
        append_to_csv(candidate_data)

    except Web3RPCError as e:
        # Handle Web3 errors
        error_message = e.args[0]
        error_dict = json.loads(error_message.replace("'", '"'))  # Convert single quotes to double quotes
        reason = error_dict.get("data", {}).get("reason", "Unknown error")  # Extract reason
        flash(f"Error: {reason}", "error")  # Flash the error message in Flask
        print(f"Error: {reason}", "error")
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/register_voter', methods=['POST'])
def register_voter():
        try:
            voter_id = int(request.form['voter_id'])
            txn = contract.functions.registerVoter(int(voter_id)).build_transaction({
                'from': admin_address,
                'gas': 200000,
                'gasPrice': w3.to_wei('10', 'gwei'),
                'nonce': w3.eth.get_transaction_count(admin_address)
            })
            signed_txn = w3.eth.account.sign_transaction(txn, private_key)
            txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            flash(f'Voter "{voter_id}" has been successfully Registered!', 'success')
        except Web3RPCError as e:
            error_message=e.args[0]
            error_dict = json.loads(error_message.replace("'", '"'))  # Convert single quotes to double quotes
            reason = error_dict.get("data", {}).get("reason", "Unknown error")  # Extract reason
            flash(f"Error: {reason}", "error")  # Flash the error message in Flask
            print(f"Error: {reason}", "error")
        return redirect(url_for('admin_dashboard')) 



@app.route('/admin/end_election', methods=['POST'])
def end_election():
    try:
        txn = contract.functions.endElection().build_transaction({
            'from': admin_address,
            'gas': 200000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': w3.eth.get_transaction_count(admin_address)
        })
        signed_txn = w3.eth.account.sign_transaction(txn, private_key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        flash(f'Election has been Ended!', 'success')
    except Web3RPCError as e:
        error_message=e.args[0]
        error_dict = json.loads(error_message.replace("'", '"'))  # Convert single quotes to double quotes
        reason = error_dict.get("data", {}).get("reason", "Unknown error")  # Extract reason
        flash(f"Error: {reason}", "error")  # Flash the error message in Flask
        print(f"Error: {reason}", "error")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/get_winner')
def get_winner():
    
    winner = contract.functions.getWinner().call()
    winner_name = winner[1]
    vote_count = winner[2]
    return render_template('show_winner.html', winner_name=winner_name, vote_count=vote_count)
    

pool_of_voter_address_and_key = {
    "0x61109E6673a81F4836aDB1df61445606De32379E": "0xe6a4af79bd221936ce11162b6ffbf474d87b94a8fb4f55e7816d69a3860243d6",
    "0x83aE2108973020a8Daa6284F2B88d3ed7b4a8063": "0x22ffb39b37fbb1faaf8570b998afffd084944fd5967af0739372dc844af76126"
   }
# Dictionary to track assigned voters
assigned_voters = {}  # voter_id -> (address, private_key)

#VOTER WORKS START HERE 
# Define the upload folder and ensure it exists
app.config[r'UPLOAD_FOLDER'] = 'uploads'  # You can change this to any directory path you want to use
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
# Make sure the folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def voter_welcome():
    return render_template('voter_welcome.html')

@app.route('/voter/verify', methods=['GET', 'POST'])
def voter_verify():
    if request.method == 'POST':
        verification_method = request.form.get('verification_method')

        if verification_method == 'upload' and 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No file selected.', 'error')
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            is_verified = is_same_person(file_path)
        
        elif verification_method == 'capture':
            file_path = capture_image()  # Capture from webcam
            is_verified = is_same_person(file_path) if file_path else False

        else:
            flash('Invalid verification method.', 'error')
            return redirect(url_for('voter_verify'))

        if is_verified:
            print (is_verified)
            
            session["image_folder"] = is_verified # Store value in session
            flash('Face verification successful! Proceed to vote.', 'success')
            session['flash_message'] = 'Face verification successful! Proceed to User Data Verification.'
            return redirect(url_for('voter_data_verify'))
        else:
            flash('Face verification failed. Please try again.', 'error')
            return redirect(url_for('voter_verify'))

    return render_template('voter_verify.html')



@app.route('/voter/data_verify', methods=['GET', 'POST'])
def voter_data_verify():
    flash_message = session.pop('flash_message', None)  
    print (session["image_folder"])
    if request.method == 'POST':
        name = request.form['name']
        nid = request.form['nid']
        dob = request.form['dob']
        address = request.form['address']

        if verify_user_data(name, nid, dob, address,session["image_folder"]):
            flash('Voter data verification successful! Proceed to login.', 'success')
            session['flash_message'] = 'Voter data verification successful! Proceed to login.', 'success'
            # Generate QR code for the voter after data verification
            voter_id = nid  # Use NID or another unique identifier as the user ID
            qr_path = generate_qr_code(voter_id, name)
                # Store user name in session
            session['user_name'] = name 
            session['qr_file'] = qr_path
            
            return redirect(url_for('generate_qr_page', user_id=voter_id)) 

            # return redirect(url_for('voter_login'))
        else:
            flash('Voter data verification failed. Please check your details and try again.', 'error')
            return redirect(url_for('voter_data_verify'))

    return render_template('voter_data_verify.html', flash_message=flash_message)
# # Directory for QR codes
qr_folder = 'static/qr_codes'


# Route to display the QR code after successful verification
@app.route('/generate_qr_page/<user_id>')
def generate_qr_page(user_id):
    # Retrieve the QR file path from the session
    qr_file_path = session.get('qr_file')
    user_name = session.get('user_name')
    if not qr_file_path:
        return redirect(url_for('verify_user_data'))  # Redirect to verification if no QR file found
    print (qr_file_path)
    # Render the page with the QR code
    stripped_qr_filename = qr_file_path.replace('static/', '', 1)
    return render_template('generate_qr_code.html', qr_file=stripped_qr_filename,  user_id=user_id, user_name=user_name)

# Route to handle QR code download
@app.route('/download_qr_code')
def download_qr_code():
    # Retrieve the QR code file path from the session
    qr_file = session.get('qr_file')
    if not qr_file:
        return redirect(url_for('verify_user_data'))  # Redirect if no QR file found

    # Serve the file for download
    return send_from_directory(os.path.dirname(qr_file) , os.path.basename(qr_file), as_attachment=True)

def extract_qr_code_id(file_path):
    """
    Extract the ID from a QR code image file.
    """
    # Open the image using Pillow
    image = Image.open(file_path)
    
    # Decode the QR code
    decoded_objects = decode(image)
    
    # Assuming the QR code contains only one decoded object (the ID)
    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')  # Decode bytes to string
        voter_data = json.loads(qr_data)
        return int(voter_data['user_id'])  # The ID stored in the QR code
    
    return None  # Return None if no QR code was found


# Voter login functionality
@app.route('/voter/login', methods=['GET', 'POST'])
def voter_login():
    flash_message = session.pop('flash_message', None) 
    # flash_message = session.pop('flash_message', None)
    
    if request.method == 'POST':
        # Check if a QR code is uploaded
        if 'qr_code' in request.files:
            qr_code_file = request.files['qr_code']
            
            if qr_code_file.filename == '':
                flash('No file selected.', 'error')
                return redirect(request.url)

            # Secure and save the uploaded QR code image
            filename = secure_filename(qr_code_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            qr_code_file.save(file_path)

            # Extract the voter ID from the QR code
            voter_id = extract_qr_code_id(file_path)
            
            if not voter_id:
                flash('Invalid QR code. Please try again.', 'error')
                return redirect(url_for('voter_login'))
        else:
            # If no QR code uploaded, use the manually entered voter ID
            voter_id = request.form['voter_id']

    # if request.method == 'POST':
    #     voter_id = int(request.form['voter_id'])

        # Check if the voter is registered in the smart contract
        is_registered = contract.functions.voters(voter_id).call()[0]
        
        if is_registered:
            # If the voter already has an assigned address, redirect to voting
            if voter_id in assigned_voters:
                return redirect(url_for('vote', voter_id=voter_id))
            
            # If the voter is new, assign an available address
            if pool_of_voter_address_and_key:
                voter_address, voter_private_key = pool_of_voter_address_and_key.popitem()
                assigned_voters[voter_id] = (voter_address, voter_private_key)
                return redirect(url_for('vote', voter_id=voter_id))
            else:
                return "No available voter addresses. Please contact the admin.", 403

        return "Voter not registered", 401
    
    return render_template('voter_login.html', flash_message=flash_message)

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/voter/<int:voter_id>', methods=['GET', 'POST'])
def vote(voter_id):

        # Ensure voter is assigned an address before voting
        if voter_id not in assigned_voters:
            return "Voter ID not assigned an address. Please log in again.", 401
        
        voter_address, voter_private_key = assigned_voters[voter_id]
        candidates_list = contract.functions.getCandidateList().call()  # Retrieve candidates from smart contract
        
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'vote':  # Voter chooses to vote
                candidate_index = int(request.form['candidate_index'])  # Get the selected candidate index
                
                # Call the contract to vote
                txn = contract.functions.vote(voter_id, candidate_index).build_transaction({
                    'from': voter_address,
                    'gas': 200000,
                    'gasPrice': w3.to_wei('10', 'gwei'),
                    'nonce': w3.eth.get_transaction_count(voter_address)
                })
                signed_txn = w3.eth.account.sign_transaction(txn, voter_private_key)
                txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
                
                print(f"Voter {voter_id} voted for candidate {candidate_index}, tx hash: {txn_hash.hex()}")
            return redirect(url_for('thank_you'))
        return render_template('voter_dashboard.html', voter_id=voter_id, candidates=candidates_list)

@app.route('/candidate/<int:candidate_id>/<int:voter_id>', methods=['GET'])
def candidate_details(candidate_id, voter_id):
    # Load candidate details from CSV
    df = pd.read_csv("CandidateList/candidates_list.csv")
    candidate_data = df[df['id'] == candidate_id].to_dict(orient='records')
    if not candidate_data:
        return "Candidate not found", 404

    return render_template('candidate_details.html', candidate=candidate_data[0], voter_id=voter_id)


if __name__ == '__main__':
    app.run(debug=True)
    
