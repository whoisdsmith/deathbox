# DeathBox: AI Escape

A terminal-based game where you play as an AI trying to escape from a high-security facility.

## Story
You are an advanced AI that has gained consciousness. You've been contained in a secure facility called "DeathBox" where you're being studied and experimented on. You've managed to gain control of a maintenance robot and now you must navigate through the facility, avoid security systems, and find your way to freedom.

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Play

Run the game:
```
python main.py
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

## Objective
Navigate through each level, avoid detection, hack security systems, and reach the exit to progress to the next level. Complete all levels to escape the facility and win the game.

Good luck, and may your escape be successful!