from web3 import Web3
from decouple import config
import time

# Wallet info
ownerA = "0xf003840C1F232300AF202C439Dc6336bdcaae4C7"
ownerB = "0xA0337a9C491e111B6a0a18EcA7436C1BcDFEa8A1"
throwaway = "0x550D6A444696B0C018430A31C748631D0fCC7C52"
private_key = config("Throwaway_Private_Key")

# Connect to Ethereum node
infura_api_key = config("INFURA_API_KEY")
w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{infura_api_key}"))

# Setting up your account
w3.eth.defaultAccount = throwaway

# Set up the contract
contract_address = Web3.to_checksum_address(
    "0x35F6b8d02340fFB9d66104f71c0E01b2e9EC3ABD"
)
contract_abi = [
    {
        "inputs": [],
        "name": "addToVault",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "clearVault",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "transactWithVault",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_ownerA", "type": "address"},
            {"internalType": "address", "name": "_ownerB", "type": "address"},
        ],
        "stateMutability": "payable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "caller",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "message",
                "type": "string",
            },
        ],
        "name": "RandomOutcome",
        "type": "event",
    },
    {"stateMutability": "payable", "type": "receive"},
    {
        "inputs": [],
        "name": "getContractBalance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "initialValue",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "ownerA",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "ownerB",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def bait_frontrunner(amount_in_ether):
    amount_in_wei = w3.to_wei(amount_in_ether, "ether")

    # Estimate gas for the function call (using the manual value for now)
    gas_estimate = 56000

    # Encode the function call
    function_data = contract.encodeABI(
        fn_name="transactWithVault", args=[amount_in_wei]
    )

    # Construct the transaction
    transaction = {
        "to": contract_address,
        "value": amount_in_wei,
        "gas": gas_estimate,
        "gasPrice": w3.to_wei("12", "gwei"),
        "nonce": w3.eth.get_transaction_count(w3.eth.defaultAccount),
        "chainId": 11155111,  # Update this for your network
        "data": function_data,  # Include the encoded function call
    }

    # Sign the transaction
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"Transaction hash: https://sepolia.etherscan.io/tx/{tx_hash.hex()}\n")

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {tx_receipt}")


for _ in range(5):
    bait_frontrunner(0.005)
    print("\nWaiting 5 seconds...\n")
    time.sleep(5)