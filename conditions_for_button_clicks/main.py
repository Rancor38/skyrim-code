"""
Automated Numpad 1 Key Presser for Skyrim Special Edition
Uses multiple methods including AutoHotkey for maximum compatibility.
Must run as Administrator for Skyrim compatibility.
"""

import ctypes
import ctypes.wintypes
import time
import signal
import sys
import subprocess
import os
import tempfile


# Windows API constants
VK_NUMPAD1 = 0x61
KEYEVENTF_KEYUP = 0x0002
INPUT_KEYBOARD = 1

# Input structures for SendInput
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.wintypes.WORD),
        ("wScan", ctypes.wintypes.WORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))
    ]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("ki", KEYBDINPUT)]
    
    _anonymous_ = ("_input",)
    _fields_ = [
        ("type", ctypes.wintypes.DWORD),
        ("_input", _INPUT)
    ]


def check_autohotkey():
    """Check if AutoHotkey is installed"""
    try:
        # Try common AutoHotkey installation paths
        ahk_paths = [
            r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
            r"C:\Program Files (x86)\AutoHotkey\AutoHotkey.exe",
            r"C:\Users\%USERNAME%\AppData\Local\Programs\AutoHotkey\AutoHotkey.exe"
        ]
        
        for path in ahk_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                return expanded_path
        
        # Try to find it in PATH
        result = subprocess.run(['where', 'AutoHotkey.exe'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
        
        return None
    except:
        return None


def press_numpad1_autohotkey():
    """Press numpad 1 using AutoHotkey - most reliable for games"""
    try:
        ahk_path = check_autohotkey()
        if not ahk_path:
            return False
        
        # Create temporary AutoHotkey script
        ahk_script = """
; Skyrim numpad 1 press
Send, {Numpad1}
Sleep, 50
ExitApp
        """
        
        # Write script to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ahk', delete=False) as f:
            f.write(ahk_script)
            temp_script = f.name
        
        try:
            # Run AutoHotkey script
            result = subprocess.run([ahk_path, temp_script], 
                                  timeout=5, capture_output=True)
            return result.returncode == 0
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_script)
            except:
                pass
                
    except Exception as e:
        return False


def is_admin():
    """Check if script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def press_numpad1_hardware():
    """Press numpad 1 using hardware scan codes - bypasses most game filters"""
    try:
        # Hardware scan code for Numpad 1
        NUMPAD1_SCANCODE = 0x4F
        
        # Send hardware scan code directly
        ctypes.windll.user32.keybd_event(0, NUMPAD1_SCANCODE, 0x0008, 0)  # Key down with scan code
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(0, NUMPAD1_SCANCODE, 0x0008 | 0x0002, 0)  # Key up with scan code
        return True
    except:
        return False


def press_numpad1_direct_input():
    """Press numpad 1 using direct input structures"""
    try:
        # More advanced SendInput with scan codes
        key_down = INPUT()
        key_down.type = INPUT_KEYBOARD
        key_down.ki.wVk = 0  # No virtual key
        key_down.ki.wScan = 0x4F  # Hardware scan code for Numpad 1
        key_down.ki.dwFlags = 0x0008  # KEYEVENTF_SCANCODE
        key_down.ki.time = 0
        key_down.ki.dwExtraInfo = None
        
        key_up = INPUT()
        key_up.type = INPUT_KEYBOARD
        key_up.ki.wVk = 0
        key_up.ki.wScan = 0x4F
        key_up.ki.dwFlags = 0x0008 | 0x0002  # KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
        key_up.ki.time = 0
        key_up.ki.dwExtraInfo = None
        
        # Send both events
        result1 = ctypes.windll.user32.SendInput(1, ctypes.byref(key_down), ctypes.sizeof(INPUT))
        time.sleep(0.05)
        result2 = ctypes.windll.user32.SendInput(1, ctypes.byref(key_up), ctypes.sizeof(INPUT))
        
        return result1 == 1 and result2 == 1
    except:
        return False


def press_numpad1_sendinput():
    """Press numpad 1 using SendInput API - most reliable for games"""
    try:
        # Create key down input
        key_down = INPUT()
        key_down.type = INPUT_KEYBOARD
        key_down.ki.wVk = VK_NUMPAD1
        key_down.ki.wScan = 0
        key_down.ki.dwFlags = 0
        key_down.ki.time = 0
        key_down.ki.dwExtraInfo = None
        
        # Create key up input
        key_up = INPUT()
        key_up.type = INPUT_KEYBOARD
        key_up.ki.wVk = VK_NUMPAD1
        key_up.ki.wScan = 0
        key_up.ki.dwFlags = KEYEVENTF_KEYUP
        key_up.ki.time = 0
        key_up.ki.dwExtraInfo = None
        
        # Send key down
        result1 = ctypes.windll.user32.SendInput(1, ctypes.byref(key_down), ctypes.sizeof(INPUT))
        time.sleep(0.05)  # Hold key for 50ms
        
        # Send key up
        result2 = ctypes.windll.user32.SendInput(1, ctypes.byref(key_up), ctypes.sizeof(INPUT))
        
        return result1 == 1 and result2 == 1
    except Exception as e:
        return False


def press_numpad1_fallback():
    """Fallback method using keybd_event"""
    try:
        ctypes.windll.user32.keybd_event(VK_NUMPAD1, 0, 0, 0)  # Key down
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(VK_NUMPAD1, 0, KEYEVENTF_KEYUP, 0)  # Key up
        return True
    except:
        return False


def click_numpad_1():
    """Press numpad 1 using the most reliable methods for games"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Try AutoHotkey first (most reliable for games)
    if press_numpad1_autohotkey():
        print(f"[{current_time}] ✅ Pressed numpad 1 (AutoHotkey)")
        return
    
    # Try hardware scan codes (bypasses most game input filters)
    if press_numpad1_hardware():
        print(f"[{current_time}] ✅ Pressed numpad 1 (Hardware scan codes)")
        return
    
    # Try direct input with scan codes
    if press_numpad1_direct_input():
        print(f"[{current_time}] ✅ Pressed numpad 1 (Direct input scan codes)")
        return
    
    # Try SendInput with virtual keys
    if press_numpad1_sendinput():
        print(f"[{current_time}] ✅ Pressed numpad 1 (SendInput API)")
        return
    
    # Final fallback
    if press_numpad1_fallback():
        print(f"[{current_time}] ⚠️  Pressed numpad 1 (fallback method)")
        return
    
    print(f"[{current_time}] ❌ Failed to press numpad 1 (all methods failed)")


def main():
    """Main function to run the automated key presser"""
    print("🎮 Skyrim Numpad 1 Auto-Clicker (Enhanced)")
    print("=" * 45)
    
    # Check AutoHotkey availability
    ahk_path = check_autohotkey()
    if ahk_path:
        print(f"✅ AutoHotkey found: {os.path.basename(ahk_path)}")
    else:
        print("⚠️  AutoHotkey not found")
        print("💡 Install from: https://www.autohotkey.com/")
    
    # Check admin privileges
    if is_admin():
        print("✅ Running as Administrator")
    else:
        print("❌ NOT running as Administrator!")
        print("⚠️  This may not work with Skyrim")
        print("💡 Right-click script → 'Run as administrator'")
        print()
    
    print("📋 Instructions:")
    print("1. 🎮 Start Skyrim Special Edition")
    print("2. 🎯 Make sure Skyrim window is active/focused")
    print("3. ⏰ Script will press numpad 1 every 30 seconds")
    print("4. 🛑 Press Ctrl+C to stop")
    
    print("\n🔧 Methods (in order of preference):")
    print("• AutoHotkey (best for games)")
    print("• Hardware scan codes (bypasses input filters)")
    print("• Direct input scan codes")
    print("• SendInput API")
    print("• keybd_event (fallback)")
    
    print("\n💡 For best results:")
    print("• Use Windowed Fullscreen mode in Skyrim")
    print("• Run as Administrator")
    print("• Install AutoHotkey if not present")
    
    print("\n" + "-" * 45)
    
    print("🚀 Starting automated numpad 1 pressing...")
    
    try:
        while True:
            click_numpad_1()
            
            # Wait 30 seconds with progress indication
            for i in range(30, 0, -1):
                print(f"\r⏰ Next press in {i:2d} seconds...", end="", flush=True)
                time.sleep(1)
            print()  # New line after countdown
            
    except KeyboardInterrupt:
        print("\n\n🛑 Script interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()