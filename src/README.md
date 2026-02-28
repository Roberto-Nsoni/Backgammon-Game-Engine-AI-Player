# Backgammon Engine & Arena Management
Welcome to the core engine and management system for Backgammon!

This project implements a robust game server for the classic board game "Backgammon." It features complete game logic, a CLI for human players, a heuristic-based AI bot, and a centralized `Arena` system to manage users, match history, and persistent statistics.

## Project Structure
The project is decoupled into specific modules to ensure a clean separation of concerns:

### 1. `board.py` Module
The heart of the project. It handles all game rules, legal move validation, and state transitions. Key components include:

- **`Dice` Dataclass:** Represents the value of two dice.
- **`DiceCup` Class:** Manages dice rolling using a Linear Congruential Generator for deterministic pseudo-randomness, crucial for fair play and debugging.
- **`Jump` Dataclass:** Represents a single checker's leap.
- **`Move` Dataclass:** Represents a full turn, consisting of a sequence of jumps.
- **`Board` Class:** Manages the complete board state and rule enforcement.

### 2. Gameplay Interfaces
- **`human_vs_human.py`:** A CLI interface for local multiplayer.
- **`human_vs_bot.py` & `bot_vs_bot.py`:** Interfaces to challenge the AI or simulate automated matches to test strategy efficiency.

### 3. `bot.py` Module (Heuristic AI)
This module implements an automated agent capable of playing against humans or other bots. The AI decision-making process follows these steps:

1. **Evaluation:** Assigns a score to every possible legal move using a custom heuristic function.
2. **Minimax-lite approach:** Simulates the opponent's best possible response for each move to anticipate risks.
3. **Selection:** Executes the move with the highest net score.

**Heuristic factors include:**
- Optimal checker positioning.
- Prioritizing "bearing off" (finishing the game).
- Penalty for checkers on the bar.
- Penalty for "blots" (solitary, vulnerable checkers).

### 4. `arena.py` Module (Server Management)
Acts as the backend manager for users and matches. It includes:

- **`User` Dataclass:** Stores profile data, win/loss ratios, and connection status.
- **`Game` Dataclass:** Manages active match metadata (players, dice seeds, board state, move history).
- **`Arena` Class:** The central controller managing registrations, active sessions, and global rankings.

**Custom Exception Handling:**
- `UserRegistrationError`: For ID collisions during sign-up.
- `UserLogError`: For session management issues (login/logout).
- `GameError`: For internal logic errors (e.g., deleting a user mid-game).

## Key Features

1. **Data Persistence:** Integrated state saving/loading using the `pickle` module, allowing the `Arena` to persist between sessions.
2. **Custom Configurations:** Both `Board` and `Arena` support custom initial states for specialized testing or scenarios.
3. **Interactive CLI Menu:** A fully-featured menu to register, login, play, and view leaderboards directly from the terminal.
4. **Unit Testing:** Comprehensive test suites using `pytest` to ensure logic integrity and prevent regressions in game rules.

## 🎮 How to Play
Ensure you have **Python 3.8+** installed. The project relies on the standard library (`typing`, `sys`, `random`, `uuid`, `pickle`) and `pytest` for testing.

### Mode: Human vs. Human
To play against a friend locally:
```bash
python3 human_vs_human.py
```

- **Controls:** Enter pairs of (position, die). Example: `12 3 19 1` moves a piece from 12 by 3 units, and another from 19 by 1 unit.
- **Special Commands:** Type `?` to see all available legal moves.
- **Bar Representation:** The bar is represented as position `0`.

### Mode: Human vs. Bot
To challenge the AI (Human plays White, Bot plays Black):

```bash
python3 human_vs_bot.py
```

## ✅ Running Tests
The project includes a suite of unit tests covering core game logic, edge cases, and Arena management to ensure stability. Interface-related components are excluded from automated testing. To run the suite:

```bash
python -m pytest .
```

