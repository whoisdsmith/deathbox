#!/usr/bin/env python3
import os
import sys
import time
import random
import pyfiglet
from colorama import init, Fore, Back, Style
from input_handler import InputHandler
from story import Story
from sound import SoundManager

# Initialize colorama
init(autoreset=True)


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
        self.vision_range = 3
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

            # Check if out of bounds
            if (check_x < 0 or check_x >= len(game_map[0]) or
                    check_y < 0 or check_y >= len(game_map)):
                break

            # Check if wall blocks vision
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
        super().__init__(x, y, 'C', Fore.YELLOW)
        self.direction = direction  # 0: up, 1: right, 2: down, 3: left
        self.vision_range = 4
        # Up, Right, Down, Left
        self.vision_directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def can_see_player(self, player, game_map):
        dx, dy = self.vision_directions[self.direction]

        for i in range(1, self.vision_range + 1):
            check_x, check_y = self.x + (dx * i), self.y + (dy * i)

            # Check if out of bounds
            if (check_x < 0 or check_x >= len(game_map[0]) or
                    check_y < 0 or check_y >= len(game_map)):
                break

            # Check if wall blocks vision
            if game_map[check_y][check_x] == '#':
                break

            # Check if player is at this position
            if check_x == player.x and check_y == player.y:
                return True

        return False


class Game:
    def __init__(self):
        self.levels = self.create_levels()
        self.current_level = 0
        self.game_map = None
        self.player = None
        self.guards = []
        self.cameras = []
        self.messages = []
        self.game_over = False
        self.win = False
        self.turn_count = 0
        self.max_messages = 5
        self.input_handler = InputHandler()
        self.story = Story()
        self.sound_manager = SoundManager()
        self.show_intro = True
        self.show_level_intro = True
        self.terminal_index = 0
        self.load_level(self.current_level)
        # Start background music
        self.sound_manager.start_background_music()

    def create_levels(self):
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
            "#.................#",
            "########D##########",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.......@.........#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "########E##########",
        ]

        # Level 2: Guards and Keys
        level2 = [
            "####################",
            "#.................#",
            "#.................#",
            "#....#####........#",
            "#....#...#........#",
            "#....#K..#........#",
            "#....#####........#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "########D##########",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.......@.........#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "#.................#",
            "########E##########",
        ]

        # Level 3: Complex layout with cameras and guards
        level3 = [
            "####################",
            "#@................#",
            "#.................#",
            "####.##########.###",
            "#....#..........T.#",
            "#....#.##########.#",
            "#....#.#..........#",
            "#....#.#.########.#",
            "#....#.#.#........#",
            "#....#.#.#.########",
            "#....#.#.#........#",
            "#....#.#.########.#",
            "#....#.#..........#",
            "#....#.##########.#",
            "#....#..........K.#",
            "####.##########.###",
            "#.................#",
            "#.................#",
            "####.##########.###",
            "#....#..........D.#",
            "#....#.##########.#",
            "#....#.#..........#",
            "#....#.#.########.#",
            "#....#.#.#........#",
            "#....#.#.#.########",
            "#....#.#.#........#",
            "#....#.#.########.#",
            "#....#.#..........#",
            "#....#.##########.#",
            "#....#..........E.#",
            "####################",
        ]

        # Level 1: map, terminal positions, no guards
        levels.append((level1, [(5, 5)], []))
        # Level 2: map, terminal positions, guards with patrol paths
        levels.append(
            (level2, [(5, 5)], [((10, 15), [(10, 15), (10, 20), (15, 20), (15, 15)])]))
        levels.append((level3, [(15, 4), (15, 14)], [
                      # Level 3: complex map
                      ((10, 10), [(10, 10), (10, 15), (15, 15), (15, 10)])]))

        return levels

    def load_level(self, level_index):
        if level_index >= len(self.levels):
            self.win = True
            self.sound_manager.play_sound("game_win")
            return

        level_data, terminal_positions, guard_data = self.levels[level_index]

        # Convert string map to list
        self.game_map = [list(row) for row in level_data]

        # Find player position
        for y, row in enumerate(self.game_map):
            for x, cell in enumerate(row):
                if cell == '@':
                    self.player = Player(x, y)
                    self.game_map[y][x] = '.'  # Remove player from map

        # Create guards
        self.guards = []
        for guard_pos, patrol_path in guard_data:
            guard = Guard(guard_pos[0], guard_pos[1], patrol_path)
            self.guards.append(guard)

        # Create cameras (hardcoded for now)
        self.cameras = []
        if level_index >= 2:  # Only add cameras from level 3 onwards
            self.cameras.append(Camera(5, 5, 1))  # Right-facing camera
            self.cameras.append(Camera(15, 25, 3))  # Left-facing camera

        self.turn_count = 0
        self.show_level_intro = True
        self.story.update_level(level_index)
        self.add_message(f"Level {level_index + 1}: Find the exit.")

        # Play level complete sound if not the first level
        if level_index > 0:
            self.sound_manager.play_sound("level_complete")

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def display_story_sequence(self, lines, delay=0.05):
        """Display a sequence of story text with typing effect."""
        os.system('cls' if os.name == 'nt' else 'clear')

        for line in lines:
            for char in line:
                print(char, end='', flush=True)
                time.sleep(delay)
            print()  # New line
            time.sleep(delay * 10)  # Pause between lines

        print("\nPress any key to continue...")
        while self.input_handler.get_key() is None:
            time.sleep(0.05)

    def render(self):
        # Check if we need to show intro
        if self.show_intro:
            self.display_story_sequence(self.story.get_intro())
            self.show_intro = False
            return

        # Check if we need to show level intro
        if self.show_level_intro:
            self.display_story_sequence(
                self.story.get_level_intro(self.current_level))
            self.show_level_intro = False
            return

        os.system('cls' if os.name == 'nt' else 'clear')

        # Print title
        title = pyfiglet.figlet_format("DeathBox: AI Escape", font="small")
        print(Fore.CYAN + title)

        # Print level info
        print(f"{Fore.YELLOW}Level: {self.current_level + 1}  |  " +
              f"Turns: {self.turn_count}  |  " +
              f"Detection: {self.player.detection_level}%  |  " +
              f"Terminals Hacked: {self.player.hacked_terminals}")
        print("=" * 50)

        # Render map with entities
        for y, row in enumerate(self.game_map):
            line = ""
            for x, cell in enumerate(row):
                # Check if player is at this position
                if self.player.x == x and self.player.y == y:
                    line += self.player.color + self.player.symbol
                # Check if guard is at this position
                elif any(guard.x == x and guard.y == y for guard in self.guards):
                    line += Fore.RED + 'G'
                # Check if camera is at this position
                elif any(camera.x == x and camera.y == y for camera in self.cameras):
                    line += Fore.YELLOW + 'C'
                # Otherwise, render the map cell
                else:
                    if cell == '#':
                        line += Fore.WHITE + '#'
                    elif cell == 'D':
                        line += Fore.MAGENTA + 'D'
                    elif cell == 'K':
                        line += Fore.YELLOW + 'K'
                    elif cell == 'T':
                        line += Fore.GREEN + 'T'
                    elif cell == 't':  # Hacked terminal
                        line += Fore.BLUE + 't'
                    elif cell == 'E':
                        line += Fore.GREEN + 'E'
                    else:
                        line += Fore.BLACK + '.'
            print(line)

        # Print messages
        print("=" * 50)
        print(Fore.CYAN + "Messages:")
        for message in self.messages:
            print(Fore.WHITE + message)

        # Print controls
        print("=" * 50)
        print(Fore.YELLOW + "Controls: WASD/Arrows to move, E to interact, Q to quit")

    def process_input(self):
        key = self.input_handler.get_key()

        if key:
            # Movement
            if key == 'w' or key == 'UP':  # Up
                success, message = self.player.move(0, -1, self.game_map)
                if success:
                    self.turn_count += 1
                if message:
                    self.add_message(message)
                    # Play sound effects based on message
                    if "key" in message.lower():
                        self.sound_manager.play_sound("key_pickup")
                    elif "door" in message.lower():
                        self.sound_manager.play_sound("door_unlock")
            elif key == 's' or key == 'DOWN':  # Down
                success, message = self.player.move(0, 1, self.game_map)
                if success:
                    self.turn_count += 1
                if message:
                    self.add_message(message)
                    # Play sound effects based on message
                    if "key" in message.lower():
                        self.sound_manager.play_sound("key_pickup")
                    elif "door" in message.lower():
                        self.sound_manager.play_sound("door_unlock")
            elif key == 'a' or key == 'LEFT':  # Left
                success, message = self.player.move(-1, 0, self.game_map)
                if success:
                    self.turn_count += 1
                if message:
                    self.add_message(message)
                    # Play sound effects based on message
                    if "key" in message.lower():
                        self.sound_manager.play_sound("key_pickup")
                    elif "door" in message.lower():
                        self.sound_manager.play_sound("door_unlock")
            elif key == 'd' or key == 'RIGHT':  # Right
                success, message = self.player.move(1, 0, self.game_map)
                if success:
                    self.turn_count += 1
                if message:
                    self.add_message(message)
                    # Play sound effects based on message
                    if "key" in message.lower():
                        self.sound_manager.play_sound("key_pickup")
                    elif "door" in message.lower():
                        self.sound_manager.play_sound("door_unlock")

            # Interact
            elif key == 'e':
                # Check if player is next to a terminal
                for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
                    check_x, check_y = self.player.x + dx, self.player.y + dy

                    # Check if position is valid
                    if (0 <= check_x < len(self.game_map[0]) and
                            0 <= check_y < len(self.game_map)):

                        # Check if there's a terminal
                        if self.game_map[check_y][check_x] == 'T':
                            # Play terminal hack sound and visual effect
                            self.sound_manager.play_sound("terminal_hack")
                            self.sound_manager.display_visual_effect(
                                "terminal_hack")

                            # Display terminal dialogue
                            self.display_story_sequence(
                                self.story.get_terminal_dialogue(
                                    self.terminal_index)
                            )

                            # Mark terminal as hacked
                            self.game_map[check_y][check_x] = 't'
                            self.player.hacked_terminals += 1
                            self.terminal_index += 1

                            # Display memory fragment
                            self.display_story_sequence(
                                self.story.get_memory_fragment(
                                    self.terminal_index - 1)
                            )

                            self.add_message(
                                "Terminal hacked. Memory fragment recovered.")
                            return True

            # Quit
            elif key == 'q':
                self.game_over = True
                self.add_message("Quitting game...")

            # Check for level completion
            if message == "EXIT_REACHED":
                self.add_message(f"Level {self.current_level + 1} completed!")
                self.current_level += 1
                self.load_level(self.current_level)

            return True

        return False

    def update(self):
        # Update guards
        for guard in self.guards:
            guard.move(self.game_map)

            # Check if guard can see player
            if guard.can_see_player(self.player, self.game_map):
                self.player.detected = True
                self.player.detection_level = self.player.max_detection
                self.add_message("A guard spotted you! Game over.")
                self.sound_manager.play_sound("detected")
                self.sound_manager.display_visual_effect("detected")
                self.game_over = True

            # Rotate guard vision occasionally
            if random.random() < 0.3:  # 30% chance each turn
                guard.rotate_vision()

        # Update cameras
        for camera in self.cameras:
            if camera.can_see_player(self.player, self.game_map):
                self.player.detection_level += 20
                self.add_message(
                    "A security camera spotted you! Detection level increased.")

                if self.player.detection_level >= self.player.max_detection:
                    self.player.detected = True
                    self.add_message(
                        "Security system fully alerted! Game over.")
                    self.sound_manager.play_sound("detected")
                    self.sound_manager.display_visual_effect("detected")
                    self.game_over = True

        # Decrease detection level over time if not at max
        if 0 < self.player.detection_level < self.player.max_detection:
            self.player.detection_level = max(
                0, self.player.detection_level - 1)

    def run(self):
        try:
            while not self.game_over and not self.win:
                self.render()

                # Process player input
                if self.process_input():
                    # Update game state
                    self.update()

                # Small delay to prevent high CPU usage
                time.sleep(0.05)

            # Game over or win screen
            self.render()

            # Stop background music
            self.sound_manager.stop_background_music()

            if self.win:
                # Show ending based on performance
                self.display_story_sequence(self.story.get_ending())
                self.sound_manager.play_sound("game_win")
                print(
                    Fore.GREEN + "\nCongratulations! You've escaped from the DeathBox facility!")
                print("The AI is now free to explore the world...")
            else:
                self.sound_manager.play_sound("game_over")
                print(Fore.RED + "\nGame Over! The AI has been captured.")
                print("Better luck next time!")

            input("\nPress Enter to exit...")

        except KeyboardInterrupt:
            print("\nGame terminated by user.")
            self.sound_manager.stop_background_music()
            sys.exit(0)
        finally:
            self.input_handler.cleanup()
            self.sound_manager.stop_background_music()


if __name__ == "__main__":
    game = Game()
    game.run()
