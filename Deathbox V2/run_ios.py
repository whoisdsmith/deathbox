#!/usr/bin/env python3
"""
iOS-specific launcher for DeathBox V2: AI Escape
Optimized for iPhone devices using a-Shell in portrait mode
"""
import os
import sys
import time
import subprocess
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)


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
    """Display iOS-specific tips for portrait mode."""
    clear_screen()
    print(f"{Fore.CYAN}{'=' * 40}")
    print(f"{Fore.CYAN}DeathBox V2: AI Escape")
    print(f"{Fore.CYAN}iOS Edition - Portrait Mode")
    print(f"{Fore.CYAN}{'=' * 40}")
    print()
    print(f"{Fore.YELLOW}TIPS FOR PLAYING ON IPHONE:")
    print(f"{Fore.WHITE}1. This version is optimized for")
    print(f"{Fore.WHITE}   portrait mode on iPhone")
    print()
    print(f"{Fore.WHITE}2. If text appears too small,")
    print(f"{Fore.WHITE}   use a-Shell's zoom feature")
    print(f"{Fore.WHITE}   (pinch to zoom)")
    print()
    print(f"{Fore.WHITE}3. If keyboard doesn't show,")
    print(f"{Fore.WHITE}   tap the screen to bring it up")
    print()
    print(f"{Fore.WHITE}4. Game uses visual effects")
    print(f"{Fore.WHITE}   instead of sounds on iOS")
    print()
    print(f"{Fore.WHITE}5. If you experience input lag,")
    print(f"{Fore.WHITE}   try tapping keys more deliberately")
    print()
    print(f"{Fore.WHITE}6. Controls:")
    print(f"{Fore.WHITE}   [↑↓←→] or [WASD]: Move")
    print(f"{Fore.WHITE}   [E]: Interact")
    print(f"{Fore.WHITE}   [Q]: Quit game")
    print()
    print(f"{Fore.CYAN}{'=' * 40}")
    input(f"{Fore.GREEN}Press Enter to continue...")


def check_screen_size():
    """Check if the terminal screen size is adequate."""
    try:
        # Get terminal size
        columns, lines = os.get_terminal_size()

        if columns < 40 or lines < 24:
            clear_screen()
            print(f"{Fore.YELLOW}WARNING: Small screen detected")
            print(f"{Fore.YELLOW}Current size: {columns}x{lines}")
            print(f"{Fore.YELLOW}Recommended: 40x24 or larger")
            print()
            print(f"{Fore.WHITE}The game may not display correctly.")
            print(f"{Fore.WHITE}Try these solutions:")
            print(f"{Fore.WHITE}1. Use a smaller font size")
            print(f"{Fore.WHITE}2. Use a-Shell's zoom feature")
            print()
            input(f"{Fore.GREEN}Press Enter to continue anyway...")

        return True
    except:
        # If we can't get the terminal size, just continue
        return True


def main():
    """Main function to launch the game."""
    clear_screen()

    # Display welcome message
    print(f"{Fore.CYAN}{'=' * 40}")
    print(f"{Fore.CYAN}DeathBox V2: AI Escape")
    print(f"{Fore.CYAN}iOS Edition")
    print(f"{Fore.CYAN}{'=' * 40}")
    print()

    # Check if running on iOS
    if not check_ios():
        print(f"{Fore.YELLOW}This launcher is designed for iOS devices.")
        print(f"{Fore.YELLOW}On desktop systems, you can still run the game,")
        print(f"{Fore.YELLOW}but some features may not work as expected.")
        print()
        input(f"{Fore.GREEN}Press Enter to continue anyway or Ctrl+C to exit...")

    # Check screen size
    check_screen_size()

    # Display iOS-specific tips
    display_ios_tips()

    # Check dependencies
    if not check_dependencies():
        print(f"{Fore.YELLOW}Some dependencies are missing.")
        choice = input(
            f"{Fore.GREEN}Would you like to install them now? (y/n): ").lower()

        if choice == 'y':
            if not install_dependencies():
                input(f"{Fore.RED}Press Enter to exit...")
                return
        else:
            print(f"{Fore.RED}Cannot run the game without required dependencies.")
            input(f"{Fore.RED}Press Enter to exit...")
            return

    clear_screen()
    print(f"{Fore.CYAN}Starting DeathBox V2: AI Escape...")
    print(f"{Fore.CYAN}Optimizing for iOS environment...")

    # Show loading animation
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(0.3)
    print()

    try:
        # Import and run the game
        from main import Game
        game = Game()
        game.run()
    except Exception as e:
        clear_screen()
        print(f"{Fore.RED}An error occurred while running the game:")
        print(f"{Fore.RED}Error: {e}")
        print()
        print(f"{Fore.YELLOW}Please report this issue to the developer.")
        input(f"{Fore.GREEN}Press Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
        sys.exit(0)
