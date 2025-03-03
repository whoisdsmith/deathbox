#!/usr/bin/env python3
"""
iOS-specific launcher for DeathBox: AI Escape
This script helps run the game on iOS terminal apps like a-Shell
"""
import os
import sys
import time
import subprocess


def clear_screen():
    """Clear the terminal screen."""
    print("\033c", end="")  # ANSI escape sequence to clear screen


def check_ios():
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


def check_dependencies():
    """Check if required dependencies are installed."""
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
            [sys.executable, "-m", "pip", "install", "colorama", "pyfiglet"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install dependencies.")
        print("Please install them manually:")
        print("pip install colorama pyfiglet")
        return False


def display_ios_tips():
    """Display iOS-specific tips."""
    print("=" * 60)
    print("iOS TIPS FOR DEATHBOX: AI ESCAPE")
    print("=" * 60)
    print("1. Hold your device in LANDSCAPE orientation for best display")
    print("2. If text appears too small, use the terminal app's zoom feature")
    print("3. If keyboard doesn't show, tap the screen to bring it up")
    print("4. Game uses visual effects instead of sounds on iOS")
    print("5. If you experience input lag, try tapping keys more deliberately")
    print("=" * 60)
    input("Press Enter to continue...")


def main():
    """Main function to launch the game."""
    clear_screen()

    # Check if running on iOS
    if not check_ios():
        print("This launcher is designed for iOS devices.")
        print("On desktop systems, please use run_game.py instead.")
        input("Press Enter to continue anyway or Ctrl+C to exit...")

    # Display iOS-specific tips
    display_ios_tips()

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

    clear_screen()
    print("Starting DeathBox: AI Escape...")
    print("Optimizing for iOS environment...")
    time.sleep(2)

    try:
        # Import and run the game
        from main import Game
        game = Game()
        game.run()
    except Exception as e:
        clear_screen()
        print("An error occurred while running the game:")
        print(f"Error: {e}")
        print("\nPlease report this issue to the developer.")
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
        sys.exit(0)
