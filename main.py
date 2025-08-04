import os
import shutil
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define paths
DOCUMENTS = Path.home() / "Documents"
ORGANIZER = DOCUMENTS / "BLAMITE_Organizer"
SUBFOLDERS = {
    "pdf": ORGANIZER / "PDFs",
    "doc": ORGANIZER / "Word_Documents",
    "docx": ORGANIZER / "Word_Documents",
    "xls": ORGANIZER / "Excel_Files",
    "xlsx": ORGANIZER / "Excel_Files"
}
DOWNLOADS = Path.home() / "Downloads"

# Create organizer folders if they don't exist
def setup_folders():
    ORGANIZER.mkdir(exist_ok=True)
    for folder in SUBFOLDERS.values():
        folder.mkdir(exist_ok=True)

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        file_path = Path(event.src_path)
        ext = file_path.suffix.lower().lstrip('.')
        if ext in SUBFOLDERS:
            dest_folder = SUBFOLDERS[ext]
            dest_path = dest_folder / file_path.name
            # Wait for file to finish downloading and exist
            for attempt in range(30):  # Increased attempts for larger files
                try:
                    # Check if file still exists
                    if not file_path.exists():
                        print(f"File {file_path} no longer exists, skipping...")
                        return
                    
                    # Check if file is still being written to
                    try:
                        with open(file_path, 'rb') as f:
                            pass  # Just try to open it
                    except (PermissionError, OSError):
                        print(f"File {file_path} is still being written, waiting... (attempt {attempt + 1}/30)")
                        time.sleep(2)
                        continue
                    
                    # Avoid duplicate files
                    counter = 1
                    original_dest = dest_path
                    while dest_path.exists():
                        name_part = original_dest.stem
                        ext_part = original_dest.suffix
                        dest_path = dest_folder / f"{name_part}_{counter}{ext_part}"
                        counter += 1
                    
                    shutil.move(str(file_path), str(dest_path))
                    print(f"✓ Moved {file_path.name} to {dest_path}")
                    break
                    
                except FileNotFoundError:
                    print(f"File {file_path} was deleted before it could be moved")
                    break
                except PermissionError:
                    print(f"Permission denied for {file_path}, waiting... (attempt {attempt + 1}/30)")
                    time.sleep(2)
                except Exception as e:
                    print(f"Unexpected error moving {file_path}: {e}")
                    break
            else:
                print(f"Failed to move {file_path} after 30 attempts")

def main():
    setup_folders()
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, str(DOWNLOADS), recursive=False)
    observer.start()
    print("BLAMITE Organizer is running...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

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
        "This project automatically organizes your downloaded PDF, Word, and Excel files "
        "into categorized folders in your Documents directory.\n"
        "Thank you for using BLAMITE Organizer!\n"
    )
    print(description)
    
    # Start monitoring both Downloads and Desktop
    DESKTOP = Path.home() / "Desktop"
    main_folders = [DOWNLOADS, DESKTOP]

    def run_observers():
        setup_folders()
        event_handler = FileHandler()
        observer = Observer()
        for folder in main_folders:
            observer.schedule(event_handler, str(folder), recursive=False)
        observer.start()
        print("BLAMITE Organizer is running...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    run_observers()