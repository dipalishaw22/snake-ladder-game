import random
from enum import Enum

class GamePiece(Enum):
    SNAKE = "🐍"
    LADDER = "🪜"

class SnakeLadderGame:
    """A classic Snake and Ladder game implementation."""
    
    def __init__(self, board_size=100, num_players=2):
        """
        Initialize the game.
        
        Args:
            board_size: Size of the board (default 100)
            num_players: Number of players (default 2)
        """
        self.board_size = board_size
        self.num_players = num_players
        self.players = {}
        self.board = self._create_board()
        self.current_player_index = 0
        self.game_over = False
        self.winner = None
        
    def _create_board(self):
        """Create the board with snakes and ladders."""
        board = {}
        
        # Define snakes (position -> destination)
        snakes = {
            17: 4, 54: 34, 62: 18, 87: 24, 93: 73, 99: 79
        }
        
        # Define ladders (position -> destination)
        ladders = {
            1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 51: 67, 72: 91, 80: 98
        }
        
        for i in range(1, self.board_size + 1):
            if i in snakes:
                board[i] = {'type': GamePiece.SNAKE, 'destination': snakes[i]}
            elif i in ladders:
                board[i] = {'type': GamePiece.LADDER, 'destination': ladders[i]}
            else:
                board[i] = {'type': None, 'destination': i}
        
        return board
    
    def add_player(self, player_name):
        """Add a player to the game."""
        if len(self.players) >= self.num_players:
            print(f"Maximum {self.num_players} players already added!")
            return False
        
        self.players[player_name] = 0
        print(f"✅ Player '{player_name}' added!")
        return True
    
    def roll_dice(self):
        """Roll a dice (1-6)."""
        return random.randint(1, 6)
    
    def move_player(self, player_name, dice_value):
        """
        Move a player based on dice value.
        
        Args:
            player_name: Name of the player
            dice_value: Value from dice roll
            
        Returns:
            New position of the player
        """
        if player_name not in self.players:
            print(f"Player '{player_name}' not found!")
            return None
        
        current_pos = self.players[player_name]
        new_pos = current_pos + dice_value
        
        # Check if position exceeds board size
        if new_pos > self.board_size:
            print(f"  ❌ Overshoot! {player_name} stays at position {current_pos}")
            return current_pos
        
        # Check for snake or ladder
        square = self.board[new_pos]
        if square['type'] == GamePiece.SNAKE:
            destination = square['destination']
            print(f"  🐍 Oh no! {player_name} landed on a snake! {new_pos} → {destination}")
            new_pos = destination
        elif square['type'] == GamePiece.LADDER:
            destination = square['destination']
            print(f"  🪜 Yay! {player_name} found a ladder! {new_pos} → {destination}")
            new_pos = destination
        
        self.players[player_name] = new_pos
        return new_pos
    
    def play_turn(self, player_name):
        """Play a single turn for a player."""
        if self.game_over:
            print("Game is already over!")
            return False
        
        print(f"\n🎮 {player_name}'s turn!")
        dice = self.roll_dice()
        print(f"  🎲 Rolled: {dice}")
        
        new_pos = self.move_player(player_name, dice)
        print(f"  📍 {player_name} is now at position {new_pos}")
        
        # Check for win
        if new_pos == self.board_size:
            print(f"\n🏆 Congratulations {player_name}! You won! 🏆")
            self.game_over = True
            self.winner = player_name
            return True
        
        return False
    
    def get_board_state(self):
        """Get current state of all players."""
        print("\n📊 Current Positions:")
        print("-" * 40)
        for player, position in self.players.items():
            print(f"  {player}: Position {position}")
        print("-" * 40)
    
    def play_game(self):
        """Play the complete game with auto turns."""
        print(f"\n{'='*50}")
        print(f"  🎯 Snake and Ladder Game Started!")
        print(f"  Board Size: {self.board_size}")
        print(f"  Players: {', '.join(self.players.keys())}")
        print(f"{'='*50}\n")
        
        turn_count = 0
        max_turns = 1000  # Prevent infinite loops
        
        while not self.game_over and turn_count < max_turns:
            player_name = list(self.players.keys())[self.current_player_index]
            self.play_turn(player_name)
            
            if not self.game_over:
                self.current_player_index = (self.current_player_index + 1) % self.num_players
            
            turn_count += 1
        
        self.get_board_state()
        
        if self.game_over:
            print(f"\n🎊 Game finished in {turn_count} turns!")
        else:
            print("\n⚠️  Max turns reached. Game ended.")


def main():
    """Main function to run the game."""
    print("\n" + "="*50)
    print("  Welcome to Snake and Ladder Game! 🎮")
    print("="*50)
    
    # Get number of players
    while True:
        try:
            num_players = int(input("\nHow many players? (2-4): "))
            if 2 <= num_players <= 4:
                break
            print("Please enter a number between 2 and 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Create game
    game = SnakeLadderGame(board_size=100, num_players=num_players)
    
    # Add players
    print("\nEnter player names:")
    for i in range(num_players):
        while True:
            name = input(f"Player {i+1} name: ").strip()
            if name:
                game.add_player(name)
                break
            print("Please enter a valid name.")
    
    # Play game
    game.play_game()
    
    print("\n" + "="*50)
    print("  Thanks for playing! 👋")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
