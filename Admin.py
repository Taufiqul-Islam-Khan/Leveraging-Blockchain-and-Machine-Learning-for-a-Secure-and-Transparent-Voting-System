import csv
from web3 import Web3
import json
import json
from flask import Flask, render_template, request, jsonify
from web3 import Web3
from solcx import compile_standard
# Connect to local Ganache Ethereum network
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))
assert w3.is_connected(), "Unable to connect to Ganache."

# Read the Solidity contract
with open('SmartContract/Voting.sol', 'r') as file:
    contract_source = file.read()

# Compile the contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "SmartContract/Voting.sol": {
            "content": contract_source
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": [
                    "abi",
                    "metadata",
                    "evm.bytecode",
                    "evm.sourceMap"
                ]
            }
        },
    },
}, solc_version="0.8.0")

#Admin deploying the smart Contract=======================================
contract_data = compiled_sol['contracts']['SmartContract/Voting.sol']['Election']
abi = contract_data['abi']
bytecode = contract_data['evm']['bytecode']['object']
# Set transaction details For deployment This can be the admin address to make candidate and all admin related task
chain_id = 1337
my_address = "0xF0A861D698FEFffB3681FA5256cB0F24d061f47B"
private_key = "0x2520c26702aef34c6206ef44516ae3b48d8e97a3e9e15624248523ce52594c44"

candidate_name=[]
with open('CandidateList/candidates_list.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        candidate_name.append(row['name'])

# Deploy the contract
def deploy_contract():
    # Create contract instance
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    # nonce = w3.eth.get_transaction_count(my_address)
    transaction = contract.constructor(candidate_name).build_transaction({
        'from': my_address,
        'gas': 5000000,
        'gasPrice': w3.to_wei('10', 'gwei'),
        'nonce': w3.eth.get_transaction_count(my_address)
    })

    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    print (signed_txn)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print (txn_hash)
    # Wait for transaction receipt
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    print (txn_receipt)
    print(f"Contract deployed at address: {txn_receipt.contractAddress}")
    contract_details = {
                "address": txn_receipt.contractAddress,
                "abi": abi
            }
    with open('deployed_contract.json', 'w') as f:
            json.dump(contract_details, f)
    return txn_receipt.contractAddress
# # Deploy the contract
# contract_address = deploy_contract()
# #Deployed Contract Instance
# contract = w3.eth.contract(address=contract_address, abi=abi)

# # Save contract details (address and ABI) to a JSON file for later use
# contract_details = {
#         "address": contract_address,
#         "abi": abi
#     }

# with open('deployed_contract.json', 'w') as f:
#         json.dump(contract_details, f)
