from web3 import Web3
import json

# Connect to Ethereum network (local or testnet)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Local node URL
w3.eth.defaultAccount = w3.eth.accounts[0]  # Set default account (admin)

# Contract ABI and address (you get this after deploying the contract)
contract_abi = json.loads('[...]')  # Replace with actual ABI from Remix
contract_address = '0xYourContractAddressHere'

# Connect to contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Function to register a voter
def register_voter(user_id, voter_address):
    tx = contract.functions.registerVoter(user_id, voter_address).buildTransaction({
        'gas': 2000000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': w3.eth.getTransactionCount(w3.eth.defaultAccount),
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key='your_private_key')
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(f"Voter registered: {tx_hash.hex()}")

# Function to register a candidate
def register_candidate(candidate_id, name, party, motto):
    tx = contract.functions.registerCandidate(candidate_id, name, party, motto).buildTransaction({
        'gas': 2000000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': w3.eth.getTransactionCount(w3.eth.defaultAccount),
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key='your_private_key')
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(f"Candidate registered: {tx_hash.hex()}")

# Function to vote for a candidate
def vote(candidate_id):
    tx = contract.functions.vote(candidate_id).buildTransaction({
        'gas': 2000000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': w3.eth.getTransactionCount(w3.eth.defaultAccount),
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key='your_private_key')
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(f"Vote cast: {tx_hash.hex()}")

# Function to get election results
def get_results():
    result = contract.functions.getElectionResults().call()
    print(f"Winner: {result[0]}, Votes: {result[1]}")

# Example Usage
register_voter(123456789, '0xVoterAddressHere')
register_candidate(1, 'John Doe', 'Democratic Party', 'For a better future this way')
vote(1)
get_results()
