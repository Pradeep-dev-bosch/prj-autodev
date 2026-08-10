#!/usr/bin/env python3
"""
Unified Document Extraction Business Logic
Automatically detects file type and routes to appropriate extraction method

Supported formats:
- Word documents (.docx)
- PDF documents (.pdf)
- Text files (.txt)
- Markdown files (.md)
- Images (.jpg, .jpeg, .png, .bmp, .tiff) - with OCR
"""

import sys
import subprocess
from pathlib import Path


# Map of file extensions to extraction scripts
EXTRACTORS = {
    '.docx': 'extract_docx_to_md.py',
    '.pdf': 'extract_pdf_to_md.py',
    '.txt': 'extract_text_to_md.py',
    '.md': 'extract_text_to_md.py',
    '.jpg': 'extract_image_to_md.py',
    '.jpeg': 'extract_image_to_md.py',
    '.png': 'extract_image_to_md.py',
    '.bmp': 'extract_image_to_md.py',
    '.tiff': 'extract_image_to_md.py',
    '.tif': 'extract_image_to_md.py',
}


def detect_file_type(file_path):
    """
    Detect file type from extension.
    
    Returns: (extension, extractor_script)
    """
    ext = Path(file_path).suffix.lower()
    
    if ext in EXTRACTORS:
        return ext, EXTRACTORS[ext]
    else:
        return ext, None


def run_extractor(script_name, input_path, output_path):
    """
    Execute the appropriate extraction script.
    
    Business Logic:
    1. Get the directory containing this script
    2. Build path to the specific extractor
    3. Run extractor as subprocess
    4. Return success/failure
    """
    
    # Get script directory
    script_dir = Path(__file__).parent
    extractor_path = script_dir / script_name
    
    if not extractor_path.exists():
        print(f"ERROR: Extractor script not found: {extractor_path}")
        return False
    
    # Run extractor
    try:
        result = subprocess.run(
            [sys.executable, str(extractor_path), input_path, output_path],
            capture_output=False,  # Show output directly
            text=True
        )
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"ERROR: Failed to run extractor - {str(e)}")
        return False


def main():
    """
    Main business logic:
    1. Parse command line arguments
    2. Detect file type
    3. Route to appropriate extractor
    4. Report results
    """
    
    if len(sys.argv) not in [2, 3]:
        print("=" * 70)
        print("Unified Document Extraction Tool")
        print("=" * 70)
        print("\nUsage: python3 extract_document.py <input_file> [output.md]")
        print("\nSupported formats:")
        print("  • Word documents (.docx)")
        print("  • PDF documents (.pdf)")
        print("  • Text files (.txt)")
        print("  • Markdown files (.md)")
        print("  • Images (.jpg, .png, .bmp, .tiff) - with OCR")
        print("\nExamples:")
        print("  python3 extract_document.py document.docx")
        print("  python3 extract_document.py report.pdf report.md")
        print("  python3 extract_document.py scan.jpg")
        print("=" * 70)
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    # Validate input file exists
    if not Path(input_path).exists():
        print(f"✗ ERROR: File not found: {input_path}")
        sys.exit(1)
    
    # Detect file type
    ext, extractor = detect_file_type(input_path)
    
    if not extractor:
        print(f"✗ ERROR: Unsupported file type: {ext}")
        print(f"\nSupported: {', '.join(EXTRACTORS.keys())}")
        sys.exit(1)
    
    # Determine output path
    if len(sys.argv) == 3:
        output_path = sys.argv[2]
    else:
        # Auto-generate output filename
        output_path = str(Path(input_path).with_suffix('.md'))
    
    # Show processing info
    print("=" * 70)
    print(f"Input:  {input_path} ({ext})")
    print(f"Output: {output_path}")
    print(f"Method: {extractor}")
    print("=" * 70)
    print()
    
    # Run extraction
    success = run_extractor(extractor, input_path, output_path)
    
    print()
    print("=" * 70)
    if success:
        print("✓ EXTRACTION SUCCESSFUL")
        print(f"  Output saved to: {output_path}")
    else:
        print("✗ EXTRACTION FAILED")
        print("  Check error messages above for details")
    print("=" * 70)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
