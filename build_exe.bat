@echo off
echo Building BLAMITE Organizer executable...
echo.

REM Clean previous builds
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo Installing required packages...
pip install pyinstaller watchdog pywin32

echo.
echo Building executable with PyInstaller...
pyinstaller --onefile --console --icon=BLAMITE_Logo.ico --name="BLAMITE_Organizer" main.py

echo.
if exist "dist\BLAMITE_Organizer.exe" (
    echo ✓ Build successful!
    echo ✓ Executable created: dist\BLAMITE_Organizer.exe
    echo.
    echo Features included:
    echo   - Custom BLAMITE_Logo.ico icon
    echo   - Desktop-based organization system
    echo   - Backtracks and organizes files from last 30 days
    echo   - Monitors Downloads folder
    echo   - Supports multiple file types:
    echo     * Documents: PDF, DOC, DOCX, XLS, XLSX
    echo     * Images: PNG, JPG, JPEG, GIF
    echo     * Audio: MP3
    echo     * Video: MP4, MOV
    echo   - Smart download completion detection
    echo   - Automatic file organization with duplicate handling
    echo.
    echo You can now run the executable from the dist folder.
) else (
    echo ✗ Build failed!
    echo Check the output above for errors.
)

echo.
pause
