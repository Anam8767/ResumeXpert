@echo off
echo Creating HireLens desktop shortcut...
echo.

powershell -Command "
$WshShell = New-Object -comObject WScript.Shell;
$Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\HireLens.lnk');
$Shortcut.TargetPath = 'powershell.exe';
$Shortcut.Arguments = '-ExecutionPolicy Bypass -File \"d:\Windsurf\Hire lens FYP\hire_lens-dev\AUTO_START.ps1\"';
$Shortcut.WorkingDirectory = 'd:\Windsurf\Hire lens FYP\hire_lens-dev';
$Shortcut.IconLocation = 'shell32.dll,13';
$Shortcut.Description = 'Start HireLens Backend and Frontend';
$Shortcut.Save();
"

echo ✅ Desktop shortcut created!
echo Look for "HireLens" on your desktop.
echo.
pause
