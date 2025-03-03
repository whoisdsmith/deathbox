#!/usr/bin/env python3
import os
import sys
import time
import random
import threading


class SoundManager:
    """
    A simple sound manager that uses terminal beeps and ASCII art
    to create a sound-like experience without external dependencies.
    """

    def __init__(self, enable_sound=True):
        self.enable_sound = enable_sound
        self.background_thread = None
        self.stop_background = False

    def beep(self, frequency=440, duration=0.1):
        """
        Make a beep sound using the terminal bell.
        This is a simple way to create sound without external libraries.
        """
        if not self.enable_sound:
            return

        if os.name == 'nt':  # Windows
            try:
                import winsound
                winsound.Beep(frequency, int(duration * 1000))
            except (ImportError, RuntimeError):
                print('\a', end='', flush=True)  # Fallback to terminal bell
        else:  # Unix/Linux/Mac
            print('\a', end='', flush=True)
            time.sleep(duration)

    def play_sound(self, sound_type):
        """Play a specific sound effect."""
        if sound_type == "terminal_hack":
            self._play_terminal_hack()
        elif sound_type == "door_unlock":
            self._play_door_unlock()
        elif sound_type == "key_pickup":
            self._play_key_pickup()
        elif sound_type == "detected":
            self._play_detected()
        elif sound_type == "level_complete":
            self._play_level_complete()
        elif sound_type == "game_over":
            self._play_game_over()
        elif sound_type == "game_win":
            self._play_game_win()

    def _play_terminal_hack(self):
        """Sound for hacking a terminal."""
        for _ in range(5):
            self.beep(880, 0.05)
            time.sleep(0.05)
        self.beep(1760, 0.2)

    def _play_door_unlock(self):
        """Sound for unlocking a door."""
        self.beep(440, 0.1)
        time.sleep(0.1)
        self.beep(660, 0.2)

    def _play_key_pickup(self):
        """Sound for picking up a key."""
        self.beep(1320, 0.1)

    def _play_detected(self):
        """Sound for being detected."""
        for _ in range(3):
            self.beep(220, 0.2)
            time.sleep(0.1)

    def _play_level_complete(self):
        """Sound for completing a level."""
        self.beep(523, 0.1)  # C
        time.sleep(0.1)
        self.beep(659, 0.1)  # E
        time.sleep(0.1)
        self.beep(784, 0.1)  # G
        time.sleep(0.1)
        self.beep(1047, 0.3)  # C (octave up)

    def _play_game_over(self):
        """Sound for game over."""
        self.beep(880, 0.1)
        time.sleep(0.1)
        self.beep(830, 0.1)
        time.sleep(0.1)
        self.beep(784, 0.1)
        time.sleep(0.1)
        self.beep(740, 0.1)
        time.sleep(0.1)
        self.beep(698, 0.3)

    def _play_game_win(self):
        """Sound for winning the game."""
        self.beep(523, 0.1)  # C
        time.sleep(0.1)
        self.beep(659, 0.1)  # E
        time.sleep(0.1)
        self.beep(784, 0.1)  # G
        time.sleep(0.1)
        self.beep(1047, 0.2)  # C (octave up)
        time.sleep(0.2)
        self.beep(1047, 0.4)  # C (octave up)

    def _background_music_thread(self):
        """Thread function for background music."""
        notes = [
            (440, 0.2),   # A
            (494, 0.2),   # B
            (523, 0.2),   # C
            (587, 0.2),   # D
            (659, 0.2),   # E
            (698, 0.2),   # F
            (784, 0.2),   # G
        ]

        while not self.stop_background:
            # Play a random sequence of notes
            for _ in range(random.randint(3, 6)):
                if self.stop_background:
                    break

                note = random.choice(notes)
                self.beep(note[0], note[1])
                time.sleep(random.uniform(0.5, 1.5))

            # Pause between sequences
            time.sleep(random.uniform(2.0, 4.0))

    def start_background_music(self):
        """Start playing background music in a separate thread."""
        if self.background_thread is not None and self.background_thread.is_alive():
            return  # Already playing

        self.stop_background = False
        self.background_thread = threading.Thread(
            target=self._background_music_thread)
        self.background_thread.daemon = True
        self.background_thread.start()

    def stop_background_music(self):
        """Stop the background music."""
        self.stop_background = True
        if self.background_thread is not None:
            self.background_thread.join(1.0)  # Wait for thread to finish
            self.background_thread = None

    def display_visual_effect(self, effect_type):
        """Display a visual effect as an alternative to sound."""
        if effect_type == "terminal_hack":
            self._display_hack_effect()
        elif effect_type == "detected":
            self._display_alert_effect()

    def _display_hack_effect(self):
        """Display a hacking visual effect."""
        hack_frames = [
            "  HACKING...  ",
            " [=         ] ",
            " [==        ] ",
            " [===       ] ",
            " [====      ] ",
            " [=====     ] ",
            " [======    ] ",
            " [=======   ] ",
            " [========  ] ",
            " [========= ] ",
            " [==========] ",
            "  ACCESS GRANTED  "
        ]

        for frame in hack_frames:
            sys.stdout.write('\r' + frame)
            sys.stdout.flush()
            time.sleep(0.1)
        print()

    def _display_alert_effect(self):
        """Display an alert visual effect."""
        alert_frames = [
            "  !!! ALERT !!!  ",
            " !!! ALERT !!! ",
            "!!! ALERT !!!",
            " !!! ALERT !!! ",
            "  !!! ALERT !!!  ",
        ]

        for _ in range(3):
            for frame in alert_frames:
                sys.stdout.write('\r' + frame)
                sys.stdout.flush()
                time.sleep(0.1)
        print()


# Example usage
if __name__ == "__main__":
    sound_manager = SoundManager()

    print("Testing sound effects...")
    sound_manager.play_sound("terminal_hack")
    time.sleep(1)

    sound_manager.play_sound("door_unlock")
    time.sleep(1)

    sound_manager.play_sound("key_pickup")
    time.sleep(1)

    sound_manager.play_sound("detected")
    time.sleep(1)

    sound_manager.play_sound("level_complete")
    time.sleep(1)

    print("Testing visual effects...")
    sound_manager.display_visual_effect("terminal_hack")
    time.sleep(1)

    sound_manager.display_visual_effect("detected")
    time.sleep(1)

    print("Testing background music (will play for 10 seconds)...")
    sound_manager.start_background_music()
    time.sleep(10)
    sound_manager.stop_background_music()

    print("Sound test complete!")
