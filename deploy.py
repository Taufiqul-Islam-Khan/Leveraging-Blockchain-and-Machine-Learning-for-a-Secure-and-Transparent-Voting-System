import json
from solcx import compile_standard
import solcx
solcx.install_solc('0.6.0')
from web3 import Web3

# Read the Solidity contract
with open('Voting.sol', 'r') as file:
    contract_source = file.read()

# Compile the contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "Voting.sol": {
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
}, solc_version="0.6.0")

# Save compiled contract
with open('compiled_file.json', 'w') as file:
    json.dump(compiled_sol, file)

# Extract ABI and Bytecode
contract_data = compiled_sol['contracts']['Voting.sol']['Voting']
abi = contract_data['abi']
bytecode = contract_data['evm']['bytecode']['object']

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))
if w3.is_connected():
    print("-" * 50)
    print("Connection Successful")
    print("-" * 50)
else:
    print("Connection Failed")
    exit()

# Set transaction details
chain_id = 1337
my_address = "0x2Bc1a58e1A88C62048d8b38b410cF84013648f8e"
private_key = "0x3491c8f08ed0c49defe9ed794b9887674741b4a0c40a0f913e5298c46a4e066c"


# Create contract instance
Voting = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(my_address)


# Build and sign transaction
transaction = Voting.constructor().build_transaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce,
    "gas": 6721975,
    "gasPrice": w3.to_wei('10', 'gwei')
})
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

# Send transaction
print("Deploying Contract!")
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

# Wait for transaction receipt
print("Waiting for transaction to be mined...")
txn_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Get deployed contract address
contract_address = txn_receipt.contractAddress
print(f"Done! Contract deployed to {contract_address}")


# Interact with contract
Voting = w3.eth.contract(address=contract_address, abi=abi)
# Example function call (change `retrieve` to an actual function from your contract)
try:
    print(Voting.functions.retrieve().call())
except Exception as e:
    print(f"Error calling function: {e}")

# Retrieve initial stored value (Ensure 'retrieve()' is an actual function in your contract)
print(f"Initial Stored Value: {Voting.functions.retrieve().call()}")

# Get updated nonce
updated_nonce = w3.eth.get_transaction_count(my_address)


# Create a transaction to store a new value (Assuming `store(uint256)` is a valid function)
greeting_transaction = Voting.functions.store(15).build_transaction({
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": my_address,
    "nonce": updated_nonce,  # Ensure correct nonce usage
    "gas": 1000000  # Provide sufficient gas
})

# Sign the transaction
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)

# Send the signed transaction
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.raw_transaction)

print("Updating stored Value...")

# Wait for the transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

# Retrieve updated value
print(f"Updated Stored Value: {Voting.functions.retrieve().call()}")
