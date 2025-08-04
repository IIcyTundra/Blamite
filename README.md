# BLAMITE Organizer 📁

**Automatically organize your downloaded files into categorized folders on your Desktop!**

BLAMITE Organizer is a Python-based file organization tool that monitors your Downloads folder and automatically sorts files into organized subfolders on your Desktop. It supports real-time monitoring and can also organize existing files from the past 30 days.

## ✨ Features

- **🔄 Real-time File Monitoring**: Automatically detects and organizes new downloads
- **📂 Smart Organization**: Sorts files into categorized folders by type
- **🗂️ Desktop Integration**: Creates organized folders directly on your Desktop for easy access
- **⏰ Backtracking**: Organizes existing files from the last 30 days on startup
- **🔍 Duplicate Handling**: Automatically renames duplicate files to avoid conflicts
- **📥 Download Detection**: Waits for files to finish downloading before organizing
- **🚀 Executable Available**: Run as a standalone .exe file (no Python required)

## 📋 Supported File Types

| Category | File Types | Organized To |
|----------|------------|--------------|
| **Documents** | PDF, DOC, DOCX, XLS, XLSX | `Desktop/BLAMITE_Organizer/PDFs`, `Word_Documents`, `Excel_Files` |
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

## 🛠️ How It Works

1. **Startup Process**:
   - Creates organized folders on your Desktop if they don't exist
   - Scans Downloads folder for files modified in the last 30 days
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
(PDF, Word, Excel, Images, Audio, Video)
into categorized folders directly on your Desktop for easy access.

📁 SETTING UP BLAMITE ORGANIZER FOLDERS
==================================================
✅ Created main folder: C:\Users\YourName\Desktop\BLAMITE_Organizer
✅ Created subfolder: PDFs
✅ Created subfolder: Images
...

🔄 BACKTRACKING: Organizing files from Downloads (last 30 days)
==================================================
🔍 Scanning Downloads for files from the last 30 days...
📂 Found 5 files to check in Downloads
📋 Found recent PDF file: document.pdf
✅ Organized: document.pdf → PDFs
...

🚀 BLAMITE Organizer is running...
📥 Watching Downloads folder, organizing to Desktop...
Press Ctrl+C to stop...
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
```

## ⚙️ Configuration

The organizer is configured to work out-of-the-box, but you can modify the source code to:

- **Change file types**: Edit the `SUBFOLDERS` dictionary in `main.py`
- **Modify organization location**: Change the `ORGANIZER` path
- **Adjust backtrack period**: Modify `days_back=30` in the backtrack function
- **Add new file types**: Extend the file type mappings

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
