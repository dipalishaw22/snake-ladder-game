import requests
import random
import time
from typing import Dict, List, Optional

class JokeGenerator:
    """Generate random jokes from multiple external APIs."""
    
    # API endpoints
    OFFICIAL_JOKE_API = "https://official-joke-api.appspot.com/jokes/random"
    OFFICIAL_JOKE_TYPE_API = "https://official-joke-api.appspot.com/jokes/{type}/random"
    JOKEAPI_BASE = "https://v2.jokeapi.dev/joke/{category}"
    DAD_JOKES_API = "https://icanhazdadjoke.com/"
    
    # Timeout for API requests
    TIMEOUT = 10
    
    def __init__(self):
        """Initialize the joke generator."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JokeGenerator/1.0'
        })
    
    def fetch_official_joke(self, joke_type: Optional[str] = None) -> Optional[Dict]:
        """
        Fetch a joke from Official Joke API.
        
        Args:
            joke_type: Type of joke (general, programming, knock-knock, etc.)
            
        Returns:
            Dictionary with joke setup and punchline, or None if failed
        """
        try:
            if joke_type:
                url = self.OFFICIAL_JOKE_TYPE_API.format(type=joke_type)
            else:
                url = self.OFFICIAL_JOKE_API
            
            response = self.session.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            return {
                'setup': data.get('setup', ''),
                'punchline': data.get('punchline', ''),
                'source': 'Official Joke API',
                'type': data.get('type', 'general')
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching from Official Joke API: {e}")
            return None
    
    def fetch_jokeapi_joke(self, category: str = 'Any') -> Optional[Dict]:
        """
        Fetch a joke from JokeAPI.
        
        Args:
            category: Category (Any, Miscellaneous, Programming, Knock-Knock, etc.)
            
        Returns:
            Dictionary with joke data, or None if failed
        """
        try:
            url = self.JOKEAPI_BASE.format(category=category)
            params = {
                'format': 'json',
                'type': 'twopart',
                'safe-mode': True
            }
            
            response = self.session.get(url, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('error'):
                return None
            
            return {
                'setup': data.get('setup', ''),
                'punchline': data.get('delivery', ''),
                'source': 'JokeAPI',
                'category': data.get('category', 'General'),
                'type': data.get('type', 'twopart')
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching from JokeAPI: {e}")
            return None
    
    def fetch_dad_joke(self) -> Optional[Dict]:
        """
        Fetch a dad joke from icanhazdadjoke.com.
        
        Returns:
            Dictionary with joke data, or None if failed
        """
        try:
            response = self.session.get(self.DAD_JOKES_API, timeout=self.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            joke = data.get('joke', '')
            
            return {
                'setup': joke,
                'punchline': '',
                'source': 'Dad Jokes API',
                'type': 'single'
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching from Dad Jokes API: {e}")
            return None
    
    def get_random_joke(self) -> Optional[Dict]:
        """
        Fetch a random joke from any source.
        
        Returns:
            Dictionary with joke data, or None if all APIs fail
        """
        sources = [
            self.fetch_official_joke,
            self.fetch_jokeapi_joke,
            self.fetch_dad_joke
        ]
        
        # Shuffle to randomize which API is used first
        random.shuffle(sources)
        
        for source in sources:
            joke = source()
            if joke:
                return joke
        
        return None
    
    def get_batch_jokes(self, count: int = 5) -> List[Dict]:
        """
        Fetch multiple jokes.
        
        Args:
            count: Number of jokes to fetch (1-10)
            
        Returns:
            List of joke dictionaries
        """
        count = min(max(count, 1), 10)  # Clamp between 1-10
        jokes = []
        
        for i in range(count):
            joke = self.get_random_joke()
            if joke:
                jokes.append(joke)
            
            # Rate limiting to avoid overwhelming APIs
            if i < count - 1:
                time.sleep(0.5)
        
        return jokes
    
    def display_joke(self, joke: Dict) -> None:
        """
        Display a joke in a formatted way.
        
        Args:
            joke: Dictionary with joke data
        """
        if not joke:
            print("❌ Could not fetch a joke. Please try again.")
            return
        
        print("\n" + "="*60)
        print(f"📚 Source: {joke.get('source', 'Unknown')}")
        
        if 'type' in joke:
            print(f"📂 Type: {joke.get('type', 'Unknown')}")
        
        if 'category' in joke:
            print(f"🏷️  Category: {joke.get('category', 'Unknown')}")
        
        print("="*60)
        
        # Display setup
        setup = joke.get('setup', '')
        if setup:
            print(f"😂 {setup}")
            
            # Pause for dramatic effect
            print("\n⏳ ", end="", flush=True)
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(0.5)
            print("\n")
        
        # Display punchline
        punchline = joke.get('punchline', '')
        if punchline:
            print(f"🎉 {punchline}")
        elif not setup:
            # Single-line joke (dad joke)
            full_joke = joke.get('setup', '')
            print(f"😂 {full_joke}")
        
        print("="*60 + "\n")
    
    def get_available_types(self) -> List[str]:
        """
        Get available joke types from Official Joke API.
        
        Returns:
            List of available joke types
        """
        try:
            url = "https://official-joke-api.appspot.com/types"
            response = self.session.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching joke types: {e}")
            return ['general', 'programming', 'knock-knock']
    
    def close(self):
        """Close the session."""
        self.session.close()


def display_menu():
    """Display the main menu."""
    print("\n" + "="*60)
    print("  🎭 Random Joke Generator 🎭")
    print("="*60)
    print("1. 😂 Get a random joke")
    print("2. 🎓 Jokes from Official Joke API")
    print("3. 🎪 Jokes from JokeAPI")
    print("4. 👨‍👩‍👧‍👦 Dad Jokes")
    print("5. 🎱 Batch jokes (multiple)")
    print("6. 🏷️  Get jokes by category")
    print("7. 📋 View available types")
    print("8. 🚪 Exit")
    print("="*60)


def main():
    """Main function to run the joke generator."""
    generator = JokeGenerator()
    
    print("\n" + "🎭"*30)
    print("Welcome to the Random Joke Generator!")
    print("🎭"*30)
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            print("\n⏳ Fetching a random joke...")
            joke = generator.get_random_joke()
            generator.display_joke(joke)
        
        elif choice == '2':
            print("\n⏳ Fetching from Official Joke API...")
            joke = generator.fetch_official_joke()
            generator.display_joke(joke)
        
        elif choice == '3':
            print("\n⏳ Fetching from JokeAPI...")
            joke = generator.fetch_jokeapi_joke()
            generator.display_joke(joke)
        
        elif choice == '4':
            print("\n⏳ Fetching a dad joke...")
            joke = generator.fetch_dad_joke()
            generator.display_joke(joke)
        
        elif choice == '5':
            try:
                count = int(input("How many jokes? (1-10): ").strip())
                print(f"\n⏳ Fetching {count} jokes...")
                jokes = generator.get_batch_jokes(count)
                print(f"\n📊 Fetched {len(jokes)} jokes:\n")
                for i, joke in enumerate(jokes, 1):
                    print(f"\n--- Joke {i} ---")
                    generator.display_joke(joke)
            except ValueError:
                print("❌ Please enter a valid number.")
        
        elif choice == '6':
            available_types = generator.get_available_types()
            print("\n📋 Available categories:")
            for i, joke_type in enumerate(available_types, 1):
                print(f"   {i}. {joke_type}")
            
            try:
                type_choice = int(input("\nSelect category number: ").strip())
                if 1 <= type_choice <= len(available_types):
                    selected_type = available_types[type_choice - 1]
                    print(f"\n⏳ Fetching {selected_type} joke...")
                    joke = generator.fetch_official_joke(selected_type)
                    generator.display_joke(joke)
                else:
                    print("❌ Invalid selection.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        elif choice == '7':
            available_types = generator.get_available_types()
            print("\n📋 Available Joke Types:")
            print("-" * 40)
            for joke_type in available_types:
                print(f"   • {joke_type}")
            print("-" * 40)
        
        elif choice == '8':
            print("\n👋 Thanks for using the Joke Generator!")
            print("Have a great day! 😂\n")
            generator.close()
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-8.")


if __name__ == "__main__":
    main()
