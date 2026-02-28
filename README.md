# Backgammon Game Engine & AI Player

A robust Python-based implementation of the Backgammon game logic, featuring a CLI interface, a specialized Server-side management system, and an AI bot driven by custom heuristics.

## Overview
This project focuses on clean software architecture, separating the core game physics (rules, moves, board states) from the high-level management (users, match history, and rankings). It also includes an automated player (Bot) capable of evaluating and making optimal decisions.

## Key Features
- **Core Game Logic (`Board` class):** Complete implementation of Backgammon rules, including legal move validation, hit mechanics (the bar), and bearing off.
- **AI Bot:** An intelligent agent that evaluates board states using heuristics like:
    - Piece distance to home.
    - Risk management (blots/solitary pieces).
    - Defensive structures (anchors/walls).
- **Arena Management:** A backend simulation for a game server:
    - **User Management:** Registration, persistent stats (Win/Loss ratio), and rankings.
    - **Game Persistence:** Capacity to save and resume matches.
- **Fair Play System:** Implementation of a `DiceCup` using a Linear Congruential Generator (LCG) with seeds to ensure transparency and prevent cheating.

## Tech Stack
- **Language:** Python 3
- **Principles:** Object-Oriented Programming (OOP), Unit Testing, Deterministic Algorithms.
- **Data Handling:** Persistence via `pickle` and structured state management.

## Game Modes
You can run the engine in three different modes:
1. **Human vs Human:** Local multiplayer via CLI.
2. **Human vs Bot:** Challenge the heuristic AI.
3. **Bot vs Bot:** Watch two AI agents compete to test strategy efficiency.

## Technical Highlight: The "Flip" Logic
To keep the code DRY (Don't Repeat Yourself), I implemented a `flip` method. Instead of writing separate logic for White and Black players, the engine "flips" the board perspective, processes the move as a single player type, and flips it back, ensuring 100% consistency in rule application.

## Contributions
This project was developed for the Algorithms & Programming II course at UPC.
