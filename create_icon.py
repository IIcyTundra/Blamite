#!/usr/bin/env python3
"""
Simple script to create a basic icon for BLAMITE Organizer
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a 256x256 image with a blue background
    size = 256
    img = Image.new('RGBA', (size, size), (30, 144, 255, 255))  # Blue background
    draw = ImageDraw.Draw(img)
    
    # Draw a folder-like shape
    folder_color = (255, 215, 0, 255)  # Gold color
    
    # Main folder rectangle
    folder_width = 180
    folder_height = 140
    folder_x = (size - folder_width) // 2
    folder_y = (size - folder_height) // 2 + 20
    
    # Draw folder tab
    tab_width = 60
    tab_height = 20
    draw.rectangle([folder_x, folder_y - tab_height, folder_x + tab_width, folder_y], fill=folder_color)
    
    # Draw main folder body
    draw.rectangle([folder_x, folder_y, folder_x + folder_width, folder_y + folder_height], fill=folder_color)
    
    # Add "B" for BLAMITE in the center
    try:
        # Try to use a system font
        font_size = 80
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw the "B" letter
    text = "B"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2
    
    draw.text((text_x, text_y), text, fill=(0, 0, 0, 255), font=font)
    
    # Save as ICO file
    icon_path = "blamite_icon.ico"
    # Convert to different sizes for ICO format
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    images = []
    
    for size_tuple in sizes:
        resized = img.resize(size_tuple, Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Save the ICO file
    images[0].save(icon_path, format='ICO', sizes=[img.size for img in images])
    print(f"Icon created: {icon_path}")
    
    return icon_path

if __name__ == "__main__":
    try:
        create_icon()
    except ImportError:
        print("PIL (Pillow) not found. Installing...")
        os.system("pip install Pillow")
        create_icon()
