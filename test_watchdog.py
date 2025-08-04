#!/usr/bin/env python3

print("Testing watchdog imports...")

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    print("✓ Watchdog imports successful!")
    
    # Test basic functionality
    observer = Observer()
    print("✓ Observer created successfully!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Other error: {e}")

print("Test completed.")
