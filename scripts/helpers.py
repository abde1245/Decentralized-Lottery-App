
import os
import json
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

load_dotenv()

def get_account():
    w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
    private_key = os.getenv("PRIVATE_KEY")
    account = w3.eth.account.from_key(private_key)
    return account, w3

def compile_contract(contract_file_path):
    with open(contract_file_path, "r") as file:
        contract_file = file.read()

    # Install correct solc version if not present
    try:
        install_solc("0.8.19")
    except Exception as e:
        print(f"Could not install solc 0.8.19: {e}")

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {os.path.basename(contract_file_path): {"content": contract_file}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.19",
    )
    return compiled_sol

def save_contract_info(contract_address, abi):
    info = {
        "address": contract_address,
        "abi": abi,
    }
    with open("app/contract_info.json", "w") as f:
        json.dump(info, f)
    print("Contract address and ABI saved to app/contract_info.json")

