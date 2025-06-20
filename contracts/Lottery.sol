
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/vrf/VRFConsumerBaseV2.sol";

/**
 * @title A Decentralized Lottery Contract
 * @author Abhradeep Dey
 * @notice This contract is for creating a decentralized lottery
 * @dev Implements Chainlink VRF V2 for provably random winner selection
 */
contract Lottery is VRFConsumerBaseV2 {
    enum LotteryState {
        OPEN,
        CALCULATING_WINNER,
        CLOSED
    }

    // State Variables
    uint256 private immutable i_entryFee;
    address payable[] private s_players;
    address private s_recentWinner;
    LotteryState private s_lotteryState;
    address private immutable i_owner;

    // Chainlink VRF Variables
    VRFCoordinatorV2Interface private immutable i_vrfCoordinator;
    uint64 private immutable i_subscriptionId;
    bytes32 private immutable i_gasLane; // keyHash
    uint32 private immutable i_callbackGasLimit;
    uint16 private constant REQUEST_CONFIRMATIONS = 3;
    uint32 private constant NUM_WORDS = 1;

    // Events
    event LotteryEnter(address indexed player);
    event RequestedLotteryWinner(uint256 indexed requestId);
    event WinnerPicked(address indexed winner);

    // Errors
    error Lottery__NotOwner();
    error Lottery__NotOpen();
    error Lottery__NotEnoughETHEntered();
    error Lottery__TransferFailed();

    constructor(
        uint256 entryFee,
        address vrfCoordinatorV2, // Contract address
        uint64 subscriptionId,
        bytes32 gasLane // keyHash
    ) VRFConsumerBaseV2(vrfCoordinatorV2) {
        i_entryFee = entryFee;
        s_lotteryState = LotteryState.OPEN;
        i_owner = msg.sender;
        i_vrfCoordinator = VRFCoordinatorV2Interface(vrfCoordinatorV2);
        i_subscriptionId = subscriptionId;
        i_gasLane = gasLane;
        i_callbackGasLimit = 100000; // Adjust as needed
    }

    function enterLottery() public payable {
        if (s_lotteryState != LotteryState.OPEN) {
            revert Lottery__NotOpen();
        }
        if (msg.value < i_entryFee) {
            revert Lottery__NotEnoughETHEntered();
        }
        s_players.push(payable(msg.sender));
        emit LotteryEnter(msg.sender);
    }

    /**
     * @notice This is the function that the owner calls to start the winner selection
     * @dev It requests a random number from the Chainlink VRF.
     * The actual winner selection happens in the fulfillRandomWords callback.
     */
    function requestWinner() public {
        if (msg.sender != i_owner) {
            revert Lottery__NotOwner();
        }
        if (s_lotteryState != LotteryState.OPEN) {
            revert Lottery__NotOpen();
        }

        s_lotteryState = LotteryState.CALCULATING_WINNER;

        uint256 requestId = i_vrfCoordinator.requestRandomWords(
            i_gasLane, // keyHash
            i_subscriptionId,
            REQUEST_CONFIRMATIONS,
            i_callbackGasLimit,
            NUM_WORDS
        );
        emit RequestedLotteryWinner(requestId);
    }

    /**
     * @notice This is the callback function that the Chainlink VRF node calls
     * once it has a verifiable random number.
     */
    function fulfillRandomWords(
        uint256 /* requestId */,
        uint256[] memory randomWords
    ) internal override {
        uint256 indexOfWinner = randomWords[0] % s_players.length;
        address payable recentWinner = s_players[indexOfWinner];
        s_recentWinner = recentWinner;

        // Reset the lottery for the next round
        s_lotteryState = LotteryState.OPEN;
        s_players = new address payable[](0);

        // Transfer funds to the winner
        (bool success, ) = recentWinner.call{value: address(this).balance}("");
        if (!success) {
            revert Lottery__TransferFailed();
        }

        emit WinnerPicked(recentWinner);
    }

    // --- View / Pure Functions ---
    function getEntryFee() public view returns (uint256) {
        return i_entryFee;
    }

    function getLotteryState() public view returns (LotteryState) {
        return s_lotteryState;
    }

    function getPlayer(uint256 index) public view returns (address) {
        return s_players[index];
    }

    function getNumberOfPlayers() public view returns (uint256) {
        return s_players.length;
    }

    function getRecentWinner() public view returns (address) {
        return s_recentWinner;
    }

    function getOwner() public view returns (address) {
        return i_owner;
    }
}
