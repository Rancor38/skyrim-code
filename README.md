# Skyrim Automation

Simple Python script that reads YAML configs and creates hotkeys for Skyrim console commands.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the automation:**
   ```bash
   python skyrim_automation.py
   ```

3. **Configure your hotkeys** in `keypress.yaml`

4. **Press your hotkeys in Skyrim!**

## How It Works

- **`skyrim_automation.py`** - Main script that reads YAML configs and creates hotkeys
- **`keypress.yaml`** - Your hotkey configurations (F1, F2, F3, etc.)
- **`commands.yaml`** - Reference of available Skyrim console commands
- **`ids.yaml`** - Item ID mappings for convenience

## Default Hotkeys

- **F1** - Give 10,000 gold
- **F2** - Toggle god mode  
- **F3** - Restore health/magicka/stamina

## Usage

1. Run `python skyrim_automation.py`
2. Choose whether to launch Skyrim automatically
3. Switch to Skyrim and press your configured hotkeys
4. Press `Ctrl+C` in the terminal to stop automation

The script sends console commands directly to Skyrim while it's running.

## Customization

Edit `keypress.yaml` to add your own hotkeys and commands. The script will automatically read your changes.

**That's it. Simple and straightforward.**
