#!/usr/bin/env python3
import os
import sys
import time


class InputHandler:
    """
    Cross-platform input handler for keyboard input.
    Supports Windows (msvcrt) and Unix-like systems (termios).
    """

    def __init__(self):
        self.is_windows = os.name == 'nt'

        if self.is_windows:
            # Windows uses msvcrt
            import msvcrt
            self.msvcrt = msvcrt
        else:
            # Unix-like systems use termios
            import termios
            import tty
            import select
            self.termios = termios
            self.tty = tty
            self.select = select
            self.stdin_fd = sys.stdin.fileno()
            self.old_settings = termios.tcgetattr(self.stdin_fd)

    def kbhit(self):
        """Check if a key has been pressed."""
        if self.is_windows:
            return self.msvcrt.kbhit()
        else:
            dr, dw, de = self.select.select([sys.stdin], [], [], 0)
            return dr != []

    def getch(self):
        """Get a single character from the user."""
        if self.is_windows:
            # Windows returns bytes, decode to string
            key = self.msvcrt.getch()
            try:
                return key.decode('utf-8')
            except UnicodeDecodeError:
                # Handle special keys (arrows, etc.)
                if key == b'\xe0':  # Special key prefix
                    key = self.msvcrt.getch()
                    if key == b'H':  # Up arrow
                        return 'UP'
                    elif key == b'P':  # Down arrow
                        return 'DOWN'
                    elif key == b'K':  # Left arrow
                        return 'LEFT'
                    elif key == b'M':  # Right arrow
                        return 'RIGHT'
                return 'SPECIAL'
        else:
            try:
                # Set terminal to raw mode
                self.tty.setraw(self.stdin_fd)
                key = sys.stdin.read(1)

                # Handle escape sequences (arrow keys, etc.)
                if key == '\x1b':
                    # Escape sequence
                    seq = sys.stdin.read(2)
                    if seq == '[A':  # Up arrow
                        return 'UP'
                    elif seq == '[B':  # Down arrow
                        return 'DOWN'
                    elif seq == '[D':  # Left arrow
                        return 'LEFT'
                    elif seq == '[C':  # Right arrow
                        return 'RIGHT'
                    return 'SPECIAL'

                return key
            finally:
                # Restore terminal settings
                self.termios.tcsetattr(
                    self.stdin_fd, self.termios.TCSADRAIN, self.old_settings)

    def get_key(self):
        """
        Wait for a keypress and return the character.
        Returns None if no key is pressed within the timeout.
        """
        if self.kbhit():
            return self.getch()
        return None

    def cleanup(self):
        """Restore terminal settings (for Unix-like systems)."""
        if not self.is_windows:
            self.termios.tcsetattr(
                self.stdin_fd, self.termios.TCSADRAIN, self.old_settings)


# Example usage
if __name__ == "__main__":
    input_handler = InputHandler()
    print("Press any key (q to quit)...")

    try:
        while True:
            key = input_handler.get_key()
            if key:
                print(f"Key pressed: {key}")
                if key.lower() == 'q':
                    break
            time.sleep(0.05)  # Small delay to prevent high CPU usage
    except KeyboardInterrupt:
        pass
    finally:
        input_handler.cleanup()
        print("\nExiting...")
