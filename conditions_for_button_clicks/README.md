# Numpad 1 Auto-Clicker

This script automatically presses the numpad 1 key every 30 seconds. It's designed for automated key pressing in applications like Skyrim or other games where repetitive key presses are needed.

## Features

- Presses numpad 1 every 30 seconds
- Graceful exit with Ctrl+C
- Failsafe: move mouse to top-left corner to stop
- Timestamped logging of each key press
- Error handling and recovery

## Usage

### From Root Directory (Recommended)
```bash
python run_auto_clicker.py
```

### Direct Execution
```bash
python conditions_for_button_clicks/main.py
```

### With Virtual Environment
```bash
C:/Users/zakra/OneDrive/Desktop/code/skyrim/.venv/Scripts/python.exe conditions_for_button_clicks/main.py
```

## Safety Features

1. **Ctrl+C**: Stops the script immediately
2. **Failsafe**: Move your mouse to the top-left corner of the screen to stop
3. **Error Recovery**: Script continues running even if individual key presses fail

## Requirements

- Python 3.7+
- pyautogui (automatically installed with requirements.txt)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the script using one of the methods above.

## Notes

- The script will print a timestamp each time it presses the numpad 1 key
- Make sure the target application (like Skyrim) is in focus when needed
- The script runs indefinitely until manually stopped
