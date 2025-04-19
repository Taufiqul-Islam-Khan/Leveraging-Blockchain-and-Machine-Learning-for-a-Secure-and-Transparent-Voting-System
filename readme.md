# Leveraging Blockchain and Machine Learning for a Secure and Transparent Voting System

A secure and transparent electronic voting platform that integrates blockchain technology with machine learning-based biometric authentication. It enables verified voters to cast their votes digitally while ensuring that every vote is immutable, verifiable, and tamper-proof. By combining decentralized smart contracts with real-time facial recognition, this system offers a modern solution to digital election security challenges.

---

## 📘 Project Summary

This project is a prototype implementation of an e-voting system where voters are authenticated through both biometric data and national identifiers before being allowed to cast a vote. Votes are permanently recorded on the Ethereum blockchain via a smart contract, eliminating the risk of tampering or duplication. The platform is designed for academic and testing purposes and demonstrates a complete pipeline from voter registration to election result tallying.

---

## 🧠 Methodology
### 1. Biometric Verification

When attempting to vote, each user must:
- Scan their unique QR code provided at registration
- Submit a real-time facial image

### 2. Voter data Cross validation

Voters are registered using:
- Full Name, National ID (NID), Date of Birth, and Address
- A captured facial image

The image is processed to generate a facial embedding, which is stored off-chain in a local database.


The system verifies both biometric and textual credentials (DOB and NID). If both match existing records, the user gains access to the voting interface.

### 3. Election Committee Functionality

An admin portal is provided where the election committee can:
- Register or delete candidates
- Monitor the list of registered voters
- Open or close the election window
- View live vote counts during and after the election

### 4. Blockchain Voting with Smart Contracts

All votes are recorded through a Solidity-based smart contract on a local Ethereum blockchain simulated using Ganache. Once an election is closed by the admin:
- The contract blocks additional votes
- Results become publicly visible on the blockchain
- Each vote is auditable and immutable

Python’s `web3.py` library is used to integrate the smart contract with the Flask backend, enabling vote submission and contract interaction directly from the web interface.

---

## 🛠️ Technologies Used

| Layer         | Technology                   |
|---------------|------------------------------|
| Frontend      | Flask, HTML/CSS (Jinja2)     |
| Backend       | Python, Flask Framework      |
| Blockchain    | Solidity, Ganache, Web3.py   |
| ML/Verification | OpenCV, TensorFlow/Keras   |
| Data Storage  | CSV/JSON (Off-chain storage) |

---

## 🖼️ System Interface

### Voter Panel

![Voters' Activity](VoterSIDE.png)

### Election Committee Panel

![Election Committee’s Activity](ELECTIONCOMMITTEE.png)


✅ Features
Real-time QR code and facial verification

Tamper-proof voting on blockchain

Admin-controlled election management

Real-time result tracking

Smart contract-based vote recording

Voter authentication using NID and DOB

Prevention of double voting and impersonation

🧪 Testing Procedure
Run synthetic_dataset_making.py to create mock voter records.

Start Ganache and deploy the smart contract.

Launch the Flask server using python app.py.

Log in as a voter using QR code and face recognition.

Cast a vote and verify the transaction is recorded on the blockchain.

Close the election as admin and check the final results.

🔐 Data Privacy and Ethics
Facial images and embeddings are stored and processed off-chain only.

The blockchain stores vote hashes only, not voter identities.

Biometric verification occurs in real-time and is never transmitted externally.

The system design avoids storing sensitive information on-chain, in line with GDPR-style data protection guidelines.

🌱 Future Enhancements
Integration of Decentralized Identifiers (DIDs) for anonymous yet verifiable identities

Use of Zero-Knowledge Proofs (ZKPs) for eligibility verification without identity exposure

Deployment on Ethereum testnets like Goerli or Sepolia

Improved anomaly detection through ML-based pattern analysis

Mobile optimization and offline QR voter wallet support

📄 License
This project is licensed under the MIT License.
Feel free to use, modify, or extend the project with credit to the original author.

🧾 Academic Note
This system was developed as part of an academic research project titled:

"Leveraging Blockchain and Machine Learning for a Secure and Transparent Voting System"

The project demonstrates a working prototype integrating secure blockchain protocols with biometric verification to explore the potential of decentralized and tamper-proof election systems.

