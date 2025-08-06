
=============================================================================
```
________  ___       ________  _____ ______   ___  _________  _______      
|\   __  \|\  \     |\   __  \|\   _ \  _   \|\  \|\___   ___\\  ___ \     
\ \  \|\ /\ \  \    \ \  \|\  \ \  \\\__\ \  \ \  \|___ \  \_\ \   __/|    
 \ \   __  \ \  \    \ \   __  \ \  \\|__| \  \ \  \   \ \  \ \ \  \_|/__  
  \ \  \|\  \ \  \____\ \  \ \  \ \  \    \ \  \ \  \   \ \  \ \ \  \_|\ \ 
   \ \_______\ \_______\ \__\ \__\ \__\    \ \__\ \__\   \ \__\ \ \_______\
    \|_______|\|_______|\|__|\|__|\|__|     \|__|\|__|    \|__|  \|_______|
```
==============================================================================

# BLAMITE Organizer 📁

**Automatically organize your downloaded files into categorized folders on your Desktop!**

BLAMITE Organizer is a Python-based file organization tool that monitors your Downloads folder and automatically sorts files into organized subfolders on your Desktop. It supports real-time monitoring, customizable backtracking settings, and can organize existing files based on your preferences.

## ✨ Features

- **🔄 Real-time File Monitoring**: Automatically detects and organizes new downloads
- **📂 Smart Organization**: Sorts files into categorized folders by type
- **🗂️ Desktop Integration**: Creates organized folders directly on your Desktop for easy access
- **⚙️ Customizable Settings**: Configure backtracking preferences and file organization behavior
- **⏰ Flexible Backtracking**: Choose from 30-day backtracking, custom date ranges, or organize ALL files
- **🔍 Duplicate Handling**: Automatically renames duplicate files to avoid conflicts
- **📥 Download Detection**: Waits for files to finish downloading before organizing
- **🚀 Executable Available**: Run as a standalone .exe file (no Python required)
- **📝 Text File Support**: Now includes support for organizing .txt files

## 📋 Supported File Types

| Category | File Types | Organized To |
|----------|------------|--------------|
| **Documents** | PDF, DOC, DOCX, XLS, XLSX | `Desktop/BLAMITE_Organizer/PDFs`, `Word_Documents`, `Excel_Files` |
| **Text Files** | TXT | `Desktop/BLAMITE_Organizer/Text_Files` |
| **Images** | PNG, JPG, JPEG, GIF | `Desktop/BLAMITE_Organizer/Images` |
| **Audio** | MP3 | `Desktop/BLAMITE_Organizer/Audio_Files` |
| **Video** | MP4, MOV | `Desktop/BLAMITE_Organizer/Video_Files` |

## 🚀 How to Use

### Option 1: Run the Executable (Recommended)

1. **Download**: Get the `BLAMITE_Organizer.exe` file from the `dist` folder
2. **Run**: Double-click the executable to start
3. **That's it!** The organizer will:
   - Create necessary folders on your Desktop
   - Organize any recent files from your Downloads folder
   - Start monitoring for new downloads

```
📁 Your Desktop will have a new folder structure:
Desktop/
└── BLAMITE_Organizer/
    ├── PDFs/
    ├── Word_Documents/
    ├── Excel_Files/
    ├── Text_Files/
    ├── Images/
    ├── Audio_Files/
    └── Video_Files/
```

### Option 2: Run with Python

**Prerequisites:**
- Python 3.7 or higher
- Required packages (install with pip)

**Installation:**
```bash
# Clone or download this repository
cd Blamite

# Install required packages
pip install watchdog

# Run the organizer
python main.py
```

## ⚙️ Settings & Configuration

BLAMITE Organizer now includes a built-in settings menu to customize your file organization experience!

### Accessing Settings

When you start the program, you'll see:
```
==================================================
⚙️  Press 'S' + Enter for Settings, or just Enter to continue...
==================================================
```

Press **'S'** and **Enter** to access the settings menu.

### Settings Options

| Setting | Description | Options |
|---------|-------------|---------|
| **Backtrack on Startup** | Enable/disable organizing existing files when starting | ✅ Enabled / ❌ Disabled |
| **Backtrack Mode** | Choose how to handle existing files | 📅 Last X days / 🗂️ ALL FILES |
| **Backtrack Days** | Number of days to look back (when not using ALL FILES mode) | 1-365 days (default: 30) |

### Settings Menu Navigation

```
⚙️  BLAMITE ORGANIZER SETTINGS
==================================================
1. Backtrack on startup: ✅ Enabled
2. Backtrack mode: 📅 Last 30 days

3. Toggle backtrack on/off
4. Change backtrack days
5. Toggle ALL files mode
6. Reset to defaults
7. Return to main program
==================================================
```

### Important Notes

- **ALL FILES Mode**: ⚠️ **Use with caution!** This will organize EVERY file in your Downloads folder, regardless of when it was created
- **Settings File**: Your preferences are saved in `blamite_settings.txt` in the same folder as the program
- **Manual Editing**: You can also edit the settings file directly with any text editor

### Example Settings File
```ini
# BLAMITE Organizer Settings
# Edit these values to customize your experience

# Enable/disable backtracking on startup (true/false)
backtrack_enabled=true

# Number of days to look back for files (when backtrack_all_files=false)
backtrack_days=30

# Organize ALL files regardless of date (true/false)
# WARNING: Setting this to true will organize ALL files in Downloads!
backtrack_all_files=false
```

## 🛠️ How It Works

1. **Startup Process**:
   - Shows settings menu option (press 'S' for settings)
   - Loads user preferences from settings file
   - Creates organized folders on your Desktop if they don't exist
   - Scans Downloads folder based on your backtrack settings:
     - **Disabled**: Skip backtracking entirely
     - **Last X Days**: Organizes files modified in the specified time period
     - **ALL FILES**: Organizes every supported file regardless of date
   - Organizes any found files into appropriate categories

2. **Real-time Monitoring**:
   - Watches your Downloads folder for new files
   - Waits for downloads to complete (detects file size stability)
   - Automatically moves and organizes completed downloads
   - Removes files from Downloads folder after successful organization

3. **Smart Features**:
   - **Duplicate Handling**: Adds number suffix to avoid overwriting existing files
   - **Download Detection**: Monitors file size to ensure downloads are complete
   - **File Verification**: Confirms successful file moves
   - **Error Handling**: Gracefully handles locked or inaccessible files

## 🎯 Usage Examples

### Starting the Organizer
```
BLAMITE Organizer
----------------------------------------
This project automatically organizes your downloaded files
(PDF, Word, Excel, Images, Audio, Video, Text)
into categorized folders directly on your Desktop for easy access.

==================================================
⚙️  Press 'S' + Enter for Settings, or just Enter to continue...
==================================================

📁 SETTING UP BLAMITE ORGANIZER FOLDERS
==================================================
✅ Created main folder: C:\Users\YourName\Desktop\BLAMITE_Organizer
✅ Created subfolder: PDFs
✅ Created subfolder: Text_Files
✅ Created subfolder: Images
...

� Supported file types:
   📄 Documents: PDF, DOC, DOCX, XLS, XLSX
   📝 Text Files: TXT
   🖼️  Images: PNG, JPG, JPEG, GIF
   🎵 Audio: MP3
   🎬 Video: MP4, MOV

�🔄 BACKTRACKING: Organizing files from Downloads (last 30 days)
==================================================
🔍 Scanning Downloads for files from the last 30 days...
📂 Found 8 files to check in Downloads
📋 Found recent PDF file: document.pdf
📋 Found recent Text file: notes.txt
✅ Organized: document.pdf → PDFs
✅ Organized: notes.txt → Text_Files
...

🚀 BLAMITE Organizer is running...
📥 Watching Downloads folder, organizing to Desktop...
Press Ctrl+C to stop...
```

### Settings Menu Example
```
⚙️  BLAMITE ORGANIZER SETTINGS
==================================================
1. Backtrack on startup: ✅ Enabled
2. Backtrack mode: 📅 Last 30 days

3. Toggle backtrack on/off
4. Change backtrack days
5. Toggle ALL files mode
6. Reset to defaults
7. Return to main program
==================================================

Enter your choice (1-7): 4
Enter number of days to look back (1-365): 7
✅ Backtrack period set to 7 days
```

### Real-time Organization
```
📁 File detected: presentation.pdf
📋 PDF Document detected, processing...
⏳ Waiting for presentation.pdf to finish downloading...
✅ Download complete for presentation.pdf (2,456,789 bytes)
🚀 Moving presentation.pdf from Downloads to Desktop/PDFs
✅ Successfully moved and organized: presentation.pdf
🗑️  File automatically removed from Downloads folder
📁 File now available on Desktop: BLAMITE_Organizer\PDFs\presentation.pdf

📁 File detected: meeting_notes.txt
📋 Text File detected, processing...
✅ Download complete for meeting_notes.txt (1,234 bytes)
🚀 Moving meeting_notes.txt from Downloads to Desktop/Text_Files
✅ Successfully moved and organized: meeting_notes.txt
📁 File now available on Desktop: BLAMITE_Organizer\Text_Files\meeting_notes.txt
```

## ⚙️ Settings & Configuration

BLAMITE Organizer now includes a built-in settings menu to customize your file organization experience!

### Accessing Settings

When you start the program, you'll see:
```
==================================================
⚙️  Press 'S' + Enter for Settings, or just Enter to continue...
==================================================
```

Press **'S'** and **Enter** to access the settings menu.

### Settings Options

| Setting | Description | Options |
|---------|-------------|---------|
| **Backtrack on Startup** | Enable/disable organizing existing files when starting | ✅ Enabled / ❌ Disabled |
| **Backtrack Mode** | Choose how to handle existing files | 📅 Last X days / 🗂️ ALL FILES |
| **Backtrack Days** | Number of days to look back (when not using ALL FILES mode) | 1-365 days (default: 30) |

### Settings Menu Navigation

```
⚙️  BLAMITE ORGANIZER SETTINGS
==================================================
1. Backtrack on startup: ✅ Enabled
2. Backtrack mode: 📅 Last 30 days

3. Toggle backtrack on/off
4. Change backtrack days
5. Toggle ALL files mode
6. Reset to defaults
7. Return to main program
==================================================
```

### Important Notes

- **ALL FILES Mode**: ⚠️ **Use with caution!** This will organize EVERY file in your Downloads folder, regardless of when it was created
- **Settings File**: Your preferences are saved in `blamite_settings.txt` in the same folder as the program
- **Manual Editing**: You can also edit the settings file directly with any text editor

### Example Settings File
```ini
# BLAMITE Organizer Settings
# Edit these values to customize your experience

# Enable/disable backtracking on startup (true/false)
backtrack_enabled=true

# Number of days to look back for files (when backtrack_all_files=false)
backtrack_days=30

# Organize ALL files regardless of date (true/false)
# WARNING: Setting this to true will organize ALL files in Downloads!
backtrack_all_files=false
```

## ⚙️ Configuration

The organizer is configured to work out-of-the-box, but you can customize it using:

### Built-in Settings Menu
- **Access**: Press 'S' when starting the program
- **Backtrack Settings**: Enable/disable, change time period, or organize all files
- **Persistent Storage**: Settings are automatically saved to `blamite_settings.txt`

### Manual Configuration (Advanced)
You can also modify the source code to:

- **Change file types**: Edit the `SUBFOLDERS` dictionary in `main.py`
- **Modify organization location**: Change the `ORGANIZER` path
- **Add new file types**: Extend the file type mappings
- **Customize folder names**: Update the folder paths in `SUBFOLDERS`

### Settings File Location
The settings file `blamite_settings.txt` is created in the same directory as the program and contains:
- Backtrack enable/disable setting
- Number of days to look back
- ALL files mode toggle

## 🔧 Building from Source

If you want to create your own executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable with custom icon
python -m PyInstaller --onefile --console --icon=BLAMITE_Logo.ico --name=BLAMITE_Organizer main.py

# Executable will be created in dist/BLAMITE_Organizer.exe
```

## 🛑 Stopping the Organizer

- **Executable**: Close the console window or press `Ctrl+C`
- **Python**: Press `Ctrl+C` in the terminal

## ⚠️ Important Notes

- **Backup**: Always backup important files before running any file organization tool
- **Downloads Folder**: Files will be **moved** (not copied) from Downloads to organized folders
- **Permissions**: Ensure the application has read/write access to Downloads and Desktop folders
- **Antivirus**: Some antivirus software may flag the executable - this is common with PyInstaller builds

## 🐛 Troubleshooting

### Common Issues:

**"Permission denied" errors:**
- Ensure no files are open in other applications
- Run as administrator if necessary

**Files not being organized:**
- Check if file types are supported (see table above)
- Verify Downloads folder exists and is accessible
- Ensure files are not still downloading (wait for completion)

**Executable won't start:**
- Check antivirus software isn't blocking the file
- Ensure all required system libraries are installed
- Try running the Python script directly

## 📜 License

This project is open source. Feel free to modify and distribute as needed.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add support for new file types
- Improve error handling
- Enhance the user interface
- Fix bugs or optimize performance

---

**Thank you for using BLAMITE Organizer!** 🎉

*Keep your Downloads folder clean and your files organized!*
