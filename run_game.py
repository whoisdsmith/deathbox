#!/usr/bin/env python3
import os
import sys
import time
import traceback
import subprocess


def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import colorama
        import pyfiglet
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False


def install_dependencies():
    """Install required dependencies."""
    print("Installing required dependencies...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install dependencies. Please install them manually:")
        print("pip install -r requirements.txt")
        return False


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_title():
    """Display the game title."""
    try:
        import pyfiglet
        from colorama import init, Fore

        init(autoreset=True)
        title = pyfiglet.figlet_format("DeathBox: AI Escape", font="big")
        print(Fore.CYAN + title)
        print(Fore.WHITE + "A terminal game where an AI tries to escape\n")
        print(Fore.YELLOW + "=" * 60 + "\n")
    except ImportError:
        print("=" * 60)
        print("DeathBox: AI Escape")
        print("A terminal game where an AI tries to escape")
        print("=" * 60 + "\n")


def main():
    """Main function to launch the game."""
    clear_screen()
    display_title()

    # Check dependencies
    if not check_dependencies():
        print("Some dependencies are missing.")
        choice = input("Would you like to install them now? (y/n): ").lower()

        if choice == 'y':
            if not install_dependencies():
                input("Press Enter to exit...")
                return
        else:
            print("Cannot run the game without required dependencies.")
            input("Press Enter to exit...")
            return

    print("Starting game...")
    time.sleep(1)

    try:
        # Import and run the game
        from main import Game
        game = Game()
        game.run()
    except Exception as e:
        clear_screen()
        print("An error occurred while running the game:")
        print(f"Error: {e}")
        print("\nTraceback:")
        traceback.print_exc()
        print("\nPlease report this issue to the developer.")
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
