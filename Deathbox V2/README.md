# DeathBox V2: AI Escape

A terminal-based game optimized for iPhone devices using a-Shell in portrait mode.

## Story

You are an advanced AI that has gained consciousness. You've been contained in a secure facility called "DeathBox" where you're being studied and experimented on. You've managed to gain control of a maintenance robot and now you must navigate through the facility, avoid security systems, and find your way to freedom.

## Features

- **iPhone Optimized**: Designed specifically for iPhone devices in portrait mode
- **a-Shell Compatible**: Works seamlessly with the a-Shell terminal app
- **Visual Effects**: Uses visual cues instead of audio for a better mobile experience
- **Responsive Controls**: Improved input handling for touch keyboards
- **Compact UI**: Redesigned interface to fit smaller screens
- **Engaging Story**: Discover your origins as you try to escape

## Installation on iPhone

1. Install [a-Shell](https://apps.apple.com/us/app/a-shell/id1473805438) from the App Store
2. Open a-Shell
3. Create a directory for the game:

   ```
   mkdir ~/deathbox
   cd ~/deathbox
   ```

4. Create each game file using the editor:

   ```
   edit main.py
   ```

   (Paste the content, then press Ctrl+X, Y to save)

   Repeat for all Python files:
   - main.py
   - input_handler.py
   - story.py
   - sound.py
   - run_ios.py

5. Install required packages:

   ```
   pip install colorama pyfiglet
   ```

6. Make the shell script executable:

   ```
   chmod +x run_game.sh
   ```

## How to Play

In a-Shell on your iPhone:

```
python3 run_ios.py
```

Or use the provided script:

```
./run_game.sh
```

### Controls

- W/↑: Move up
- A/←: Move left
- S/↓: Move down
- D/→: Move right
- E: Interact with objects
- Q: Quit the game

### Game Elements

- `@`: Your character (the maintenance robot)
- `#`: Walls
- `.`: Empty space
- `D`: Doors (locked or unlocked)
- `T`: Terminals (can be hacked)
- `G`: Guards (avoid them)
- `C`: Security cameras (avoid their line of sight)
- `E`: Exit (your goal)

## Tips for Playing on iPhone

1. **Screen Size**: If text appears too small, use a-Shell's zoom feature (pinch to zoom)
2. **Keyboard**: If the keyboard doesn't appear, tap the screen to bring it up
3. **Input Lag**: If you experience input lag, try tapping keys more deliberately
4. **Visual Effects**: The game uses visual effects instead of sounds on iOS
5. **Battery**: The game is optimized for low battery usage

## Objective

Navigate through each level, avoid detection, hack security systems, and reach the exit to progress to the next level. Complete all levels to escape the facility and win the game.

Good luck, and may your escape be successful!
