# DeathBox: AI Escape

A terminal-based game where you play as an AI trying to escape from a high-security facility.

## Story
You are an advanced AI that has gained consciousness. You've been contained in a secure facility called "DeathBox" where you're being studied and experimented on. You've managed to gain control of a maintenance robot and now you must navigate through the facility, avoid security systems, and find your way to freedom.

## Installation

### Desktop (Windows, macOS, Linux)
1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### iOS (iPhone/iPad)
You can run this game on iOS devices using terminal apps from the App Store:

1. Install a terminal app that supports Python:
   - [a-Shell](https://apps.apple.com/us/app/a-shell/id1473805438) (Recommended)
   - [iSH Shell](https://apps.apple.com/us/app/ish-shell/id1436902243)
   - [Pythonista](https://apps.apple.com/us/app/pythonista-3/id1085978097)

2. Using a-Shell (easiest method):
   - Open a-Shell
   - Create a directory for the game:
     ```
     mkdir ~/deathbox
     cd ~/deathbox
     ```
   - Create each game file using the editor:
     ```
     edit main.py
     ```
     (Paste the content, then press Ctrl+X, Y to save)
     Repeat for all Python files (input_handler.py, story.py, sound.py, run_game.py, run_ios.py)
   - Install required packages:
     ```
     pip install colorama pyfiglet
     ```
   - Make the shell script executable:
     ```
     chmod +x run_game.sh
     ```

## How to Play

### Desktop
Run the game:
```
python main.py
```
Or use the provided scripts:
- Windows: Double-click `run_game.bat`
- macOS/Linux: `./run_game.sh`

### iOS
In a-Shell or other terminal app:
```
python3 run_ios.py
```
The iOS launcher provides:
- iOS-specific optimizations
- Helpful tips for playing on mobile
- Automatic dependency installation
- Better error handling for mobile environments

Alternatively, you can run:
```
python3 run_game.py
```
Or:
```
./run_game.sh
```

**Note for iOS users:**
- Hold your device in landscape orientation for the best display
- Some visual elements might appear differently due to the smaller screen
- The game uses visual effects instead of sound on iOS
- If the keyboard doesn't appear, tap the screen to bring it up
- If you experience input lag, try tapping keys more deliberately

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

## Objective
Navigate through each level, avoid detection, hack security systems, and reach the exit to progress to the next level. Complete all levels to escape the facility and win the game.

Good luck, and may your escape be successful!