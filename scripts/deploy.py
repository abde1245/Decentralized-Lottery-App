
import os
from web3 import Web3
from helpers import get_account, compile_contract, save_contract_info

# --- MOCK VRF Coordinator for Local Development ---
# In a real testnet/mainnet deployment, you would get these values from chainlink docs
# and a subscription you create at vrf.chain.link
MOCK_VRF_COORDINATOR = {
    "address": "0xb3dCcb4Cf7a26f6cf6B120Cf5A73875B7BBc655B", # Example for some testnets
    "subscription_id": "0", # Needs to be created on VRF platform
    "key_hash": "0x2ed0feb3e7fd2022120aa84fab1945545a9f2ffc9076fd6156fa96eaff4c1311" # Example
}

# For local Ganache, we will deploy a mock VRF coordinator first.
# For simplicity in this script, we'll assume a mock is already deployed
# or we will just use placeholder values. Ganache doesn't have a real VRF.
# We will need to manually call `fulfillRandomWords` in a local environment.

def deploy_lottery():
    account, w3 = get_account()
    w3.eth.default_account = account.address
    print(f"Attempting to deploy from account: {account.address}")

    # Compile the contract
    contract_source_path = os.path.join("contracts", "Lottery.sol")
    compiled_sol = compile_contract(contract_source_path)

    # Get bytecode and ABI
    contract_name = "Lottery.sol:Lottery" # "FileName.sol:ContractName"
    bytecode = compiled_sol["contracts"][os.path.basename(contract_source_path)]["Lottery"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"][os.path.basename(contract_source_path)]["Lottery"]["abi"]

    # Contract constructor arguments
    # For local Ganache, we don't have a real VRF Coordinator or subscription.
    # We will use the deployer's address as a placeholder for the coordinator.
    # This means the `requestWinner` and `fulfillRandomWords` will not work out-of-the-box
    # on Ganache without deploying a Mock VRF Coordinator contract first.
    # This setup is for demonstrating project structure and deployment flow.
    entry_fee = w3.toWei(0.01, "ether")
    vrf_coordinator_address = account.address # Placeholder for local dev
    subscription_id = 12345 # Placeholder
    key_hash = b'\x00' * 32 # Placeholder, 32-byte hash

    print("Deploying contract...")
    LotteryContract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Build transaction
    tx = LotteryContract.constructor(
        entry_fee,
        vrf_coordinator_address,
        subscription_id,
        key_hash
    ).buildTransaction({
        "chainId": w3.eth.chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": account.address,
        "nonce": w3.eth.getTransactionCount(account.address),
    })

    # Sign and send transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=os.getenv("PRIVATE_KEY"))
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Transaction sent, waiting for receipt... Hash: {tx_hash.hex()}")

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Contract Deployed! Address: {tx_receipt.contractAddress}")

    # Save contract info for the frontend
    save_contract_info(tx_receipt.contractAddress, abi)


if __name__ == "__main__":
    deploy_lottery()
