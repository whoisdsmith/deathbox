#!/usr/bin/env python3
"""
Cross-platform input handler for DeathBox V2
Optimized for iPhone devices using a-Shell in portrait mode
"""
import os
import sys
import time
import select


class InputHandler:
    """
    Cross-platform input handler for keyboard input.
    Optimized for iOS terminal apps, especially a-Shell.
    """

    def __init__(self):
        self.is_windows = os.name == 'nt'
        self.is_ios = False

        # Try to detect iOS terminal apps
        try:
            # Check for common iOS terminal app environment variables or paths
            if 'IPHONE' in os.environ or 'IPAD' in os.environ:
                self.is_ios = True
            # Check for a-Shell specific path
            elif os.path.exists('/var/mobile'):
                self.is_ios = True
        except:
            pass

        # Print detected platform
        if self.is_ios:
            print("iOS device detected. Optimizing for a-Shell...")
            time.sleep(1)
        elif self.is_windows:
            print("Windows detected.")
            time.sleep(1)
        else:
            print("Unix-like system detected.")
            time.sleep(1)

        if self.is_windows:
            # Windows uses msvcrt
            import msvcrt
            self.msvcrt = msvcrt
        else:
            # Unix-like systems use termios
            import termios
            import tty
            self.termios = termios
            self.tty = tty
            self.select = select
            self.stdin_fd = sys.stdin.fileno()
            try:
                self.old_settings = termios.tcgetattr(self.stdin_fd)
            except:
                # Handle case where terminal doesn't support tcgetattr
                # (some iOS terminal apps might fall here)
                self.is_ios = True
                print("Using iOS-specific input handling...")
                time.sleep(1)

    def kbhit(self):
        """Check if a key has been pressed."""
        if self.is_windows:
            return self.msvcrt.kbhit()
        elif self.is_ios:
            # iOS-specific approach with longer timeout for better responsiveness
            return self._ios_kbhit()
        else:
            dr, dw, de = self.select.select([sys.stdin], [], [], 0)
            return dr != []

    def _ios_kbhit(self):
        """iOS-specific key hit detection optimized for a-Shell."""
        try:
            # Use select with a slightly longer timeout for better responsiveness on iOS
            dr, dw, de = self.select.select([sys.stdin], [], [], 0.01)
            return dr != []
        except:
            # Fallback method if select doesn't work
            return False

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
        elif self.is_ios:
            # iOS-specific handling optimized for a-Shell
            return self._ios_getch()
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

    def _ios_getch(self):
        """iOS-specific character reading optimized for a-Shell."""
        try:
            # Try standard Unix approach first
            self.tty.setraw(self.stdin_fd)
            key = sys.stdin.read(1)

            # Handle escape sequences (arrow keys, etc.)
            if key == '\x1b':
                # iOS terminals typically use standard ANSI escape sequences
                try:
                    # Use a longer timeout for better responsiveness on iOS
                    dr, dw, de = self.select.select([sys.stdin], [], [], 0.2)
                    if dr:
                        seq = sys.stdin.read(2)
                        if seq == '[A':  # Up arrow
                            return 'UP'
                        elif seq == '[B':  # Down arrow
                            return 'DOWN'
                        elif seq == '[D':  # Left arrow
                            return 'LEFT'
                        elif seq == '[C':  # Right arrow
                            return 'RIGHT'
                except:
                    pass
                return 'SPECIAL'

            return key
        except:
            # Fallback for iOS if the above doesn't work
            try:
                # Simple blocking read
                return sys.stdin.read(1)
            except:
                # Last resort
                return None
        finally:
            try:
                # Restore terminal settings
                self.termios.tcsetattr(
                    self.stdin_fd, self.termios.TCSADRAIN, self.old_settings)
            except:
                pass

    def get_key(self):
        """
        Wait for a keypress and return the character.
        Returns None if no key is pressed within the timeout.
        """
        if self.kbhit():
            return self.getch()
        return None

    def get_key_blocking(self, timeout=None):
        """
        Wait for a keypress and return the character.
        This is a blocking call that waits until a key is pressed.

        Args:
            timeout (float, optional): Maximum time to wait for input in seconds.
                                      None means wait indefinitely.

        Returns:
            str or None: The key pressed, or None if timeout occurred.
        """
        start_time = time.time()

        while timeout is None or (time.time() - start_time) < timeout:
            key = self.get_key()
            if key:
                return key
            time.sleep(0.05)  # Small delay to prevent high CPU usage

        return None

    def cleanup(self):
        """Restore terminal settings (for Unix-like systems)."""
        if not self.is_windows and not self.is_ios:
            try:
                self.termios.tcsetattr(
                    self.stdin_fd, self.termios.TCSADRAIN, self.old_settings)
            except:
                pass


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
