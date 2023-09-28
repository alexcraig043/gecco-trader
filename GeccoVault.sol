// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract GeccoVault {
    address public ownerA;
    address public ownerB;
    uint256 public initialValue;

    event RandomOutcome(address indexed caller, string message);

    constructor(address _ownerA, address _ownerB) payable {
        ownerA = _ownerA;
        ownerB = _ownerB;
        initialValue = msg.value;  // Setting the initial value
    }

    function transactWithVault(uint256 amount) external payable {
        require(msg.value == amount, "Sent amount doesn't match the specified amount");
        require(amount <= address(this).balance * 3 / 100, "Amount exceeds 3% of the contract balance");

        uint256 toSend;
        if (msg.sender == ownerA || msg.sender == ownerB) {
            emit RandomOutcome(msg.sender, "Success");
            toSend = amount * 2;
        } else {
            if (randomChance()) {
                emit RandomOutcome(msg.sender, "Success");
                toSend = amount * 2;
            } else {
                emit RandomOutcome(msg.sender, "Fail");
                toSend = amount / 10;
            }
        }

        // Check if after the payout the balance is less than 70% of the initial value
        if (address(this).balance - toSend < initialValue * 7 / 10) {
            payable(ownerA).transfer(address(this).balance);
            return;
        }

        payable(msg.sender).transfer(toSend);
    }

    function clearVault() external {
        require(msg.sender == ownerA || msg.sender == ownerB, "Only owners can clear the vault");
        payable(msg.sender).transfer(address(this).balance);
    }

    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }

    function addToVault() external payable {
        require(msg.value > 0, "Must send Ether to add to the vault");
    }

    function randomChance() internal view returns(bool) {
        uint256 randomValue = uint256(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, msg.sender)));
        return randomValue % 5 == 0;  // 20% chance (1 in 5)
    }

    // Fallback function to accept ether
    receive() external payable {}
}
