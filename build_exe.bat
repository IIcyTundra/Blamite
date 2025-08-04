@echo off
echo Building BLAMITE Organizer executable...
echo.

REM Clean previous builds
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo Installing required packages...
pip install pyinstaller watchdog

echo.
echo Building executable with PyInstaller...
pyinstaller --onefile --console --icon=blamite_icon.ico --name="BLAMITE_Organizer" main.py

echo.
if exist "dist\BLAMITE_Organizer.exe" (
    echo ✓ Build successful!
    echo ✓ Executable created: dist\BLAMITE_Organizer.exe
    echo.
    echo You can now run the executable from the dist folder.
    echo The executable includes all dependencies and the icon.
) else (
    echo ✗ Build failed!
    echo Check the output above for errors.
)

echo.
pause
