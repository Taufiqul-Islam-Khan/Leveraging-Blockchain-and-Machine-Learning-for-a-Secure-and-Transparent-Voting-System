# Leveraging Blockchain and Machine Learning for a Secure and Transparent Voting System

This project introduces a full-stack e-voting platform that integrates **blockchain technology** with **machine learning-based facial recognition** to ensure secure, verifiable, and privacy-conscious electoral processes. Designed with decentralization, voter identity protection, and tamper-resistance in mind, the system enables authenticated individuals to cast immutable votes through a smart contract governed interface—backed by real-time biometric verification.

---

## 🖼️ System Interface

### Voter Interaction Panel

![Voters' Activity](VoterSIDE.png)

### Election Committee Dashboard

![Election Committee’s Activity](ELECTIONCOMMITTEE.png)

These panels represent the distinct workflows for voters and election officials—covering identity validation, vote submission, candidate management, and result auditing.

---

## 🛠️ Technologies Implemented

| Component       | Stack                            |
|------------------|----------------------------------|
| Web Interface    | Flask, HTML5/CSS (Jinja2 Templating) |
| Application Logic| Python (Flask MVC Framework)     |
| Blockchain Layer | Solidity, Ganache, Web3.py       |
| Biometric Auth   | FaceNet (TensorFlow/Keras), OpenCV |
| Data Storage     | Local Files (CSV/JSON)           |

The application uses `web3.py` to bridge the Python-based backend with the Ethereum blockchain, allowing seamless interaction with deployed smart contracts during voting operations.

---

## ✅ Key Features

- 🔒 **QR-based voter login** linked to verified facial identity  
- 🧠 **Facial recognition authentication** using FaceNet embeddings  
- ⛓️ **Ethereum smart contract** for secure, irreversible vote recording  
- 📊 **Live result dashboards** updated in real time  
- 🧾 **Election committee tools** for candidate entry, voter authorization, and result finalization  
- 🧩 **Biographical validation** using synthetic registry (NID, DOB, Address)  
- 🛡️ **Prevention of duplicate voting and identity spoofing**

---

## 🧪 Testing Guidelines

To deploy and test this system in a local development environment:

1. **Generate sample data**: Run `synthetic_dataset_making.py` to synthesize voter records and face associations  
2. **Launch Ganache**: Start a local Ethereum instance with test accounts  
3. **Deploy smart contract**: Use the election committee interface to deploy and initialize the contract  
4. **Configure Web3**: Update contract address and ABI in the backend configuration  
5. **Run application**: Execute `python app.py` to launch the Flask server  
6. **Use browser interface**: Access voter/admin portals, authenticate via QR and facial scan, and simulate voting  
7. **End election**: Observe real-time vote tally and system logs after election closure  

---

## 🔐 Privacy Considerations

- Facial embeddings are used transiently for matching; raw biometric images are neither stored on-chain nor persisted  
- The blockchain ledger stores anonymized, hashed votes—ensuring that ballots cannot be linked back to voters  
- Personal data is validated off-chain, mitigating exposure risks and adhering to privacy laws such as **GDPR**  
- Voter session access is tightly bound to QR codes generated post-verification, adding a secondary authentication layer  

---

## 🌱 Future Improvements

- 🔐 Integration of **Decentralized Identifiers (DIDs)** to strengthen identity portability and privacy  
- 🧾 Adoption of **Zero-Knowledge Proofs (ZKPs)** for privacy-preserving eligibility verification  
- 🌐 Deployment to public testnets such as **Goerli**, **Sepolia**, or **Polygon Mumbai**  
- 📉 Implementation of ML-based **voting anomaly detection**  
- 📱 Mobile platform support with **offline QR credential scanning**

---

## 📄 License

Distributed under the **MIT License**.  
You are free to use, modify, and build upon this project for academic, research, or non-commercial purposes. Please attribute original contributions accordingly.

---

## 🧾 Research Statement

This repository was developed as part of a graduate research initiative under the title:

**"Leveraging Blockchain and Machine Learning for a Secure and Transparent Voting System"**

The project aims to empirically explore how decentralized blockchain infrastructure and facial biometric authentication can jointly address the challenges of digital voter verification, tamper-proof ballot recording, and transparent result auditing. By demonstrating a hybrid on-chain/off-chain architecture, this work advances practical solutions for future digital democracies and regulatory-compliant electronic voting environments.
