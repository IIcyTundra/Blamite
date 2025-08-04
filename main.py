import os
import shutil
import time
from pathlib import Path
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
    "jpeg": ORGANIZER / "Images"
}
DOWNLOADS = Path.home() / "Downloads"

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
    print("   🖼️  Images: PNG, JPG, JPEG, GIF")
    print("   🎵 Audio: MP3")
    print("   🎬 Video: MP4, MOV")
    print("="*50)

def create_desktop_shortcuts():
    """No longer needed - function disabled"""
    pass

def organize_existing_files(folder_path, days_back=30):
    """Organize existing files from the last specified number of days"""
    folder = Path(folder_path)
    if not folder.exists():
        print(f"⚠️  Folder {folder} does not exist, skipping backtrack...")
        return
    
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
                
                # Check if file is recent enough
                file_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_modified < cutoff_date:
                    continue
                
                # Get file type description
                file_type_desc = {
                    'pdf': 'PDF', 'doc': 'Word', 'docx': 'Word',
                    'xls': 'Excel', 'xlsx': 'Excel', 'mp3': 'Audio',
                    'mp4': 'Video', 'mov': 'Video',
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

def backtrack_and_organize():
    """Organize existing files from Downloads from the last 30 days"""
    print("\n" + "="*50)
    print("🔄 BACKTRACKING: Organizing files from Downloads (last 30 days)")
    print("="*50)
    
    # Only check Downloads folder to avoid conflicts with Desktop organization
    folders_to_check = [DOWNLOADS]
    
    for folder in folders_to_check:
        if folder.exists():
            organize_existing_files(folder, days_back=30)
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
                'mp3': 'Audio File',
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
    # Start monitoring Downloads folder and organize to Desktop
    DESKTOP_FOLDER = Path.home() / "Desktop"
    main_folders = [DOWNLOADS, DESKTOP_FOLDER]
    
    # Setup folders (create any missing ones) and backtrack on every startup
    setup_folders()
    
    # Backtrack and organize existing files from the last 30 days
    backtrack_and_organize()
    
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
        "(PDF, Word, Excel, Images, Audio, Video) "
        "into categorized folders directly on your Desktop for easy access.\n"
        "Thank you for using BLAMITE Organizer!\n"
    )
    print(description)
    
    main()
