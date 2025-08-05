#!/usr/bin/env python3
"""
Skyrim HybridCommander Preset Generator
=======================================
Complete application for generating HybridCommander presets from YAML configuration.
Reads config.yaml and creates JSON presets that HybridCommander can use for 
background console command execution via powers/hotkeys.

Usage: python skyrim_preset_generator.py
"""

import yaml
import json
import os
import shutil
import sys
from pathlib import Path

class SkyrimPresetGenerator:
    def __init__(self):
        self.commands_data = {}
        self.keybinds_data = {}
        self.ids_data = {}
        
        # HybridCommander paths
        self.skyrim_data_path = r"C:\Program Files (x86)\Steam\steamapps\common\Skyrim Special Edition\Data"
        self.hybrid_config_path = os.path.join(self.skyrim_data_path, "SKSE", "Plugins", "StorageUtilData")
        self.hybrid_command_file = os.path.join(self.hybrid_config_path, "HybridCommander-Command.json")
        self.hybrid_config_file = os.path.join(self.hybrid_config_path, "HybridCommander-Config.json")
        
    def load_configs(self):
        """Load all YAML configuration files"""
        try:
            # Load commands reference
            with open('commands.yaml', 'r', encoding='utf-8') as f:
                self.commands_data = yaml.safe_load(f)
                
            # Load preset configurations  
            with open('config.yaml', 'r', encoding='utf-8') as f:
                self.keybinds_data = yaml.safe_load(f)
                
            # Load item IDs if exists
            if os.path.exists('ids.yaml'):
                with open('ids.yaml', 'r', encoding='utf-8') as f:
                    self.ids_data = yaml.safe_load(f)
                    
            print("✅ Loaded configuration files")
            return True
            
        except Exception as e:
            print(f"❌ Error loading configs: {e}")
            return False
    
    def check_hybrid_commander(self):
        """Check if HybridCommander is installed and accessible"""
        if not os.path.exists(self.hybrid_command_file):
            print(f"❌ HybridCommander not found at: {self.hybrid_command_file}")
            print("📋 Make sure HybridCommander mod is installed and enabled in Vortex")
            print("\n🎯 HybridCommander Integration Benefits:")
            print("   • Execute console commands in background (no console opening)")
            print("   • Bind commands to in-game powers")
            print("   • More reliable than keyboard automation")
            print("   • Commands work even if game loses focus")
            return False
            
        print("✅ HybridCommander detected!")
        return True
    
    def load_hybrid_commander_data(self):
        """Load existing HybridCommander configuration"""
        try:
            # Load command definitions
            with open(self.hybrid_command_file, 'r', encoding='utf-8') as f:
                self.hybrid_data = json.load(f)
                
            # Load or create config file with proper HybridCommander structure
            if os.path.exists(self.hybrid_config_file):
                with open(self.hybrid_config_file, 'r', encoding='utf-8') as f:
                    self.hybrid_config = json.load(f)
                print("✅ Loaded existing HybridCommander configuration")
            else:
                # Create proper HybridCommander structure based on source code analysis
                self.hybrid_config = {
                    "string": {},
                    "int": {},
                    "float": {},
                    "stringList": {
                        "PresetName": [""] * 50,  # 50 empty preset slots (intPresetLength)
                        "PowerName": [""] * 10    # 10 power slots (intPowerLength)
                    },
                    "intList": {
                        "HotkeyCode": [-1] * 10,      # 10 hotkey slots with -1 (unbound)
                        "HotkeyModifier": [0] * 10,   # 10 modifier slots
                        "HotkeyPreset": [0] * 10,     # 10 preset assignment slots
                        "PowerPreset": [0] * 10       # 10 power preset assignments
                    }
                }
                
                # Initialize all 50 preset command lists (each with 10 command slots)
                for i in range(50):
                    self.hybrid_config["stringList"][str(i)] = [""] * 10
                
                print("✅ Created new HybridCommander configuration structure")
                
            return True
            
        except Exception as e:
            print(f"❌ Error loading HybridCommander data: {e}")
            return False
    
    def resolve_command(self, function_name, args):
        """Convert function calls to actual console commands"""
        if function_name == "give_item":
            item_id, amount = args
            if item_id == "currency.gold":
                return f"player.additem 0000000f {amount}"
            else:
                # Look up item ID from ids.yaml or use directly
                actual_id = self.get_item_id(item_id)
                return f"player.additem {actual_id} {amount}"
                
        elif function_name == "execute_command":
            command_path = args[0]
            # Check if it's a direct console command (contains spaces or periods)
            if " " in command_path or "." in command_path:
                return command_path  # Return direct console command as-is
            else:
                return self.get_command_by_path(command_path)  # Look up in commands.yaml
            
        elif function_name == "set_player_stat":
            stat_name, value = args
            return f"player.setav {stat_name} {value}"
            
        elif function_name == "modify_player_stat":
            stat_name, value = args
            return f"player.modav {stat_name} {value}"
            
        elif function_name == "teleport_to":
            location_id = args[0]
            return f"coc {location_id}"
            
        elif function_name == "give_spell":
            spell_id = args[0]
            return f"player.addspell {spell_id}"
            
        elif function_name == "complete_quest":
            quest_id = args[0]
            return f"completequest {quest_id}"
            
        elif function_name == "set_weather":
            weather_id = args[0]
            return f"fw {weather_id}"
            
        else:
            print(f"⚠️ Unknown function: {function_name}")
            return None
    
    def get_command_by_path(self, path):
        """Get command from commands.yaml using dot notation"""
        parts = path.split('.')
        data = self.commands_data
        
        for part in parts:
            if part in data:
                data = data[part]
            else:
                return path  # Return as-is if not found
                
        return data
    
    def get_item_id(self, item_name):
        """Get item ID from ids.yaml or return as-is"""
        if self.ids_data and item_name in self.ids_data:
            return self.ids_data[item_name]
        return item_name
    
    def create_hybrid_commander_preset(self, preset_name, commands):
        """Create a new preset in HybridCommander with the given commands"""
        try:
            # Find first available preset slot (look for empty name or spaces)
            preset_names = self.hybrid_config["stringList"]["PresetName"]
            preset_index = None
            
            for i, name in enumerate(preset_names):
                if not name or name.strip() == "":  # Empty or whitespace-only slot found
                    preset_index = i
                    break
                    
            if preset_index is None:
                print(f"❌ No available preset slots (all 50 slots are full)")
                return None
            
            # Set the preset name
            self.hybrid_config["stringList"]["PresetName"][preset_index] = preset_name
            
            # Clear and set commands for this preset (max 10 commands per preset)
            preset_commands = [""] * 10  # Initialize with 10 empty slots
            for i, cmd in enumerate(commands[:10]):  # Take max 10 commands
                preset_commands[i] = cmd
                
            self.hybrid_config["stringList"][str(preset_index)] = preset_commands
                
            print(f"📝 Created HybridCommander preset: {preset_name} (slot {preset_index})")
            print(f"   Commands: {', '.join([cmd for cmd in commands[:10] if cmd])}")
            return preset_index
            
        except Exception as e:
            print(f"❌ Error creating preset: {e}")
            return None
    
    def save_hybrid_commander_config(self):
        """Save the modified HybridCommander configuration"""
        try:
            # Ensure directory exists
            os.makedirs(self.hybrid_config_path, exist_ok=True)
            
            # Backup original config
            backup_file = self.hybrid_config_file + ".backup"
            if os.path.exists(self.hybrid_config_file) and not os.path.exists(backup_file):
                shutil.copy2(self.hybrid_config_file, backup_file)
                print("💾 Created backup of HybridCommander config")
            
            # Save new config
            with open(self.hybrid_config_file, 'w', encoding='utf-8') as f:
                json.dump(self.hybrid_config, f, indent=2)
                
            print("✅ Saved HybridCommander configuration")
            return True
            
        except Exception as e:
            print(f"❌ Error saving HybridCommander config: {e}")
            return False
    
    def clear_python_presets(self):
        """Clear existing Python-generated presets to avoid duplicates"""
        preset_names = self.hybrid_config["stringList"]["PresetName"]
        
        # Find and clear slots with Python_ prefix
        cleared_count = 0
        for i, name in enumerate(preset_names):
            if name.startswith("Python_"):
                # Clear the preset name
                self.hybrid_config["stringList"]["PresetName"][i] = ""
                # Clear the command list for this slot
                self.hybrid_config["stringList"][str(i)] = [""] * 10
                cleared_count += 1
                
        if cleared_count > 0:
            print(f"🧹 Cleared {cleared_count} existing Python presets")
        
        return cleared_count
    
    def setup_hybrid_integration(self):
        """Create HybridCommander presets for each preset configuration"""
        if 'keybinds' not in self.keybinds_data:
            print("❌ No keybinds found in config.yaml")
            return
        
        # Clear existing Python presets first
        self.clear_python_presets()
            
        created_presets = 0
        
        for key, config in self.keybinds_data['keybinds'].items():
            name = config.get('name', key)
            description = config.get('description', 'No description')
            commands = config.get('commands', [])
            
            print(f"🔗 Setting up HybridCommander preset for {key}: {description}")
            
            # Convert YAML commands to console commands
            console_commands = []
            for cmd_config in commands:
                function = cmd_config.get('function')
                args = cmd_config.get('args', [])
                
                console_command = self.resolve_command(function, args)
                if console_command:
                    console_commands.append(console_command)
            
            if console_commands:
                # Create preset in HybridCommander
                preset_name = f"Python_{name}_{key}"
                preset_index = self.create_hybrid_commander_preset(preset_name, console_commands)
                
                if preset_index is not None:
                    print(f"✅ Created preset #{preset_index}: {preset_name}")
                    print(f"   Commands: {', '.join(console_commands)}")
                    created_presets += 1
            else:
                print(f"⚠️ No valid commands found for {key}")
        
        print(f"\n📊 Created {created_presets} presets total")
        return created_presets
    
    def run(self):
        """Main execution loop"""
        print("=" * 60)
        print("🐉 SKYRIM HYBRIDCOMMANDER PRESET GENERATOR")
        print("=" * 60)
        
        # Load configurations
        if not self.load_configs():
            return False
        
        # Check HybridCommander installation
        if not self.check_hybrid_commander():
            return False
        
        # Load HybridCommander data
        if not self.load_hybrid_commander_data():
            return False
        
        # Create presets for each hotkey
        created_count = self.setup_hybrid_integration()
        
        if created_count == 0:
            print("❌ No presets were created")
            return False
        
        # Save configuration
        if not self.save_hybrid_commander_config():
            return False
        
        print("\n" + "=" * 60)
        print("✅ HYBRIDCOMMANDER PRESET GENERATION COMPLETE")
        print("=" * 60)
        print("🎮 Your presets are now available in HybridCommander!")
        print("\n📋 CREATED PRESETS:")
        
        # Show what presets were created
        preset_names = self.hybrid_config["stringList"]["PresetName"]
        active_presets = [(i, name) for i, name in enumerate(preset_names) if name != ""]
        
        for i, name in active_presets:
            # Extract the key name from the preset name
            key_part = name.split('_')[-1] if '_' in name else f"Slot{i}"
            print(f"   • Slot {i:02d}: {name} ({key_part})")
            
        print("\n🎮 TO USE IN SKYRIM:")
        print("   1. **RESTART SKYRIM** (HybridCommander loads config on startup)")
        print("   2. In-game, open MCM (Mod Configuration Menu)")
        print("   3. Navigate to: HybridCommander → Preset List")
        print("   4. You should see your presets:")
        for i, name in active_presets:
            key_part = name.split('_')[-1] if '_' in name else f"Slot{i}"
            description = name.replace('Python_', '').replace(f'_{key_part}', '').replace('_', ' ')
            print(f"      - Slot {i:02d}: {description} ({key_part})")
        print("   5. Go to HybridCommander → Hotkey/Power pages to assign them")
        print("   6. Test your commands!")
        print("\n💡 TIP: Assign these to numpad keys in HybridCommander for intuitive use:")
        print("   • Numpad1-8: Basic utilities and enhancements")
        print("   • Numpad9,0,Period,Plus: Advanced skills and unlocks")
        print("\n🔄 Re-run this script to update presets when you change config.yaml")
        print("=" * 60)
        
        return True

def main():
    """Main application entry point"""
    print("🚀 Starting Skyrim Preset Generator...")
    
    # Check if we're in the right directory
    if not os.path.exists('commands.yaml') or not os.path.exists('config.yaml'):
        print("❌ Missing YAML config files!")
        print("📁 Make sure you're in the skyrim project directory")
        print("📁 Required files: commands.yaml, config.yaml")
        sys.exit(1)
    
    print("✅ Found required config files")
    
    # Run the preset generator
    try:
        generator = SkyrimPresetGenerator()
        success = generator.run()
        
        if success:
            print("\n🎉 Application completed successfully!")
            return 0
        else:
            print("\n❌ Application failed to complete")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Application interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
