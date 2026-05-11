# 🎮 Snake and Ladder Game

A classic Python implementation of the Snake and Ladder board game with support for multiple players!

## 📋 Features

- ✅ 2-4 player support
- ✅ 100-square board
- ✅ Classic snakes and ladders placements
- ✅ Dice rolling mechanics (1-6)
- ✅ Automatic snake/ladder detection
- ✅ Overshoot prevention (no going beyond 100)
- ✅ Win detection
- ✅ Interactive gameplay with emoji feedback

## 🎯 How to Play

### Installation
No external dependencies required! Just Python 3.6+

### Running the Game

```bash
python snake_ladder.py
```

### Gameplay

1. **Start the game** - Enter the number of players (2-4)
2. **Add player names** - Give each player a unique name
3. **Take turns** - Players take turns rolling the dice
4. **Move your piece** - Your piece moves according to the dice roll
5. **Snakes & Ladders** - 
   - Landing on a ladder bottom moves you UP to the top
   - Landing on a snake head moves you DOWN to the tail
6. **Win** - First player to reach exactly position 100 wins!

## 🐍 Board Layout

### Snakes (Bad luck!)
- 17 → 4
- 54 → 34
- 62 → 18
- 87 → 24
- 93 → 73
- 99 → 79

### Ladders (Good luck!)
- 1 → 38
- 4 → 14
- 9 → 31
- 21 → 42
- 28 → 84
- 51 → 67
- 72 → 91
- 80 → 98

## 📚 Code Structure

### Main Classes

**`SnakeLadderGame`**
- Manages the game state and logic
- Handles player movements
- Detects snakes, ladders, and wins
- Tracks game progress

### Key Methods

- `add_player(name)` - Add a new player
- `roll_dice()` - Roll a dice (returns 1-6)
- `move_player(name, dice_value)` - Move a player based on dice roll
- `play_turn(name)` - Execute a player's turn
- `play_game()` - Run the complete game
- `get_board_state()` - Display current player positions

## 🎮 Example Game Session

```
==================================================
  Welcome to Snake and Ladder Game! 🎮
==================================================

How many players? (2-4): 2

Enter player names:
Player 1 name: Alice
✅ Player 'Alice' added!
Player 2 name: Bob
✅ Player 'Bob' added!

==================================================
  🎯 Snake and Ladder Game Started!
  Board Size: 100
  Players: Alice, Bob
==================================================

🎮 Alice's turn!
  🎲 Rolled: 5
  📍 Alice is now at position 5

🎮 Bob's turn!
  🎲 Rolled: 3
  📍 Bob is now at position 3

🎮 Alice's turn!
  🎲 Rolled: 4
  🪜 Yay! Alice found a ladder! 9 → 31
  📍 Alice is now at position 31

... (game continues) ...

🏆 Congratulations Alice! You won! 🏆

📊 Current Positions:
----------------------------------------
  Alice: Position 100
  Bob: Position 78
----------------------------------------

🎊 Game finished in 47 turns!
```

## 🔧 Customization

You can modify the game by editing these variables in the `_create_board()` method:

```python
snakes = {
    17: 4, 54: 34, ...  # Add or remove snakes
}

ladders = {
    1: 38, 4: 14, ...  # Add or remove ladders
}
```

Or change the board size in the `SnakeLadderGame` initialization:

```python
game = SnakeLadderGame(board_size=100, num_players=2)
```

## 📝 License

This project is open source and available for personal and educational use.

## 🎉 Enjoy the Game!

Have fun playing Snake and Ladder! 🎲
