#!/usr/bin/env python3
"""
Banner Maker Script
A tool to create banners from image collections with customizable themes and layouts.
"""

import os
import sys
import subprocess
import importlib.util


# =============================================================================
# DEPENDENCY MANAGEMENT
# =============================================================================

def install_package(package_name):
    """
    Install a package using pip.
    
    Args:
        package_name (str): Name of the package to install
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False


def show_manual_installation_guide(failed_packages):
    """
    Show detailed installation guide for failed packages.
    
    Args:
        failed_packages (list): List of packages that failed to install
    """
    print("\n" + "="*60)
    print("❌ AUTOMATIC INSTALLATION FAILED")
    print("="*60)
    print("Some packages could not be installed automatically.")
    print("Please install them manually using one of the methods below:\n")
    
    print("📋 MISSING PACKAGES:")
    for package in failed_packages:
        print(f"   • {package}")
    
    print("\n🔧 INSTALLATION METHODS:")
    print("\n1️⃣ Method 1 - Using pip (Recommended):")
    print("   Open Command Prompt/Terminal and run:")
    for package in failed_packages:
        print(f"   pip install {package}")
    
    print("\n2️⃣ Method 2 - Using pip3 (if pip doesn't work):")
    print("   Open Command Prompt/Terminal and run:")
    for package in failed_packages:
        print(f"   pip3 install {package}")
    
    print("\n3️⃣ Method 3 - Using Python directly:")
    print("   Open Command Prompt/Terminal and run:")
    for package in failed_packages:
        print(f"   python -m pip install {package}")
    
    print("\n🚨 TROUBLESHOOTING:")
    print("   • Make sure you have internet connection")
    print("   • Try running Command Prompt as Administrator (Windows)")
    print("   • On macOS/Linux, try using 'sudo' before the command")
    print("   • Update pip first: python -m pip install --upgrade pip")
    
    print("\n💡 ALTERNATIVE SOLUTIONS:")
    print("   • Install Python from python.org (includes pip)")
    print("   • Use Anaconda distribution (includes all packages)")
    print("   • Download packages manually from pypi.org")
    
    print("\n" + "="*60)
    print("After installing the packages, run this script again.")
    print("="*60)


def check_and_install_dependencies():
    """
    Check if required packages are installed and install them if missing.
    """
    required_packages = {
        'PIL': 'Pillow',
        'requests': 'requests'
    }
    
    missing_packages = []
    
    # Check each required package
    for import_name, package_name in required_packages.items():
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            missing_packages.append((import_name, package_name))
    
    # Install missing packages
    if missing_packages:
        print("Installing required packages...")
        failed_packages = []
        
        for import_name, package_name in missing_packages:
            print(f"Installing {package_name}...")
            if install_package(package_name):
                print(f"✓ {package_name} installed successfully")
            else:
                failed_packages.append(package_name)
        
        # If any packages failed to install, show manual guide
        if failed_packages:
            show_manual_installation_guide(failed_packages)
            sys.exit(1)
        
        print("All required packages installed successfully!\n")


# Check and install dependencies before importing
check_and_install_dependencies()

# Now import the packages
import glob
import math
import random
import datetime
import ctypes
from ctypes import wintypes
from PIL import Image, ImageDraw, ImageFont
import requests
import shutil


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_actual_desktop_path():
    """
    Get the actual desktop path using Windows API.
    Works with all languages and OneDrive synchronization.
    
    Returns:
        str: Path to the user's desktop directory
    """
    try:
        # Use Windows API to get desktop path
        CSIDL_DESKTOP = 0x0000
        SHGFP_TYPE_CURRENT = 0x0000
        
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOP, None, SHGFP_TYPE_CURRENT, buf)
        
        desktop_path = buf.value
        if os.path.exists(desktop_path):
            return desktop_path
    except Exception:
        pass
    
    # Fallback to environment variables
    possible_paths = [
        os.path.join(os.environ.get('USERPROFILE', ''), 'OneDrive', 'Desktop'),
        os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop'),
        os.path.dirname(os.path.abspath(__file__))  # Last resort: script directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return os.path.dirname(os.path.abspath(__file__))  # Default: script directory


def download_font(font_path):
    """
    Download the ArchivoBlack font from Google Fonts repository.
    
    Args:
        font_path (str): Path where the font should be saved
        
    Returns:
        bool: True if download successful, False otherwise
    """
    font_url = "https://github.com/google/fonts/raw/main/ofl/archivoblack/ArchivoBlack-Regular.ttf"
    try:
        print("Downloading font from official repository...")
        response = requests.get(font_url, stream=True, timeout=10)
        response.raise_for_status()
        
        with open(font_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        
        # Test if font is valid
        try:
            ImageFont.truetype(font_path, 10)
            return True
        except Exception:
            os.remove(font_path)
            return False
    except Exception as e:
        print(f"Font download failed: {str(e)}")
        return False


def check_images_in_folder(folder_path):
    """
    Check if there are supported image files in the specified folder.
    
    Args:
        folder_path (str): Path to the folder to check
        
    Returns:
        bool: True if images found, False otherwise
    """
    supported_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp']
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in supported_extensions):
                return True
    return False


def check_image_mode(image):
    """
    Ensure image is in RGBA mode for proper transparency handling.
    
    Args:
        image (PIL.Image): Input image
        
    Returns:
        PIL.Image: Image in RGBA mode
    """
    return image.convert('RGBA') if image.mode != 'RGBA' else image


def hex_to_rgb(hex_color):
    """
    Convert hex color code to RGB tuple.
    
    Args:
        hex_color (str): Hex color code (e.g., '#FF0000')
        
    Returns:
        tuple: RGB values (r, g, b)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def cmyk_to_rgb(c, m, y, k):
    """
    Convert CMYK color to RGB tuple.
    
    Args:
        c, m, y, k (float): CMYK values (0-100)
        
    Returns:
        tuple: RGB values (r, g, b)
    """
    c, m, y, k = c/100, m/100, y/100, k/100
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return (int(r), int(g), int(b))


def parse_color_input(color_input):
    """
    Parse different color input formats and return RGB tuple.
    
    Supported formats:
    - HEX: #FF0000 or FF0000
    - RGB: rgb(255, 0, 0) or 255,0,0
    - CMYK: cmyk(0, 100, 100, 0) or 0,100,100,0
    
    Args:
        color_input (str): Color input in various formats
        
    Returns:
        tuple: RGB values (r, g, b) or None if invalid
    """
    color_input = color_input.strip().lower()
    
    try:
        # HEX format
        if color_input.startswith('#') or (len(color_input) == 6 and all(c in '0123456789abcdef' for c in color_input)):
            return hex_to_rgb(color_input)
        
        # RGB format
        elif color_input.startswith('rgb(') and color_input.endswith(')'):
            # Extract values from rgb(r, g, b)
            values = color_input[4:-1].split(',')
            if len(values) == 3:
                r, g, b = [int(v.strip()) for v in values]
                if all(0 <= val <= 255 for val in [r, g, b]):
                    return (r, g, b)
        
        # RGB format without rgb() wrapper
        elif ',' in color_input and not color_input.startswith('cmyk'):
            values = color_input.split(',')
            if len(values) == 3:
                r, g, b = [int(v.strip()) for v in values]
                if all(0 <= val <= 255 for val in [r, g, b]):
                    return (r, g, b)
        
        # CMYK format
        elif color_input.startswith('cmyk(') and color_input.endswith(')'):
            # Extract values from cmyk(c, m, y, k)
            values = color_input[5:-1].split(',')
            if len(values) == 4:
                c, m, y, k = [float(v.strip()) for v in values]
                if all(0 <= val <= 100 for val in [c, m, y, k]):
                    return cmyk_to_rgb(c, m, y, k)
        
        # CMYK format without cmyk() wrapper
        elif ',' in color_input:
            values = color_input.split(',')
            if len(values) == 4:
                c, m, y, k = [float(v.strip()) for v in values]
                if all(0 <= val <= 100 for val in [c, m, y, k]):
                    return cmyk_to_rgb(c, m, y, k)
    
    except (ValueError, IndexError):
        pass
    
    return None


def validate_hex_color(hex_color):
    """
    Validate if the given string is a valid hex color code.
    
    Args:
        hex_color (str): Hex color code to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            return False
        int(hex_color, 16)
        return True
    except ValueError:
        return False


# =============================================================================
# SETUP AND INITIALIZATION
# =============================================================================

def initial_setup():
    """
    Perform initial setup for the banner maker.
    Creates necessary directories and files if they don't exist.
    
    Returns:
        str: Path to the BannerMaker directory
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    banner_maker_path = os.path.join(script_dir, 'BannerMaker')
    os.makedirs(banner_maker_path, exist_ok=True)

    # Define required files and their default content
    required_files = {
        'ArchivoBlack-Regular.ttf': None,
        'background.png': Image.new('RGBA', (2000, 2000), (0, 0, 0, 0)),
        'watermark.png': Image.new('RGBA', (2000, 2000), (0, 0, 0, 0)),
        'folder_list.txt': None
    }

    missing_files = [f for f in required_files if not os.path.exists(os.path.join(banner_maker_path, f))]

    if missing_files:
        print("\nPerforming initial setup...")

        if 'folder_list.txt' in missing_files:
            desktop_path = get_actual_desktop_path()
            print(f"Using desktop path: {desktop_path}")
            
            desktop_images_path = ""
            
            # Image folder creation and validation loop
            while True:
                folder_name = input("Enter name for the images folder to create on desktop: ").strip()
                
                # Check for empty folder name
                if not folder_name:
                    print("❌ ERROR: Folder name cannot be empty!")
                    print("Please enter a valid folder name.")
                    continue
                
                desktop_images_path = os.path.join(desktop_path, folder_name)
                
                # Create folder
                try:
                    os.makedirs(desktop_images_path, exist_ok=True)
                    print(f"\n✓ Created/Using folder: {desktop_images_path}")
                except Exception as e:
                    print(f"❌ ERROR: Could not create folder: {str(e)}")
                    continue
                
                print("Please add your images to this folder and press Enter to continue...")
                input()
                
                # Check for images in folder
                while True:
                    if check_images_in_folder(desktop_images_path):
                        print("✓ Images found in the folder. Continuing...")
                        break
                    else:
                        print("❌ No image files found in the folder!")
                        print("Please add image files (PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP) to the folder.")
                        print(f"Folder path: {desktop_images_path}")
                        input("After adding images, press Enter to continue...")
                
                break
        else:
            desktop_images_path = ""

        # Create missing files
        for file in missing_files:
            file_path = os.path.join(banner_maker_path, file)
            if file == 'ArchivoBlack-Regular.ttf':
                if not download_font(file_path):
                    print("Could not download font automatically. Using default font.")
            elif file == 'background.png':
                required_files[file].save(file_path)
            elif file == 'watermark.png':
                required_files[file].save(file_path)
            elif file == 'folder_list.txt' and desktop_images_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("# Add your image folder paths here (one per line)\n")
                    f.write(f"{desktop_images_path}\n")

    return banner_maker_path


def check_existing_folders():
    """
    Check if images exist in the folders listed in folder_list.txt
    
    Returns:
        bool: True if all folders have images, False otherwise
    """
    banner_maker_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'BannerMaker')
    folder_list_path = os.path.join(banner_maker_path, 'folder_list.txt')
    
    if not os.path.exists(folder_list_path):
        return True  # If no folder list exists, skip check
    
    try:
        with open(folder_list_path, 'r', encoding='utf-8') as f:
            folder_list = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not folder_list:
            return True  # If no folders listed, skip check
        
        for folder_path in folder_list:
            if not os.path.exists(folder_path):
                print(f"❌ Folder not found: {folder_path}")
                return False
            
            if not check_images_in_folder(folder_path):
                print(f"❌ No image files found in the folder: {folder_path}")
                print("Please add image files (PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP) to the folder.")
                input("After adding images, press Enter to continue...")
                return check_existing_folders()  # Recheck after user adds images
        
        return True
    except Exception as e:
        print(f"Error checking folders: {str(e)}")
        return True


# =============================================================================
# BANNER CREATION FUNCTIONS
# =============================================================================

def add_info_band(image, file_count, theme_color):
    """
    Add an information band to the banner with file format and count info.
    
    Args:
        image (PIL.Image): Input image
        file_count (int): Number of PNG files
        theme_color (tuple): RGB color for the band
        
    Returns:
        PIL.Image: Image with info band added
    """
    width, height = image.size
    band_height = int(height * 0.20)
    total_files = file_count * 3

    # Create band background
    band = Image.new('RGBA', (width, band_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(band)

    # Draw rounded rectangle for band
    radius = 15
    draw.rounded_rectangle((5, 5, width, band_height), radius=radius, fill=theme_color)

    # Set up font
    try:
        font = ImageFont.truetype(font_path, int(band_height * 0.17))
    except Exception:
        font = ImageFont.load_default()

    # Left side text (file formats)
    left_x = width * 0.04
    draw.text((left_x, band_height * left_text_positions[0]), "PNG", fill=(255, 255, 255), font=font, anchor="lm")
    draw.text((left_x, band_height * left_text_positions[1]), "SVG", fill=(255, 255, 255), font=font, anchor="lm")
    draw.text((left_x, band_height * left_text_positions[2]), "PDF", fill=(255, 255, 255), font=font, anchor="lm")

    # Right side text (file count and info)
    right_texts = [f"{total_files}+ FILES", "INSTANT", "DOWNLOAD"]
    text_widths = [draw.textlength(text, font=font) for text in right_texts]
    max_text_width = max(text_widths)
    right_x_start = width * 0.97 - max_text_width

    for i, (text, txt_width) in enumerate(zip(right_texts, text_widths)):
        x_pos = right_x_start + (max_text_width - txt_width) / 2
        draw.text((x_pos, band_height * right_text_positions[i]), text, fill=(255, 255, 255), font=font, anchor="lm")

    # Composite the band onto the image
    position = (height - band_height) // 2
    final_image = Image.new('RGBA', (width, height))
    final_image.paste(image.crop((0, 0, width, position)), (0, 0))
    final_image.paste(band, (0, position), band)
    final_image.paste(image.crop((0, position, width, height)), (0, position + band_height))

    return final_image


def merge_images(input_paths, image_size, background, watermark, output_folder, theme_color=None, include_band=True):
    """
    Merge multiple images into a single banner with grid layout.
    
    Args:
        input_paths (list): List of image file paths
        image_size (int): Size of the output banner (square)
        background (PIL.Image): Background image
        watermark (PIL.Image): Watermark image
        output_folder (str): Output directory path
        theme_color (tuple): RGB color for info band
        include_band (bool): Whether to include info band
    """
    if not input_paths:
        print("No images found in the specified folders")
        return

    png_count = sum(1 for f in input_paths if f.lower().endswith('.png'))
    total_images = len(input_paths)
    
    # Calculate grid dimensions based on image count
    if total_images <= 4:
        columns = 2
    elif total_images <= 9:
        columns = 3
    elif total_images <= 16:
        columns = 4
    else:
        columns = math.ceil(math.sqrt(total_images))

    rows = math.ceil(total_images / columns)

    # Calculate individual image dimensions
    usable_size = image_size - 2 * border_spacing
    image_width = (usable_size - (columns - 1) * image_spacing) // columns
    image_height = (usable_size - (rows - 1) * image_spacing) // rows

    # Adjust height if info band is included
    if include_band:
        band_area = int(image_size * 0.20)
        content_height = image_size - band_area
        image_height = min(image_height, (content_height - 2 * border_spacing - (rows - 1) * image_spacing) // rows)

    # Create final image canvas
    final_image = Image.new('RGBA', (image_size, image_size))
    placed_images = []

    # Load and process images
    for path in input_paths:
        try:
            img = Image.open(path)
            img = check_image_mode(img)
            img.thumbnail((image_width, image_height), Image.LANCZOS)
            placed_images.append(img)
        except Exception as e:
            print(f"Failed to load image: {path} - {str(e)}")
            continue

    # Fill remaining grid spaces with random duplicates
    for _ in range(rows * columns - len(placed_images)):
        placed_images.append(random.choice(placed_images).copy())

    # Place images in grid
    for idx, img in enumerate(placed_images):
        col = idx % columns
        row = idx // columns

        x = border_spacing + col * (image_width + image_spacing)
        y = border_spacing + row * (image_height + image_spacing)

        # Center image in its grid cell
        offset_x = (image_width - img.width) // 2
        offset_y = (image_height - img.height) // 2

        final_image.paste(img, (x + offset_x, y + offset_y), img)

    # Apply background
    final_image = Image.alpha_composite(background.resize(final_image.size), final_image)

    # Add info band if requested
    if include_band and theme_color:
        final_image = add_info_band(final_image, png_count, theme_color)

    # Apply watermark
    final_image = Image.alpha_composite(final_image, watermark.resize(final_image.size))

    # Save final image
    os.makedirs(output_folder, exist_ok=True)
    final_image.save(os.path.join(output_folder, "final_output.png"), 'PNG')


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Configuration constants
    Image.MAX_IMAGE_PIXELS = None
    border_spacing = 10
    image_spacing = 10
    left_text_positions = [0.20, 0.50, 0.80]
    right_text_positions = [0.25, 0.50, 0.75]

    # Initialize setup
    banner_maker_path = initial_setup()
    
    # Check if existing folders have images
    if not check_existing_folders():
        print("Setup incomplete. Please ensure all folders contain images.")
        sys.exit(1)  # return yerine sys.exit() kullandım

    # Define file paths
    font_path = os.path.join(banner_maker_path, 'ArchivoBlack-Regular.ttf')
    image_folder = os.path.join(banner_maker_path, 'folder_list.txt')
    background_path = os.path.join(banner_maker_path, 'background.png')
    watermark_path = os.path.join(banner_maker_path, 'watermark.png')

    # User configuration
    include_band = input("\nInclude info band in the banner? (y/n): ").strip().lower() == 'y'
    include_watermark = input("\nInclude watermark in the banner? (y/n): ").strip().lower() == 'y'

    # Configure watermark
    if include_watermark:
        transparency_percent = int(input("Enter watermark transparency (0–100): ").strip())
        transparency_percent = max(0, min(100, transparency_percent))
        watermark = check_image_mode(Image.open(watermark_path))
        alpha = int(255 * (transparency_percent / 100))
        r, g, b, a = watermark.split()
        a = a.point(lambda p: int(p * (transparency_percent / 100)))
        watermark = Image.merge('RGBA', (r, g, b, a))
    else:
        watermark = Image.new('RGBA', (2000, 2000), (0, 0, 0, 0))

    # Output configuration
    current_time = datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")
    custom_folder_name = input("Enter output folder name: ").strip().capitalize()

    # Theme color configuration
    theme_color = None
    if include_band:
        print("\nSupported color formats:")
        print("• HEX: #FF0000 or FF0000")
        print("• RGB: rgb(255, 0, 0) or 255,0,0")
        print("• CMYK: cmyk(0, 100, 100, 0) or 0,100,100,0")
        
        while True:
            color_input = input("\nEnter color code for the band: ").strip()
            theme_color = parse_color_input(color_input)
            
            if theme_color:
                print(f"✓ Color accepted: RGB{theme_color}")
                break
            else:
                print("❌ Invalid color format! Please use one of the supported formats above.")
                print("Examples:")
                print("  HEX: #FF0000")
                print("  RGB: rgb(255, 0, 0)")
                print("  CMYK: cmyk(0, 100, 100, 0)")

    # Set up output folder
    output_folder = os.path.join(banner_maker_path, 'Banners', f'{custom_folder_name}_{current_time}')

    # Load background
    background = check_image_mode(Image.open(background_path))

    # Process image folders
    with open(image_folder, 'r', encoding='utf-8') as f:
        folder_list = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    for folder in folder_list:
        print(f"\nProcessing images from: {folder}")
        image_paths = glob.glob(os.path.join(folder, '**', '*.png'), recursive=True)
        merge_images(
            image_paths,
            image_size=2000,
            background=background,
            watermark=watermark,
            output_folder=output_folder,
            theme_color=theme_color,
            include_band=include_band
        )

    print("\nProcess completed successfully!")
    print(f"Banners saved to: {output_folder}")