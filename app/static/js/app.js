
// Global variables
let provider;
let signer;
let contract;
let contractInfo;

// DOM Elements
const connectWalletBtn = document.getElementById('connect-wallet-btn');
const walletStatus = document.getElementById('wallet-status');
const lotteryInfoDiv = document.getElementById('lottery-info');
const enterLotteryBtn = document.getElementById('enter-lottery-btn');
const refreshBtn = document.getElementById('refresh-btn');
const logBox = document.getElementById('log-box');

// Display elements
const lotteryStateEl = document.getElementById('lottery-state');
const prizePoolEl = document.getElementById('prize-pool');
const entryFeeEl = document.getElementById('entry-fee');
const playerCountEl = document.getElementById('player-count');
const recentWinnerEl = document.getElementById('recent-winner');
const contractAddrFooter = document.getElementById('contract-address-footer');


async function init() {
    log('Initializing application...');
    try {
        const response = await fetch('/api/contract-info');
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.error || 'Failed to fetch contract info.');
        }
        contractInfo = await response.json();
        log(`Contract info loaded. Address: ${contractInfo.address}`);
        contractAddrFooter.textContent = `Contract Address: ${contractInfo.address}`;
        connectWalletBtn.addEventListener('click', connectWallet);
        enterLotteryBtn.addEventListener('click', enterLottery);
        refreshBtn.addEventListener('click', updateLotteryInfo);

    } catch (error) {
        log(`Error: ${error.message}`);
        walletStatus.textContent = 'Error: Could not load contract info.';
        walletStatus.classList.add('text-danger');
    }
}

async function connectWallet() {
    if (typeof window.ethereum === 'undefined') {
        log('MetaMask is not installed!');
        walletStatus.textContent = 'Please install MetaMask!';
        return;
    }

    try {
        provider = new ethers.providers.Web3Provider(window.ethereum);
        await provider.send("eth_requestAccounts", []);
        signer = provider.getSigner();
        const address = await signer.getAddress();

        log(`Wallet connected: ${address}`);
        walletStatus.textContent = `Connected: ${address.substring(0, 6)}...${address.substring(address.length - 4)}`;

        contract = new ethers.Contract(contractInfo.address, contractInfo.abi, signer);

        lotteryInfoDiv.classList.remove('d-none');
        connectWalletBtn.classList.add('d-none');

        await updateLotteryInfo();
        listenForEvents();

    } catch (error) {
        log(`Connection failed: ${error.message}`);
        walletStatus.textContent = 'Failed to connect wallet.';
    }
}

async function updateLotteryInfo() {
    if (!contract) return;
    log('Refreshing lottery information...');
    try {
        const state = await contract.getLotteryState();
        const prizePool = await provider.getBalance(contract.address);
        const entryFee = await contract.getEntryFee();
        const playerCount = await contract.getNumberOfPlayers();
        const recentWinner = await contract.getRecentWinner();

        const stateMap = ['OPEN', 'CALCULATING_WINNER', 'CLOSED'];
        lotteryStateEl.textContent = stateMap[state];
        prizePoolEl.textContent = ethers.utils.formatEther(prizePool);
        entryFeeEl.textContent = ethers.utils.formatEther(entryFee);
        playerCountEl.textContent = playerCount.toString();
        recentWinnerEl.textContent = (recentWinner === "0x0000000000000000000000000000000000000000") 
            ? "No winner yet" 
            : recentWinner;

        log('Lottery info updated successfully.');
    } catch (error) {
        log(`Error updating info: ${error.message}`);
    }
}

async function enterLottery() {
    if (!contract) return;
    log('Attempting to enter lottery...');
    try {
        const entryFee = await contract.getEntryFee();
        const tx = await contract.enterLottery({ value: entryFee });
        log(`Transaction sent... Hash: ${tx.hash}`);
        log('Waiting for transaction to be mined...');
        await tx.wait();
        log('You have successfully entered the lottery!');
        await updateLotteryInfo();
    } catch (error) {
        log(`Error entering lottery: ${error.code} - ${error.message}`);
    }
}

function listenForEvents() {
    if (!contract) return;
    contract.on("LotteryEnter", (player) => {
        log(`Event: New player entered! Address: ${player}`);
        updateLotteryInfo();
    });

    contract.on("WinnerPicked", (winner) => {
        log(` Event: A winner has been picked! Congratulations to ${winner}!`);
        alert(`A new winner has been picked: ${winner}`);
        updateLotteryInfo();
    });
}

function log(message) {
    console.log(message);
    const now = new Date().toLocaleTimeString();
    logBox.textContent = `[${now}] ${message}\n` + logBox.textContent;
}

// Initialize the app when the DOM is ready
document.addEventListener('DOMContentLoaded', init);
