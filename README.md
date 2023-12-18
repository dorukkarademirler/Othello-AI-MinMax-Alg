# Othello AI Player

## Overview

This repository contains a Python implementation of an AI player for the game of Othello. The AI employs Minimax and Alpha-Beta Pruning algorithms to make intelligent decisions during gameplay.

## Introduction

The Othello AI player is designed to compete in Othello games against other players. It utilizes the Minimax and Alpha-Beta Pruning algorithms to make strategic decisions based on the current game state.

## Features

- **Minimax Algorithm:** The AI employs the Minimax algorithm to explore the game tree and make decisions that maximize its utility.
  
- **Alpha-Beta Pruning:** To enhance the efficiency of the Minimax algorithm, the AI uses Alpha-Beta Pruning for minimizing unnecessary evaluations.

- **State Caching:** An optional feature to cache game states, reducing the number of redundant state evaluations.

- **Node Ordering:** For Alpha-Beta Pruning, the AI has the option to use node ordering to expedite pruning and further reduce state evaluations.

## File Structure

The repository is organized as follows:

- `othello_ai.py`: The main Python script containing the AI implementation.
- `othello_shared.py`: A module providing shared functions for Othello game mechanics.
- `README.md`: This documentation file.

## Algorithm Details

- **Utility Function:** The utility function evaluates the desirability of a game state based on the number of disks for the specified player.

- **Heuristic Function:** An optional heuristic function estimates the value of a game state if the depth limit is reached, providing a faster evaluation.

- **Minimax and Alpha-Beta Pruning:** The AI uses Minimax for decision-making, and Alpha-Beta Pruning to optimize the search process.

## How to Run

To run the Othello AI, follow these steps:

1. [Install Python](https://www.python.org/downloads/) if not already installed.
2. Execute the `othello_ai.py` script.

## Configuration

The AI player can be configured with the following options:

- **Depth Limit:** Specify the depth limit for the search.
- **Caching:** Enable or disable state caching.
- **Node Ordering:** Enable or disable node ordering (for Alpha-Beta Pruning).

## Acknowledgments

Special thanks to the developers of the Othello game and the creators of the Minimax and Alpha-Beta Pruning algorithms.
