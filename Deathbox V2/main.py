#!/usr/bin/env python3
"""
DeathBox V2: AI Escape
A terminal-based game optimized for iPhone devices using a-Shell in portrait mode.
"""
import os
import sys
import time
import random
import pyfiglet
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# Constants for iPhone optimization
SCREEN_WIDTH = 40  # Narrower width for portrait mode
SCREEN_HEIGHT = 15  # Fewer rows to fit on iPhone screen
MESSAGE_HISTORY_SIZE = 3  # Fewer messages to save screen space


class Entity:
    def __init__(self, x, y, symbol, color=Fore.WHITE):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.color = color


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '@', Fore.CYAN)
        self.has_key = False
        self.hacked_terminals = 0
        self.detected = False
        self.detection_level = 0  # 0-100
        self.max_detection = 100

    def move(self, dx, dy, game_map):
        new_x, new_y = self.x + dx, self.y + dy

        # Check if the move is valid
        if (0 <= new_x < len(game_map[0]) and
            0 <= new_y < len(game_map) and
                game_map[new_y][new_x] != '#'):

            # Check for special tiles
            tile = game_map[new_y][new_x]

            if tile == 'D':  # Door
                if self.has_key:
                    game_map[new_y][new_x] = '.'  # Open the door
                    self.has_key = False
                    return True, "You unlocked the door with your key."
                else:
                    return False, "The door is locked. You need a key."

            elif tile == 'K':  # Key
                self.has_key = True
                game_map[new_y][new_x] = '.'
                return True, "You picked up a key."

            elif tile == 'T':  # Terminal
                game_map[new_y][new_x] = 't'  # Mark as hacked
                self.hacked_terminals += 1
                return True, "You hacked a terminal. Security systems weakened."

            elif tile == 'G':  # Guard
                self.detected = True
                self.detection_level = self.max_detection
                return False, "A guard spotted you! Game over."

            elif tile == 'E':  # Exit
                return True, "EXIT_REACHED"

            # Move the player
            self.x, self.y = new_x, new_y
            return True, None

        return False, "You can't move there."


class Guard(Entity):
    def __init__(self, x, y, patrol_path=None):
        super().__init__(x, y, 'G', Fore.RED)
        self.patrol_path = patrol_path or []
        self.patrol_index = 0
        self.vision_range = 2  # Reduced vision range for easier gameplay on mobile
        # Up, Right, Down, Left
        self.vision_directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.current_direction = 0  # Start looking up

    def move(self, game_map):
        if not self.patrol_path:
            return

        next_pos = self.patrol_path[self.patrol_index]
        self.x, self.y = next_pos
        self.patrol_index = (self.patrol_index + 1) % len(self.patrol_path)

    def can_see_player(self, player, game_map):
        # Check if player is in guard's line of sight
        dx, dy = self.vision_directions[self.current_direction]

        for i in range(1, self.vision_range + 1):
            check_x, check_y = self.x + (dx * i), self.y + (dy * i)

            # Check if position is within map bounds
            if not (0 <= check_x < len(game_map[0]) and 0 <= check_y < len(game_map)):
                break

            # Check if there's a wall blocking vision
            if game_map[check_y][check_x] == '#':
                break

            # Check if player is at this position
            if check_x == player.x and check_y == player.y:
                return True

        return False

    def rotate_vision(self):
        self.current_direction = (self.current_direction + 1) % 4


class Camera(Entity):
    def __init__(self, x, y, direction):
        super().__init__(x, y, 'C', Fore.RED)
        self.direction = direction  # 0: up, 1: right, 2: down, 3: left
        self.vision_range = 3
        self.vision_directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def can_see_player(self, player, game_map):
        dx, dy = self.vision_directions[self.direction]

        for i in range(1, self.vision_range + 1):
            check_x, check_y = self.x + (dx * i), self.y + (dy * i)

            # Check if position is within map bounds
            if not (0 <= check_x < len(game_map[0]) and 0 <= check_y < len(game_map)):
                break

            # Check if there's a wall blocking vision
            if game_map[check_y][check_x] == '#':
                break

            # Check if player is at this position
            if check_x == player.x and check_y == player.y:
                return True

        return False


class Game:
    def __init__(self):
        self.player = None
        self.guards = []
        self.cameras = []
        self.game_map = []
        self.level = 0
        self.max_levels = 5
        self.messages = []
        self.show_intro = True
        self.game_over = False
        self.victory = False
        self.input_handler = None
        self.story = None
        self.sound_manager = None
        self.is_ios = self._check_ios()

        # Import modules
        try:
            from input_handler import InputHandler
            from story import Story
            from sound import SoundManager

            self.input_handler = InputHandler()
            self.story = Story()
            self.sound_manager = SoundManager(self.is_ios)
        except ImportError as e:
            print(f"Error importing modules: {e}")
            print("Make sure all required files are in the same directory.")
            sys.exit(1)

        # Create game levels
        self.levels = self.create_levels()

        # Load the first level
        self.load_level(0)

    def _check_ios(self):
        """Check if running on iOS."""
        is_ios = False
        try:
            # Check for common iOS terminal app environment variables or paths
            if 'IPHONE' in os.environ or 'IPAD' in os.environ:
                is_ios = True
            # Check for a-Shell specific path
            elif os.path.exists('/var/mobile'):
                is_ios = True
        except:
            pass
        return is_ios

    def create_levels(self):
        """Create game levels optimized for iPhone screen size."""
        levels = []

        # Level 1: Tutorial
        level1 = [
            "####################",
            "#.................#",
            "#.................#",
            "#....#####........#",
            "#....#...#........#",
            "#....#T..#........#",
            "#....#####........#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#..@..........E...#",
            "####################"
        ]

        # Level 2: Keys and Doors
        level2 = [
            "####################",
            "#@................#",
            "#.................#",
            "#....#####........#",
            "#....#...#........#",
            "#....#K..#........#",
            "#....#####........#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.......D.........#",
            "#.................#",
            "#.............E...#",
            "####################"
        ]

        # Level 3: Guards
        level3 = [
            "####################",
            "#@................#",
            "#.................#",
            "#....#####........#",
            "#....#...#........#",
            "#....#K..#........#",
            "#....#####........#",
            "#.................#",
            "#.......G.........#",
            "#.................#",
            "#.................#",
            "#.......D.........#",
            "#.................#",
            "#.............E...#",
            "####################"
        ]

        # Level 4: Cameras
        level4 = [
            "####################",
            "#@................#",
            "#.................#",
            "#....#####........#",
            "#....#...#........#",
            "#....#K..#........#",
            "#....#####........#",
            "#.................#",
            "#.......C.........#",
            "#.................#",
            "#.................#",
            "#.......D.........#",
            "#.................#",
            "#.............E...#",
            "####################"
        ]

        # Level 5: Final Challenge
        level5 = [
            "####################",
            "#@................#",
            "#.................#",
            "#....#####........#",
            "#....#...#........#",
            "#....#T..#........#",
            "#....#####........#",
            "#.................#",
            "#.......G.........#",
            "#.................#",
            "#.......C.........#",
            "#.......D.........#",
            "#.................#",
            "#.............E...#",
            "####################"
        ]

        levels.append(level1)
        levels.append(level2)
        levels.append(level3)
        levels.append(level4)
        levels.append(level5)

        return levels

    def load_level(self, level_index):
        """Load a level and initialize entities."""
        if level_index >= len(self.levels):
            self.victory = True
            return

        self.level = level_index
        level_data = self.levels[level_index]
        self.game_map = []
        self.guards = []
        self.cameras = []

        # Process the level data
        for y, row in enumerate(level_data):
            map_row = []
            for x, cell in enumerate(row):
                if cell == '@':
                    self.player = Player(x, y)
                    map_row.append('.')
                elif cell == 'G':
                    # Create a guard with a simple patrol path
                    patrol_path = [(x, y), (x+1, y), (x+2, y), (x+1, y)]
                    guard = Guard(x, y, patrol_path)
                    self.guards.append(guard)
                    map_row.append('.')
                elif cell == 'C':
                    # Create a camera facing right
                    camera = Camera(x, y, 1)
                    self.cameras.append(camera)
                    map_row.append('.')
                else:
                    map_row.append(cell)
            self.game_map.append(map_row)

        # Display level intro
        if self.story:
            self.display_story_sequence(
                self.story.get_level_intro(level_index))

    def add_message(self, message):
        """Add a message to the message history."""
        if message:
            self.messages.append(message)
            if len(self.messages) > MESSAGE_HISTORY_SIZE:
                self.messages.pop(0)

    def display_story_sequence(self, lines, delay=0.05):
        """Display a sequence of story text with typing effect."""
        self.clear_screen()

        for line in lines:
            for char in line:
                print(char, end='', flush=True)
                time.sleep(delay)
            print()

        print("\nPress any key to continue...")
        if self.input_handler:
            while not self.input_handler.get_key():
                time.sleep(0.05)

    def clear_screen(self):
        """Clear the terminal screen."""
        print("\033c", end="")  # ANSI escape sequence to clear screen

    def render(self):
        """Render the game state to the terminal."""
        # Check if we need to show intro
        if self.show_intro:
            if self.story:
                self.display_story_sequence(self.story.get_intro())
            self.show_intro = False
            return

        # Check for game over or victory
        if self.game_over:
            self.clear_screen()
            print(pyfiglet.figlet_format("GAME OVER", font="small"))
            print("\nYou were detected by security systems.")
            print("Press any key to exit...")
            if self.input_handler:
                while not self.input_handler.get_key():
                    time.sleep(0.05)
            sys.exit(0)

        if self.victory:
            self.clear_screen()
            print(pyfiglet.figlet_format("VICTORY", font="small"))
            print("\nYou successfully escaped from the DeathBox facility!")
            print("Press any key to exit...")
            if self.input_handler:
                while not self.input_handler.get_key():
                    time.sleep(0.05)
            sys.exit(0)

        # Clear the screen
        self.clear_screen()

        # Print the level header
        print(f"{Fore.YELLOW}DeathBox V2: AI Escape - Level {self.level + 1}")
        print(f"{Fore.YELLOW}{'-' * SCREEN_WIDTH}")

        # Calculate viewport to center on player
        viewport_width = min(SCREEN_WIDTH, len(self.game_map[0]))
        viewport_height = min(SCREEN_HEIGHT, len(self.game_map))

        # Calculate viewport start positions
        start_x = max(0, min(self.player.x - viewport_width // 2,
                             len(self.game_map[0]) - viewport_width))
        start_y = max(0, min(self.player.y - viewport_height // 2,
                             len(self.game_map) - viewport_height))

        # Render the map (viewport only)
        for y in range(start_y, start_y + viewport_height):
            for x in range(start_x, start_x + viewport_width):
                # Check if position is within map bounds
                if 0 <= y < len(self.game_map) and 0 <= x < len(self.game_map[0]):
                    # Render entities
                    if self.player.x == x and self.player.y == y:
                        print(self.player.color + self.player.symbol, end='')
                    elif any(guard.x == x and guard.y == y for guard in self.guards):
                        print(Fore.RED + 'G', end='')
                    elif any(camera.x == x and camera.y == y for camera in self.cameras):
                        print(Fore.RED + 'C', end='')
                    else:
                        # Render map tiles with colors
                        tile = self.game_map[y][x]
                        if tile == '#':
                            print(Fore.WHITE + '#', end='')
                        elif tile == 'D':
                            print(Fore.YELLOW + 'D', end='')
                        elif tile == 'K':
                            print(Fore.YELLOW + 'K', end='')
                        elif tile == 'T':
                            print(Fore.GREEN + 'T', end='')
                        elif tile == 't':  # Hacked terminal
                            print(Fore.BLUE + 't', end='')
                        elif tile == 'E':
                            print(Fore.MAGENTA + 'E', end='')
                        else:
                            print(Fore.BLACK + '.', end='')
                else:
                    print(' ', end='')
            print()

        # Print status information
        print(f"{Fore.YELLOW}{'-' * SCREEN_WIDTH}")
        print(f"{Fore.CYAN}Keys: {Fore.WHITE}{'Yes' if self.player.has_key else 'No'} | "
              f"{Fore.CYAN}Terminals: {Fore.WHITE}{self.player.hacked_terminals}")

        # Print detection meter
        detection_bar = "["
        detection_level = int(self.player.detection_level /
                              self.player.max_detection * 10)
        detection_bar += "#" * detection_level
        detection_bar += " " * (10 - detection_level)
        detection_bar += "]"
        print(f"{Fore.CYAN}Detection: {Fore.RED if detection_level > 7 else Fore.YELLOW if detection_level > 3 else Fore.GREEN}{detection_bar}")

        # Print messages
        print(f"{Fore.YELLOW}{'-' * SCREEN_WIDTH}")
        for message in self.messages:
            print(message)

        # Print controls
        print(f"{Fore.YELLOW}{'-' * SCREEN_WIDTH}")
        print(
            f"{Fore.CYAN}Controls: {Fore.WHITE}[↑↓←→] Move | [E] Interact | [Q] Quit")

    def process_input(self):
        """Process user input."""
        if not self.input_handler:
            return False

        key = self.input_handler.get_key()
        if not key:
            return False

        # Process the key
        if key.lower() == 'w' or key == 'UP':
            success, message = self.player.move(0, -1, self.game_map)
            if message:
                self.add_message(message)
            if message == "EXIT_REACHED":
                self.load_level(self.level + 1)
            return success

        elif key.lower() == 'a' or key == 'LEFT':
            success, message = self.player.move(-1, 0, self.game_map)
            if message:
                self.add_message(message)
            if message == "EXIT_REACHED":
                self.load_level(self.level + 1)
            return success

        elif key.lower() == 's' or key == 'DOWN':
            success, message = self.player.move(0, 1, self.game_map)
            if message:
                self.add_message(message)
            if message == "EXIT_REACHED":
                self.load_level(self.level + 1)
            return success

        elif key.lower() == 'd' or key == 'RIGHT':
            success, message = self.player.move(1, 0, self.game_map)
            if message:
                self.add_message(message)
            if message == "EXIT_REACHED":
                self.load_level(self.level + 1)
            return success

        elif key.lower() == 'e':
            # Interact with adjacent objects
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                check_x, check_y = self.player.x + dx, self.player.y + dy

                # Check if position is within map bounds
                if not (0 <= check_x < len(self.game_map[0]) and 0 <= check_y < len(self.game_map)):
                    continue

                tile = self.game_map[check_y][check_x]

                if tile == 'T':  # Terminal
                    self.game_map[check_y][check_x] = 't'  # Mark as hacked
                    self.player.hacked_terminals += 1
                    self.add_message(
                        "You hacked a terminal. Security systems weakened.")

                    # Display terminal dialogue
                    if self.story:
                        terminal_index = self.player.hacked_terminals - 1
                        self.display_story_sequence(
                            self.story.get_terminal_dialogue(terminal_index))

                    return True

                elif tile == 'D' and self.player.has_key:  # Locked door with key
                    self.game_map[check_y][check_x] = '.'  # Open the door
                    self.player.has_key = False
                    self.add_message("You unlocked the door with your key.")
                    return True

            self.add_message("Nothing to interact with.")
            return False

        elif key.lower() == 'q':
            self.clear_screen()
            print("Thanks for playing DeathBox V2!")
            sys.exit(0)

        return False

    def update(self):
        """Update game state."""
        # Update guards
        for guard in self.guards:
            guard.move(self.game_map)

            # Check if guard can see player
            if guard.can_see_player(self.player, self.game_map):
                self.player.detected = True
                self.player.detection_level = self.player.max_detection
                self.add_message("A guard spotted you!")
                self.game_over = True

            # Randomly rotate guard vision
            if random.random() < 0.2:  # 20% chance each update
                guard.rotate_vision()

        # Update cameras
        for camera in self.cameras:
            if camera.can_see_player(self.player, self.game_map):
                self.player.detected = True
                self.player.detection_level = self.player.max_detection
                self.add_message("A security camera spotted you!")
                self.game_over = True

        # Update player detection level
        if self.player.detection_level > 0 and not self.player.detected:
            self.player.detection_level -= 1

    def run(self):
        """Main game loop."""
        try:
            while not self.game_over and not self.victory:
                self.render()

                # Process input
                moved = self.process_input()

                # Only update game state if player moved
                if moved:
                    self.update()

                # Small delay to prevent high CPU usage
                time.sleep(0.05)

        except KeyboardInterrupt:
            print("\nGame terminated by user.")
        finally:
            if self.input_handler:
                self.input_handler.cleanup()


# Run the game if this script is executed directly
if __name__ == "__main__":
    game = Game()
    game.run()
