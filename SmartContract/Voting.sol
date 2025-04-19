// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Election {
    struct Voter {
        bool isRegistered;  // Checks if voter is registered
        bool hasVoted;      // Checks if voter has already voted
        uint votedCandidate; // Index of the voted candidate
    }

    struct Candidate {
        string name;         // Candidate name
        uint voteCount;      // Number of votes received
        uint age;            // Candidate's age
        string gender;       // Candidate's gender
        string party;        // Candidate's party
        string experience;   // Candidate's experience
        string motto;        // Candidate's motto
    }

    address public electionAdmin; // Admin of the election
    bool public electionEnded;    // Flag to indicate if election has ended
    mapping(uint => Voter) public voters; // Mapping of voter ID to voter data
    Candidate[] public candidates; // List of candidates

    event VoterRegistered(uint voterID);
    event Voted(uint voterID, uint candidateIndex);
    // event ElectionEnded(uint winningCandidateIndex, string winnerName);
    event ElectionEnded(uint winningCandidateIndex, string winnerName, uint winningVoteCount);

    modifier onlyAdmin() {
        require(msg.sender == electionAdmin, "Only admin can perform this action");
        _;
    }

    modifier onlyRegisteredVoter(uint voterID) {
        require(voters[voterID].isRegistered, "Voter is not registered");
        _;
    }

    modifier electionNotEnded() {
        require(!electionEnded, "Election has already ended");
        _;
    }

    modifier electionHasEnded() {
        require(electionEnded, "Election has not ended yet");
        _;
    }

    constructor(string[] memory candidateNames) {
        electionAdmin = msg.sender;
        electionEnded = false; // Set election as ongoing initially

        // Add candidates by the admin
        for (uint i = 0; i < candidateNames.length; i++) {
            candidates.push(Candidate({
                name: candidateNames[i],
                voteCount: 0,
                age: 0,          // Default age
                gender: "",      // Default gender
                party: "",       // Default party
                experience: "",  // Default experience
                motto: ""        // Default motto
            }));
        }
    }

    // Admin adds a candidate with name, age, gender, party, experience, and motto
    function addCandidate(
        string memory candidateName, 
        uint candidateAge, 
        string memory candidateGender, 
        string memory candidateParty, 
        string memory candidateExperience, 
        string memory candidateMotto
    ) 
        public 
        onlyAdmin 
        electionNotEnded 
    {
        candidates.push(Candidate({
            name: candidateName,
            voteCount: 0,
            age: candidateAge,
            gender: candidateGender,
            party: candidateParty,
            experience: candidateExperience,
            motto: candidateMotto
        }));
    }

    // Admin registers a voter (unique voter ID)
    function registerVoter(uint voterID) public onlyAdmin electionNotEnded {
        require(!voters[voterID].isRegistered, "Voter is already registered");
        voters[voterID] = Voter(true, false, 0);
        emit VoterRegistered(voterID);
    }

    // Voter votes for a candidate
    function vote(uint voterID, uint candidateIndex) public onlyRegisteredVoter(voterID) electionNotEnded {
        Voter storage sender = voters[voterID];
        require(!sender.hasVoted, "You have already voted");
        require(candidateIndex < candidates.length, "Invalid candidate index");

        sender.hasVoted = true;
        sender.votedCandidate = candidateIndex;
        candidates[candidateIndex].voteCount += 1;

        emit Voted(voterID, candidateIndex);
    }

    // Get the list of candidates
    function getCandidateList() public view returns (Candidate[] memory) {
        return candidates;
    }

    // // End the election and prevent further voting
    // function endElection() public onlyAdmin electionNotEnded {
    //     electionEnded = true;
        
    //     // Determine the winner
    //     (uint winningVoteCount, string memory winnerName) = getWinner();
    //     emit ElectionEnded(winningCandidateIndex, winnerName);
    // }
    // End the election and prevent further voting
    function endElection() public onlyAdmin electionNotEnded {
        electionEnded = true;
        
        // Determine the winner
        (uint winningCandidateIndex, string memory winnerName, uint winningVoteCount) = getWinner();
        emit ElectionEnded(winningCandidateIndex, winnerName, winningVoteCount);
    }

    // // Get the winner based on votes
    // function getWinner() public view electionHasEnded returns (uint winningVoteCount, string memory winnerName) {
    //     uint winningVoteCount = 0;
    //     for (uint i = 0; i < candidates.length; i++) {
    //         if (candidates[i].voteCount > winningVoteCount) {
    //             winningVoteCount = candidates[i].voteCount;
    //             winningCandidateIndex = i;
    //         }
    //     }
    //     winnerName = candidates[winningCandidateIndex].name;
    // }

    // Get the winner based on votes
    function getWinner() public view electionHasEnded returns (uint winningCandidateIndex, string memory winnerName, uint winningVoteCount) {
        winningVoteCount = 0;
        for (uint i = 0; i < candidates.length; i++) {
            if (candidates[i].voteCount > winningVoteCount) {
                winningVoteCount = candidates[i].voteCount;
                winningCandidateIndex = i;
            }
        }
        winnerName = candidates[winningCandidateIndex].name;
    }
}
