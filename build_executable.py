#!/usr/bin/env python3
"""
Build script for BLAMITE Organizer executable
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and return True if successful"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("=" * 50)
    print("BLAMITE Organizer - Executable Builder")
    print("=" * 50)
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    for folder in ["dist", "build"]:
        if Path(folder).exists():
            shutil.rmtree(folder)
            print(f"✓ Removed {folder} folder")
    
    # Check if required files exist
    required_files = ["main.py", "BLAMITE_TITLE.txt", "VERSION"]
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure all required files are present before building.")
        return False
    
    # Install required packages
    packages = ["pyinstaller", "watchdog", "pywin32", "requests"]
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"Failed to install {package}. Please install manually.")
            return False
    
    # Build the executable
    build_command = [
        "pyinstaller",
        "--onefile",           # Single executable file
        "--console",           # Keep console window
        "--icon=BLAMITE_Logo.ico",  # Use our custom icon
        "--name=BLAMITE_Organizer", # Executable name
        "--add-data=BLAMITE_TITLE.txt;.",  # Include title file
        "--add-data=VERSION;.",     # Include version file
        "main.py"              # Source file
    ]
    
    if not run_command(" ".join(build_command), "Building executable"):
        print("Build failed! Check the output above for errors.")
        return False
    
    # Check if executable was created
    exe_path = Path("dist/BLAMITE_Organizer.exe")
    if exe_path.exists():
        print("\n" + "=" * 50)
        print("✓ BUILD SUCCESSFUL!")
        print("=" * 50)
        print(f"✓ Executable created: {exe_path.absolute()}")
        print(f"✓ File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        print("\nYou can now:")
        print("1. Run the executable directly from the dist folder")
        print("2. Move it to any location on your computer")
        print("3. Create a desktop shortcut")
        print("4. The executable includes all dependencies and the custom icon")
        
        # Offer to run the executable
        response = input("\nWould you like to test the executable now? (y/n): ").lower().strip()
        if response == 'y':
            print("\nStarting BLAMITE Organizer...")
            try:
                subprocess.Popen([str(exe_path)], creationflags=subprocess.CREATE_NEW_CONSOLE)
                print("✓ Executable started successfully!")
            except Exception as e:
                print(f"Error starting executable: {e}")
    else:
        print("\n✗ BUILD FAILED!")
        print("The executable was not created. Check the PyInstaller output above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    
    input("\nPress Enter to exit...")
