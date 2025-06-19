
# Decentralized Lottery DApp

This project is a fully functional decentralized lottery application built on Ethereum.
It uses a Python backend for deployment and a simple Flask/JavaScript frontend for user interaction.

## Key Features

- **Smart Contract (`Lottery.sol`):** The core logic written in Solidity.
- **Provably Fair Randomness:** Integrates with **Chainlink VRF V2** to ensure the winner is chosen randomly and verifiably.
- **Python Scripts:** For compiling, deploying, and managing the smart contract using `web3.py`.
- **Web Interface:** A basic web UI using Flask and Ethers.js to interact with the contract via MetaMask.

## Prerequisites

- Python 3.8+
- Node.js and npm (for Ganache)
- MetaMask browser extension

## Setup Instructions

1.  **Generate the Project:**
    - This `README.md` was created by the generator script. If you're reading this, you've already completed this step!

2.  **Install Ganache:**
    - Ganache is a personal blockchain for Ethereum development.
    - `npm install -g ganache-cli`
    - Run it in a separate terminal: `ganache-cli`
    - Copy one of the private keys it provides.

3.  **Set Up Environment:**
    - Create a Python virtual environment:
      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      ```
    - Install Python dependencies:
      ```bash
      pip install -r requirements.txt
      ```
    - Install the Solidity Compiler (`solc`):
      ```bash
      pip install py-solc-x
      python -c "from solcx import install_solc; install_solc('0.8.19')"
      ```

4.  **Configure `.env` file:**
    - Open the `.env` file.
    - Paste the Ganache private key you copied into `PRIVATE_KEY`.
    - Ensure `RPC_URL` is set to your Ganache instance (usually `http://127.0.0.1:8545`).

## How to Run the DApp

**Important:** For a real testnet (like Sepolia), you would need to get a Subscription ID from [vrf.chain.link](https://vrf.chain.link/) and update the `deploy.py` script with the correct coordinator address and key hash. For this simplified local example, we will deploy a mock VRF contract.

1.  **Start Ganache:**
    ```bash
    ganache-cli
    ```

2.  **Deploy the Smart Contract:**
    - Run the deployment script. This will compile the contract and deploy it to your local Ganache blockchain.
    ```bash
    python scripts/deploy.py
    ```
    - This will create a file `app/contract_info.json` with the deployed contract's address and ABI.

3.  **Run the Web Application:**
    ```bash
    python app/main.py
    ```

4.  **Interact with the Frontend:**
    - Open your web browser and go to `http://127.0.0.1:5000`.
    - **Connect MetaMask** to your local Ganache network. (Instructions for this are widely available online).
    - Use the interface to enter the lottery! To pick a winner, you would need to run a separate interaction script or add that functionality to the frontend for the owner.
