; Skyrim Auto-Clicker - Numpad 1 every 30 seconds
; This AutoHotkey script is specifically designed for Skyrim Special Edition
; 
; Instructions:
; 1. Install AutoHotkey from https://www.autohotkey.com/
; 2. Run this script as Administrator
; 3. Start Skyrim and make sure it's the active window
; 4. Press Ctrl+Alt+S to start/stop the auto-clicker
; 5. Press Ctrl+Alt+Q to quit the script
;
; Hotkeys:
; Ctrl+Alt+S = Start/Stop auto-clicking
; Ctrl+Alt+Q = Quit script
; F12 = Emergency stop (if something goes wrong)

#NoEnv
#SingleInstance Force
#Persistent
SetBatchLines -1
SetKeyDelay, 10, 50  ; Delay between key presses for game compatibility

; Variables
isRunning := false
intervalSeconds := 30

; Create GUI for status
Gui, Add, Text, x10 y10 w300 h20 vStatusText, Status: Stopped
Gui, Add, Text, x10 y30 w300 h40, Hotkeys:`nCtrl+Alt+S: Start/Stop`nCtrl+Alt+Q: Quit
Gui, Add, Text, x10 y80 w300 h20 vTargetText, Target: Skyrim Special Edition
Gui, Add, Text, x10 y100 w300 h20 vIntervalText, Interval: %intervalSeconds% seconds
Gui, Show, w320 h140, Skyrim Auto-Clicker
return

; Start/Stop hotkey
^!s::
    isRunning := !isRunning
    if (isRunning) {
        GuiControl,, StatusText, Status: Running - Pressing Numpad1 every %intervalSeconds%s
        SetTimer, PressNumpad1, % intervalSeconds * 1000
        TrayTip, Skyrim Auto-Clicker, Started! Pressing Numpad1 every %intervalSeconds% seconds, 3
    } else {
        GuiControl,, StatusText, Status: Stopped
        SetTimer, PressNumpad1, Off
        TrayTip, Skyrim Auto-Clicker, Stopped!, 2
    }
return

; Quit hotkey
^!q::
    ExitApp

; Emergency stop
F12::
    isRunning := false
    GuiControl,, StatusText, Status: Emergency Stop!
    SetTimer, PressNumpad1, Off
    TrayTip, Skyrim Auto-Clicker, Emergency Stop Activated!, 2
return

; Main function to press Numpad1
PressNumpad1:
    if (!isRunning)
        return
    
    ; Check if Skyrim window exists and is active
    IfWinExist, Skyrim Special Edition
    {
        IfWinActive, Skyrim Special Edition
        {
            ; Send Numpad1 with multiple methods for maximum reliability
            ; Method 1: Standard Send
            Send, {Numpad1}
            Sleep, 10
            
            ; Method 2: SendRaw (if standard fails)
            SendRaw, {Numpad1}
            Sleep, 10
            
            ; Method 3: SendInput (most reliable)
            SendInput, {Numpad1}
            
            ; Update status
            FormatTime, currentTime, , HH:mm:ss
            GuiControl,, StatusText, Status: Running - Last press at %currentTime%
        }
        else
        {
            GuiControl,, StatusText, Status: Waiting - Skyrim not active
        }
    }
    else
    {
        GuiControl,, StatusText, Status: Waiting - Skyrim not found
    }
return

; GUI Close handler
GuiClose:
    ExitApp

; Auto-detect Skyrim window variations
DetectSkyrim() {
    skyrimTitles := ["Skyrim Special Edition", "The Elder Scrolls V: Skyrim Special Edition", "SkyrimSE"]
    
    for index, title in skyrimTitles {
        IfWinExist, %title%
            return title
    }
    return ""
}

; Tray menu customization
Menu, Tray, NoStandard
Menu, Tray, Add, Start/Stop (Ctrl+Alt+S), ToggleScript
Menu, Tray, Add, Quit (Ctrl+Alt+Q), ExitScript
Menu, Tray, Default, Start/Stop (Ctrl+Alt+S)
Menu, Tray, Tip, Skyrim Auto-Clicker

ToggleScript:
    Gosub, ^!s
return

ExitScript:
    ExitApp
