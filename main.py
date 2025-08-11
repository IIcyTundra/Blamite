import os
import shutil
import sys
import time
import json
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    import requests
except ImportError:
    requests = None

# Define paths
DESKTOP = Path.home() / "Desktop"
ORGANIZER = DESKTOP / "BLAMITE_Organizer"
SUBFOLDERS = {
    "pdf": ORGANIZER / "PDFs",
    "doc": ORGANIZER / "Word_Documents",
    "docx": ORGANIZER / "Word_Documents",
    "xls": ORGANIZER / "Excel_Files",
    "xlsx": ORGANIZER / "Excel_Files",
    "mp3": ORGANIZER / "Audio_Files",
    "mp4": ORGANIZER / "Video_Files",
    "mov": ORGANIZER / "Video_Files",
    "gif": ORGANIZER / "Images",
    "png": ORGANIZER / "Images",
    "jpg": ORGANIZER / "Images",
    "jpeg": ORGANIZER / "Images",
    "txt": ORGANIZER / "Text_Files"
}
DOWNLOADS = Path.home() / "Downloads"

# Settings file for user preferences
SETTINGS_FILE = Path(__file__).parent / "blamite_settings.txt"

def get_current_version():
    """Get current version from version file or default"""
    try:
        if getattr(sys, 'frozen', False):
            # Running as executable
            version_file = Path(sys.executable).parent / "VERSION"
        else:
            # Running as script
            version_file = Path(__file__).parent / "VERSION"
        
        if version_file.exists():
            return version_file.read_text().strip()
    except:
        pass
    return "1.0.0"

def version_compare(v1, v2):
    """Compare version strings (returns 1 if v1 > v2, -1 if v1 < v2, 0 if equal)"""
    try:
        v1_parts = [int(x) for x in v1.split('.')]
        v2_parts = [int(x) for x in v2.split('.')]
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0
            
            if v1_part > v2_part:
                return 1
            elif v1_part < v2_part:
                return -1
        
        return 0
    except:
        return 0

def check_for_updates():
    """Check GitHub releases for newer version"""
    if not requests:
        return {'update_available': False, 'error': 'Requests module not available'}
    
    try:
        current_version = get_current_version()
        # Update with your actual GitHub username and repo name
        api_url = "https://api.github.com/repos/IIcyTundra/Blamite/releases/latest"
        
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release['tag_name'].lstrip('v')
            
            if version_compare(latest_version, current_version) > 0:
                # Find the executable asset
                download_url = None
                for asset in latest_release['assets']:
                    if asset['name'].endswith('.exe'):
                        download_url = asset['browser_download_url']
                        break
                
                if download_url:
                    return {
                        'update_available': True,
                        'latest_version': latest_version,
                        'current_version': current_version,
                        'download_url': download_url,
                        'changelog': latest_release.get('body', 'No changelog available'),
                        'release_name': latest_release.get('name', f'Version {latest_version}')
                    }
        
        return {'update_available': False, 'current_version': current_version}
    
    except requests.exceptions.RequestException:
        return {'update_available': False, 'error': 'Connection failed'}
    except Exception as e:
        return {'update_available': False, 'error': str(e)}

def show_update_prompt(update_info):
    """Show update notification to user"""
    print("\n" + "="*60)
    print("🔔 UPDATE AVAILABLE!")
    print("="*60)
    print(f"📦 {update_info.get('release_name', 'New Version')}")
    print(f"📊 Current version: v{update_info['current_version']}")
    print(f"🆕 Latest version:  v{update_info['latest_version']}")
    print()
    
    changelog = update_info.get('changelog', '').strip()
    if changelog and changelog != 'No changelog available':
        print("📋 What's new:")
        print("-"*40)
        # Limit changelog display to avoid overwhelming user
        lines = changelog.split('\n')[:10]
        for line in lines:
            print(f"  {line}")
        if len(changelog.split('\n')) > 10:
            print("  ... (see full changelog on GitHub)")
        print()
    
    while True:
        choice = input("Would you like to update now? (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def download_and_install_update(download_url, latest_version):
    """Download and install the update"""
    if not requests:
        print("❌ Cannot download updates - requests module not available")
        return False
    
    try:
        print(f"\n🔄 Downloading BLAMITE Organizer v{latest_version}...")
        print("This may take a moment depending on your internet connection...")
        
        # Download the new executable
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.exe') as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r📥 Progress: {percent:.1f}% ({downloaded//1024}KB/{total_size//1024}KB)", end="")
            temp_path = temp_file.name
        
        print("\n✅ Download complete!")
        
        # Get current executable path
        if getattr(sys, 'frozen', False):
            current_exe = Path(sys.executable)
        else:
            current_exe = Path(__file__).parent / "dist" / "BLAMITE_Organizer.exe"
        
        # Create backup of current version
        backup_path = current_exe.parent / f"BLAMITE_Organizer_backup_{get_current_version()}.exe"
        
        # Create update script
        update_script = f"""@echo off
title BLAMITE Organizer Update
echo.
echo 🔄 Installing BLAMITE Organizer v{latest_version}...
echo.

REM Wait a moment for the main program to close
timeout /t 2 /nobreak >nul

REM Create backup
echo 📦 Creating backup...
if exist "{current_exe}" (
    copy "{current_exe}" "{backup_path}" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Backup created successfully
    ) else (
        echo ⚠️  Could not create backup, continuing anyway...
    )
)

REM Install update
echo 🔄 Installing new version...
move "{temp_path}" "{current_exe}" >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Update installed successfully!
    echo 🚀 Starting BLAMITE Organizer v{latest_version}...
    echo.
    timeout /t 2 /nobreak >nul
    start "" "{current_exe}"
) else (
    echo.
    echo ❌ Update failed! Restoring backup...
    if exist "{backup_path}" (
        copy "{backup_path}" "{current_exe}" >nul 2>&1
        echo ✅ Backup restored
    )
    echo.
    echo Press any key to start the original version...
    pause >nul
    start "" "{current_exe}"
)

REM Clean up
timeout /t 3 /nobreak >nul
del "%~f0" >nul 2>&1
"""
        
        # Write and execute update script
        script_path = current_exe.parent / "update_blamite.bat"
        with open(script_path, 'w') as f:
            f.write(update_script)
        
        print("🔄 Preparing to install update...")
        print("The program will restart automatically after the update.")
        print("Please wait...")
        
        # Start update process
        subprocess.Popen([str(script_path)], shell=True, cwd=str(current_exe.parent))
        
        # Close current instance
        time.sleep(1)
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Update installation failed: {e}")
        print("You can download the latest version manually from GitHub.")
        input("Press Enter to continue with current version...")
        return False

def manual_update_check():
    """Manual update check from settings menu"""
    print("\n🔍 Checking for updates...")
    update_info = check_for_updates()
    
    if 'error' in update_info:
        print(f"❌ Update check failed: {update_info['error']}")
    elif update_info.get('update_available', False):
        if show_update_prompt(update_info):
            download_and_install_update(update_info['download_url'], update_info['latest_version'])
    else:
        current_version = update_info.get('current_version', get_current_version())
        print(f"✅ You're running the latest version (v{current_version})")
    
    input("\nPress Enter to continue...")

def load_settings():
    """Load user settings from file"""
    default_settings = {
        'backtrack_enabled': True,
        'backtrack_days': 30,
        'backtrack_all_files': False,  # If True, ignore date filtering
        'run_on_startup': False  # If True, add to Windows startup
    }
    
    if not SETTINGS_FILE.exists():
        save_settings(default_settings)
        return default_settings
    
    try:
        settings = {}
        with open(SETTINGS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().lower()
                    
                    if value in ['true', 'false']:
                        settings[key] = value == 'true'
                    elif value.isdigit():
                        settings[key] = int(value)
                    else:
                        settings[key] = value
        
        # Ensure all required settings exist
        for key, default_value in default_settings.items():
            if key not in settings:
                settings[key] = default_value
        
        return settings
    except Exception as e:
        print(f"⚠️  Error loading settings: {e}. Using defaults.")
        return default_settings

def save_settings(settings):
    """Save user settings to file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            f.write("# BLAMITE Organizer Settings\n")
            f.write("# Edit these values to customize your experience\n\n")
            f.write("# Enable/disable backtracking on startup (true/false)\n")
            f.write(f"backtrack_enabled={str(settings['backtrack_enabled']).lower()}\n\n")
            f.write("# Number of days to look back for files (when backtrack_all_files=false)\n")
            f.write(f"backtrack_days={settings['backtrack_days']}\n\n")
            f.write("# Organize ALL files regardless of date (true/false)\n")
            f.write("# WARNING: Setting this to true will organize ALL files in Downloads!\n")
            f.write(f"backtrack_all_files={str(settings['backtrack_all_files']).lower()}\n\n")
            f.write("# Run BLAMITE Organizer on Windows startup (true/false)\n")
            f.write(f"run_on_startup={str(settings['run_on_startup']).lower()}\n")
    except Exception as e:
        print(f"⚠️  Error saving settings: {e}")

def manage_startup(enable, exe_path=None):
    """Add or remove BLAMITE Organizer from Windows startup"""
    import winreg
    
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    app_name = "BLAMITE_Organizer"
    
    try:
        # Open the registry key
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        
        if enable:
            # Determine the executable path
            if exe_path is None:
                # Try to find the executable in the same directory
                current_dir = Path(__file__).parent
                exe_path = current_dir / "BLAMITE_Organizer.exe"
                
                # If no exe found, use Python script
                if not exe_path.exists():
                    python_exe = Path(sys.executable)
                    script_path = Path(__file__)
                    exe_path = f'"{python_exe}" "{script_path}"'
                else:
                    exe_path = f'"{exe_path}"'
            
            # Add to startup
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, str(exe_path))
            winreg.CloseKey(key)
            return True, "Added to Windows startup"
            
        else:
            # Remove from startup
            try:
                winreg.DeleteValue(key, app_name)
                winreg.CloseKey(key)
                return True, "Removed from Windows startup"
            except FileNotFoundError:
                winreg.CloseKey(key)
                return True, "Already not in startup"
                
    except Exception as e:
        return False, f"Error managing startup: {e}"

def check_startup_status():
    """Check if BLAMITE Organizer is currently set to run on startup"""
    import winreg
    
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    app_name = "BLAMITE_Organizer"
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        try:
            winreg.QueryValueEx(key, app_name)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            winreg.CloseKey(key)
            return False
    except Exception:
        return False

def show_settings_menu():
    """Display and handle settings configuration"""
    settings = load_settings()
    
    while True:
        # Check current startup status
        startup_enabled = check_startup_status()
        
        print("\n" + "="*50)
        print("⚙️  BLAMITE ORGANIZER SETTINGS")
        print("="*50)
        print(f"1. Backtrack on startup: {'✅ Enabled' if settings['backtrack_enabled'] else '❌ Disabled'}")
        
        if settings['backtrack_enabled']:
            if settings['backtrack_all_files']:
                print("2. Backtrack mode: 🗂️  ALL FILES (ignores date)")
            else:
                print(f"2. Backtrack mode: 📅 Last {settings['backtrack_days']} days")
        else:
            print("2. Backtrack mode: ❌ Disabled")
        
        print(f"3. Run on Windows startup: {'✅ Enabled' if startup_enabled else '❌ Disabled'}")
        
        print("\n4. Toggle backtrack on/off")
        print("5. Change backtrack days")
        print("6. Toggle ALL files mode")
        print("7. Toggle Windows startup")
        print("8. Check for updates")
        print("9. Reset to defaults")
        print("10. Return to main program")
        print("="*50)
        
        choice = input("\nEnter your choice (1-10): ").strip()
        
        if choice == '4':
            settings['backtrack_enabled'] = not settings['backtrack_enabled']
            status = "enabled" if settings['backtrack_enabled'] else "disabled"
            print(f"✅ Backtracking {status}")
            
        elif choice == '5':
            try:
                days = int(input("Enter number of days to look back (1-365): "))
                if 1 <= days <= 365:
                    settings['backtrack_days'] = days
                    settings['backtrack_all_files'] = False  # Reset all files mode
                    print(f"✅ Backtrack period set to {days} days")
                else:
                    print("❌ Please enter a number between 1 and 365")
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif choice == '6':
            settings['backtrack_all_files'] = not settings['backtrack_all_files']
            if settings['backtrack_all_files']:
                confirm = input("⚠️  This will organize ALL files in Downloads! Continue? (y/n): ")
                if confirm.lower() != 'y':
                    settings['backtrack_all_files'] = False
                    print("❌ All files mode cancelled")
                else:
                    print("✅ All files mode enabled")
            else:
                print("✅ All files mode disabled")
                
        elif choice == '7':
            current_startup = check_startup_status()
            success, message = manage_startup(not current_startup)
            if success:
                settings['run_on_startup'] = not current_startup
                print(f"✅ {message}")
            else:
                print(f"❌ {message}")
                
        elif choice == '8':
            manual_update_check()
            
        elif choice == '9':
            confirm = input("Reset all settings to defaults? (y/n): ")
            if confirm.lower() == 'y':
                # Remove from startup if currently enabled
                if check_startup_status():
                    manage_startup(False)
                
                settings = {
                    'backtrack_enabled': True,
                    'backtrack_days': 30,
                    'backtrack_all_files': False,
                    'run_on_startup': False
                }
                print("✅ Settings reset to defaults")
                
        elif choice == '10':
            save_settings(settings)
            print("✅ Settings saved!")
            return settings
            
        else:
            print("❌ Invalid choice. Please enter 1-10")

# Create organizer folders if they don't exist
def setup_folders():
    """Create organizer folders if they don't exist and show info"""
    print("\n" + "="*50)
    print("📁 SETTING UP BLAMITE ORGANIZER FOLDERS")
    print("="*50)
    
    # Create main organizer folder
    if not ORGANIZER.exists():
        ORGANIZER.mkdir(exist_ok=True)
        print(f"✅ Created main folder: {ORGANIZER}")
    else:
        print(f"📁 Main folder exists: {ORGANIZER}")
    
    # Create subfolders
    folders_created = 0
    unique_folders = set(SUBFOLDERS.values())  # Use set to avoid duplicates
    for folder in unique_folders:
        if not folder.exists():
            folder.mkdir(exist_ok=True)
            print(f"✅ Created subfolder: {folder.name}")
            folders_created += 1
        else:
            print(f"📂 Subfolder exists: {folder.name}")
    
    if folders_created > 0:
        print(f"\n🎉 Created {folders_created} new subfolders!")
    
    print("\n📋 Supported file types:")
    print("   📄 Documents: PDF, DOC, DOCX, XLS, XLSX")
    print("   📝 Text Files: TXT")
    print("   🖼️  Images: PNG, JPG, JPEG, GIF")
    print("   🎵 Audio: MP3")
    print("   🎬 Video: MP4, MOV")
    print("="*50)

def create_desktop_shortcuts():
    """No longer needed - function disabled"""
    pass

def organize_existing_files(folder_path, settings):
    """Organize existing files based on user settings"""
    folder = Path(folder_path)
    if not folder.exists():
        print(f"⚠️  Folder {folder} does not exist, skipping backtrack...")
        return
    
    if settings['backtrack_all_files']:
        print(f"🔍 Scanning {folder.name} for ALL files (ignoring date)...")
        cutoff_date = None
    else:
        days_back = settings['backtrack_days']
        print(f"🔍 Scanning {folder.name} for files from the last {days_back} days...")
        cutoff_date = datetime.now() - timedelta(days=days_back)
    
    organized_count = 0
    
    # Get all files in the folder (not directories)
    try:
        files = [f for f in folder.iterdir() if f.is_file()]
        print(f"📂 Found {len(files)} files to check in {folder.name}")
        
        for file_path in files:
            try:
                # Skip temporary files and system files
                if (file_path.name.startswith('.') or 
                    file_path.name.endswith('.tmp') or 
                    file_path.name.endswith('.part') or
                    file_path.name.endswith('.crdownload') or
                    file_path.name.startswith('~')):
                    continue
                
                # Check file extension
                ext = file_path.suffix.lower().lstrip('.')
                if ext not in SUBFOLDERS:
                    continue
                
                # Check if file is recent enough (skip if backtrack_all_files is True)
                if cutoff_date is not None:
                    file_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_modified < cutoff_date:
                        continue
                
                # Get file type description
                file_type_desc = {
                    'pdf': 'PDF', 'doc': 'Word', 'docx': 'Word',
                    'xls': 'Excel', 'xlsx': 'Excel', 'mp3': 'Audio',
                    'mp4': 'Video', 'mov': 'Video', 'txt': 'Text',
                    'png': 'Image', 'jpg': 'Image', 'jpeg': 'Image', 'gif': 'Image'
                }.get(ext, ext.upper())
                
                print(f"📋 Found recent {file_type_desc} file: {file_path.name}")
                
                # Organize the file
                dest_folder = SUBFOLDERS[ext]
                dest_path = dest_folder / file_path.name
                
                # Handle duplicate files
                counter = 1
                original_dest = dest_path
                while dest_path.exists():
                    name_part = original_dest.stem
                    ext_part = original_dest.suffix
                    dest_path = dest_folder / f"{name_part}_{counter}{ext_part}"
                    counter += 1
                
                # Move the file
                shutil.move(str(file_path), str(dest_path))
                print(f"✅ Organized: {file_path.name} → {dest_path.parent.name}")
                organized_count += 1
                
            except Exception as e:
                print(f"❗ Error processing {file_path.name}: {e}")
                continue
        
        if organized_count > 0:
            print(f"🎉 Organized {organized_count} files from {folder.name}")
        else:
            print(f"ℹ️  No recent supported files found in {folder.name}")
            
    except Exception as e:
        print(f"❗ Error scanning {folder}: {e}")

def backtrack_and_organize(settings):
    """Organize existing files from Downloads based on user settings"""
    if not settings['backtrack_enabled']:
        print("\n" + "="*50)
        print("⏭️  BACKTRACKING DISABLED (check settings to enable)")
        print("="*50)
        return
    
    print("\n" + "="*50)
    if settings['backtrack_all_files']:
        print("🔄 BACKTRACKING: Organizing ALL files from Downloads")
    else:
        print(f"🔄 BACKTRACKING: Organizing files from Downloads (last {settings['backtrack_days']} days)")
    print("="*50)
    
    # Only check Downloads folder to avoid conflicts with Desktop organization
    folders_to_check = [DOWNLOADS]
    
    for folder in folders_to_check:
        if folder.exists():
            organize_existing_files(folder, settings)
        else:
            print(f"⚠️  {folder} does not exist, skipping...")
    
    print("="*50)
    print("✅ Backtracking complete! Now monitoring Downloads folder...")
    print("="*50 + "\n")

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        print(f"📁 File detected: {file_path.name}")
        
        # Skip temporary files and partial downloads
        if (file_path.name.startswith('.') or 
            file_path.name.endswith('.tmp') or 
            file_path.name.endswith('.part') or
            file_path.name.endswith('.crdownload')):
            print(f"⏭️  Skipping temporary file: {file_path.name}")
            return
        
        ext = file_path.suffix.lower().lstrip('.')
        if ext in SUBFOLDERS:
            # Get file type description
            file_type_desc = {
                'pdf': 'PDF Document',
                'doc': 'Word Document', 'docx': 'Word Document',
                'xls': 'Excel File', 'xlsx': 'Excel File',
                'mp3': 'Audio File', 'txt': 'Text File',
                'mp4': 'Video File', 'mov': 'Video File',
                'png': 'Image File', 'jpg': 'Image File', 'jpeg': 'Image File', 'gif': 'Image File'
            }.get(ext, f'{ext.upper()} File')
            
            print(f"📋 {file_type_desc} detected, processing...")
            dest_folder = SUBFOLDERS[ext]
            dest_path = dest_folder / file_path.name
            
            # Wait for file to finish downloading completely
            print(f"⏳ Waiting for {file_path.name} to finish downloading...")
            file_size = -1
            stable_count = 0
            
            for attempt in range(60):  # Increased attempts for larger files
                try:
                    # Check if file still exists
                    if not file_path.exists():
                        print(f"❌ File {file_path.name} no longer exists, skipping...")
                        return
                    
                    # Check if file size is stable (not growing = download complete)
                    current_size = file_path.stat().st_size
                    if current_size == file_size:
                        stable_count += 1
                        if stable_count >= 3:  # File size stable for 3 checks = download complete
                            print(f"✅ Download complete for {file_path.name} ({current_size} bytes)")
                            break
                    else:
                        file_size = current_size
                        stable_count = 0
                        print(f"📥 Still downloading {file_path.name}... ({current_size} bytes)")
                    
                    # Check if file is accessible (not locked by downloader)
                    try:
                        with open(file_path, 'rb') as f:
                            f.read(1)  # Try to read 1 byte
                    except (PermissionError, OSError):
                        print(f"🔒 File {file_path.name} is locked, waiting... (attempt {attempt + 1}/60)")
                        time.sleep(2)
                        continue
                    
                    time.sleep(1)  # Wait 1 second between checks
                    
                except Exception as e:
                    print(f"❗ Error checking {file_path.name}: {e}")
                    time.sleep(2)
                    continue
            else:
                print(f"❌ Timeout waiting for {file_path.name} to finish downloading")
                return
            
            # Now move the file (this automatically deletes from source)
            try:
                # Avoid duplicate files in destination
                counter = 1
                original_dest = dest_path
                while dest_path.exists():
                    name_part = original_dest.stem
                    ext_part = original_dest.suffix
                    dest_path = dest_folder / f"{name_part}_{counter}{ext_part}"
                    counter += 1
                
                # Verify file still exists before moving
                if not file_path.exists():
                    print(f"❌ File {file_path.name} disappeared before move")
                    return
                
                print(f"🚀 Moving {file_path.name} from Downloads to Desktop/{dest_path.parent.name}")
                shutil.move(str(file_path), str(dest_path))
                print(f"✅ Successfully moved and organized: {dest_path.name}")
                print(f"🗑️  File automatically removed from Downloads folder")
                print(f"📁 File now available on Desktop: {dest_path.relative_to(DESKTOP)}")
                
                # Verify the move was successful
                if dest_path.exists() and not file_path.exists():
                    print(f"✅ Verification passed: File is now in {dest_path}")
                else:
                    print(f"⚠️  Warning: Move verification failed")
                    
            except Exception as e:
                print(f"❗ Error moving {file_path.name}: {e}")
                
        else:
            print(f"ℹ️  File type '{ext}' not supported, ignoring {file_path.name}")

def main():
    # Load user settings
    settings = load_settings()
    
    # Check for updates on startup (optional background check)
    try:
        update_info = check_for_updates()
        if update_info.get('update_available', False):
            print("\n🔔 A new version is available!")
            print(f"Current: v{update_info['current_version']} → Latest: v{update_info['latest_version']}")
            print("💡 Go to Settings (press 'S') to update or continue normally.")
    except:
        pass  # Don't let update checks interrupt startup
    
    # Show welcome message and settings option
    print("\n" + "="*50)
    print("⚙️  Press 'S' + Enter for Settings, or just Enter to continue...")
    print("="*50)
    
    try:
        user_input = input().strip().lower()
        if user_input == 's':
            settings = show_settings_menu()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return
    
    # Start monitoring Downloads folder and organize to Desktop
    DESKTOP_FOLDER = Path.home() / "Desktop"
    main_folders = [DOWNLOADS, DESKTOP_FOLDER]
    
    # Setup folders (create any missing ones) and backtrack based on settings
    setup_folders()
    
    # Backtrack and organize existing files based on user settings
    backtrack_and_organize(settings)
    
    # Start monitoring for new files
    event_handler = FileHandler()
    observer = Observer()
    
    # Monitor Downloads folder (don't monitor Desktop to avoid conflicts)
    if DOWNLOADS.exists():
        observer.schedule(event_handler, str(DOWNLOADS), recursive=False)
        print(f"📡 Monitoring: {DOWNLOADS}")
    else:
        print(f"⚠️  Warning: {DOWNLOADS} does not exist")
    
    observer.start()
    print("🚀 BLAMITE Organizer is running...")
    print(f"📥 Watching Downloads folder, organizing to Desktop...")
    print(f"📁 Organized files location: {ORGANIZER}")
    print("Press Ctrl+C to stop...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping BLAMITE Organizer...")
        observer.stop()
    observer.join()
    print("✅ BLAMITE Organizer stopped.")

if __name__ == "__main__":
    # Set terminal title and print welcome message
    title_file = Path(__file__).parent / "BLAMITE_TITLE.txt"
    if title_file.exists():
        with open(title_file, "r", encoding="utf-8") as f:
            project_title = f.read().strip()
    else:
        project_title = "BLAMITE Organizer"

    # Set terminal title (works on Windows)
    os.system(f"title {project_title}")

    description = (
        f"{project_title}\n"
        "----------------------------------------\n"
        "This project automatically organizes your downloaded files "
        "(PDF, Word, Excel, Images, Audio, Video, Text) "
        "into categorized folders directly on your Desktop for easy access.\n"
        "Thank you for using BLAMITE Organizer!\n"
    )
    print(description)
    
    main()
