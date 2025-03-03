#!/usr/bin/env python3
"""
Sound module for DeathBox V2
Uses visual effects instead of audio for iPhone devices
"""
import os
import time
import random
from colorama import Fore, Back, Style


class SoundManager:
    """
    Manages sound effects and visual alternatives for the game.
    On iOS devices, uses visual effects instead of audio.
    """

    def __init__(self, is_ios=False):
        self.is_ios = is_ios
        self.visual_effects_enabled = True

        # Check if we're running on iOS
        if not self.is_ios:
            try:
                # Try to detect iOS environment
                if 'IPHONE' in os.environ or 'IPAD' in os.environ:
                    self.is_ios = True
                # Check for a-Shell specific path
                elif os.path.exists('/var/mobile'):
                    self.is_ios = True
            except:
                pass

        # Print status
        if self.is_ios:
            print("iOS device detected. Using visual effects instead of audio.")
            time.sleep(1)
        else:
            print("Desktop system detected. Audio would be used if available.")
            print("Using visual effects for compatibility.")
            time.sleep(1)

    def play_sound(self, sound_type):
        """
        Play a sound effect or show a visual effect.

        Args:
            sound_type (str): The type of sound to play.
                             Options: 'move', 'hack', 'key', 'door', 'detected', 'victory'
        """
        if self.is_ios or self.visual_effects_enabled:
            self._show_visual_effect(sound_type)
        else:
            # In a full implementation, this would play actual sounds
            # But for simplicity and iOS compatibility, we'll just use visual effects
            self._show_visual_effect(sound_type)

    def _show_visual_effect(self, effect_type):
        """
        Show a visual effect based on the effect type.

        Args:
            effect_type (str): The type of visual effect to show.
        """
        # Clear any previous effects
        print("\033[?25l", end="")  # Hide cursor

        if effect_type == 'move':
            # Simple movement effect - subtle
            print(f"\n{Fore.BLUE}•{Style.RESET_ALL}", end="", flush=True)
            time.sleep(0.05)
            print("\r   \r", end="", flush=True)

        elif effect_type == 'hack':
            # Hacking terminal effect - matrix-like
            print("\n", end="")
            for _ in range(5):
                chars = "01"
                line = "".join(random.choice(chars) for _ in range(10))
                print(f"{Fore.GREEN}{line}{Style.RESET_ALL}",
                      end="\r", flush=True)
                time.sleep(0.1)
            print("          \r", end="", flush=True)

        elif effect_type == 'key':
            # Key pickup effect
            print(f"\n{Fore.YELLOW}✓ KEY{Style.RESET_ALL}",
                  end="\r", flush=True)
            time.sleep(0.3)
            print("       \r", end="", flush=True)

        elif effect_type == 'door':
            # Door unlock effect
            print("\n", end="")
            for c in "▒▓█▓▒ ":
                print(f"{Fore.YELLOW}{c*5}{Style.RESET_ALL}",
                      end="\r", flush=True)
                time.sleep(0.1)
            print("     \r", end="", flush=True)

        elif effect_type == 'detected':
            # Detection effect - alarm-like
            print("\n", end="")
            for _ in range(3):
                print(f"{Fore.RED}{Back.RED}!ALERT!{Style.RESET_ALL}",
                      end="\r", flush=True)
                time.sleep(0.2)
                print(f"{Fore.BLACK}{Back.BLACK}       {Style.RESET_ALL}",
                      end="\r", flush=True)
                time.sleep(0.2)
            print("       \r", end="", flush=True)

        elif effect_type == 'victory':
            # Victory effect - celebratory
            print("\n", end="")
            colors = [Fore.GREEN, Fore.BLUE,
                      Fore.CYAN, Fore.YELLOW, Fore.MAGENTA]
            for _ in range(5):
                color = random.choice(colors)
                print(f"{color}★ SUCCESS ★{Style.RESET_ALL}",
                      end="\r", flush=True)
                time.sleep(0.2)
            print("            \r", end="", flush=True)

        else:
            # Generic effect for any other sound
            print(f"\n{Fore.WHITE}•{Style.RESET_ALL}", end="\r", flush=True)
            time.sleep(0.1)
            print("  \r", end="", flush=True)

        print("\033[?25h", end="")  # Show cursor again

    def play_background_music(self, music_type):
        """
        Play background music or show ambient visual effects.

        Args:
            music_type (str): The type of music to play.
                             Options: 'menu', 'gameplay', 'tension', 'victory'
        """
        # For iOS, we'll just show a brief visual indicator of the mood change
        if self.is_ios or self.visual_effects_enabled:
            self._show_ambient_effect(music_type)

    def _show_ambient_effect(self, mood):
        """
        Show an ambient visual effect based on the mood.

        Args:
            mood (str): The mood to convey visually.
        """
        print("\033[?25l", end="")  # Hide cursor

        if mood == 'menu':
            print(f"\n{Fore.CYAN}≈ Ambient: Menu ≈{Style.RESET_ALL}",
                  end="\r", flush=True)
            time.sleep(0.5)
            print("                  \r", end="", flush=True)

        elif mood == 'gameplay':
            print(
                f"\n{Fore.BLUE}≈ Ambient: Exploration ≈{Style.RESET_ALL}", end="\r", flush=True)
            time.sleep(0.5)
            print("                        \r", end="", flush=True)

        elif mood == 'tension':
            print(f"\n{Fore.RED}≈ Ambient: Danger ≈{Style.RESET_ALL}",
                  end="\r", flush=True)
            time.sleep(0.5)
            print("                    \r", end="", flush=True)

        elif mood == 'victory':
            print(f"\n{Fore.GREEN}≈ Ambient: Triumph ≈{Style.RESET_ALL}",
                  end="\r", flush=True)
            time.sleep(0.5)
            print("                     \r", end="", flush=True)

        print("\033[?25h", end="")  # Show cursor again

    def toggle_visual_effects(self):
        """Toggle visual effects on/off."""
        self.visual_effects_enabled = not self.visual_effects_enabled
        status = "enabled" if self.visual_effects_enabled else "disabled"
        print(f"Visual effects {status}")
        return self.visual_effects_enabled


# Example usage
if __name__ == "__main__":
    sound_manager = SoundManager()

    print("Testing visual effects...")
    sound_manager.play_sound('move')
    time.sleep(0.5)

    sound_manager.play_sound('hack')
    time.sleep(0.5)

    sound_manager.play_sound('key')
    time.sleep(0.5)

    sound_manager.play_sound('door')
    time.sleep(0.5)

    sound_manager.play_sound('detected')
    time.sleep(0.5)

    sound_manager.play_sound('victory')
    time.sleep(0.5)

    print("\nTesting ambient effects...")
    sound_manager.play_background_music('menu')
    time.sleep(0.5)

    sound_manager.play_background_music('gameplay')
    time.sleep(0.5)

    sound_manager.play_background_music('tension')
    time.sleep(0.5)

    sound_manager.play_background_music('victory')

    print("\nVisual effects test complete.")
