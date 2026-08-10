#!/usr/bin/env python3
"""
Business Logic: Extract text from images (JPG, PNG, etc.) using OCR
Requires: pytesseract and Pillow (auto-installs if missing)
"""

import sys
from pathlib import Path
import subprocess


def ensure_dependencies_installed():
    """Install required OCR dependencies"""
    dependencies = {
        'PIL': 'Pillow',  # PIL module name -> package name
        'pytesseract': 'pytesseract'
    }
    
    installed = []
    failed = []
    
    for module, package in dependencies.items():
        try:
            __import__(module)
            installed.append(module)
        except ImportError:
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                     stdout=subprocess.DEVNULL)
                print(f"✓ {package} installed")
                installed.append(module)
            except Exception as e:
                print(f"✗ Failed to install {package}: {e}")
                failed.append(package)
    
    if failed:
        return False, failed
    return True, installed


def check_tesseract_binary():
    """Check if tesseract OCR engine is installed on system"""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✓ Found {version}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    return False


def extract_text_from_image(image_path):
    """
    Extract text from image using OCR.
    
    Business Logic:
    1. Load image using PIL
    2. Apply OCR using pytesseract
    3. Extract and clean text
    4. Return formatted text
    
    Args:
        image_path: Path to image file
        
    Returns:
        Extracted text content
    """
    
    try:
        from PIL import Image
        import pytesseract
        
        # Load image
        print(f"Loading image: {image_path}")
        image = Image.open(image_path)
        
        # Get image info
        width, height = image.size
        mode = image.mode
        print(f"  Image: {width}x{height}, mode={mode}")
        
        # Convert to RGB if needed
        if mode not in ['RGB', 'L']:
            print(f"  Converting from {mode} to RGB")
            image = image.convert('RGB')
        
        # Perform OCR
        print("  Running OCR... (this may take a moment)")
        text = pytesseract.image_to_string(image, lang='eng')
        
        # Clean up text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned_text = '\n\n'.join(lines)
        
        word_count = len(cleaned_text.split())
        print(f"✓ Extracted {len(lines)} lines, ~{word_count} words")
        
        return cleaned_text
        
    except Exception as e:
        return f"ERROR: Failed to extract text from image - {str(e)}"


def save_as_markdown(text_content, md_path, image_filename):
    """Save OCR result as markdown with metadata"""
    try:
        # Add metadata header
        markdown_content = f"# OCR Extraction from: {image_filename}\n\n"
        markdown_content += f"_Extracted using Tesseract OCR_\n\n---\n\n"
        markdown_content += text_content
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        return True
    except Exception as e:
        print(f"ERROR: Failed to write file - {str(e)}")
        return False


def main():
    """Main execution flow"""
    
    if len(sys.argv) != 3:
        print("Usage: python3 extract_image_to_md.py <input.jpg|png> <output.md>")
        print("\nExamples:")
        print("  python3 extract_image_to_md.py scan.jpg scan.md")
        print("  python3 extract_image_to_md.py diagram.png diagram.md")
        print("\nSupported formats: JPG, JPEG, PNG, BMP, TIFF")
        sys.exit(1)
    
    image_path = sys.argv[1]
    md_path = sys.argv[2]
    
    # Validate input
    if not Path(image_path).exists():
        print(f"ERROR: Image file not found: {image_path}")
        sys.exit(1)
    
    # Check dependencies
    print("Checking dependencies...")
    success, info = ensure_dependencies_installed()
    
    if not success:
        print(f"\n✗ Failed to install: {', '.join(info)}")
        print("\nPlease install manually:")
        print("  pip3 install Pillow pytesseract")
        sys.exit(1)
    
    # Check tesseract binary
    if not check_tesseract_binary():
        print("\n⚠ WARNING: Tesseract OCR engine not found on system")
        print("\nPlease install tesseract:")
        print("  Ubuntu/Debian: sudo apt-get install tesseract-ocr")
        print("  macOS: brew install tesseract")
        print("  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        sys.exit(1)
    
    # Extract text
    print(f"\nExtracting text from image...")
    text_content = extract_text_from_image(image_path)
    
    if text_content.startswith("ERROR:"):
        print(text_content)
        sys.exit(1)
    
    # Check if any text was extracted
    if not text_content.strip():
        print("⚠ WARNING: No text was extracted from the image")
        print("  The image may not contain readable text or text may be too unclear")
    
    # Save
    print(f"Saving to: {md_path}")
    image_filename = Path(image_path).name
    
    if save_as_markdown(text_content, md_path, image_filename):
        print(f"✓ SUCCESS: Markdown file created")
        print(f"  Extracted: {len(text_content)} characters")
        return 0
    else:
        print(f"✗ FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
