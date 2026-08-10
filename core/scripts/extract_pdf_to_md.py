#!/usr/bin/env python3
"""
Business Logic: Extract text from PDF documents and save as Markdown
Uses PyPDF2 (pure Python) - installs automatically if missing
"""

import sys
from pathlib import Path
import subprocess

def ensure_pypdf2_installed():
    """Check if PyPDF2 is installed, install if missing"""
    try:
        import PyPDF2
        return True
    except ImportError:
        print("PyPDF2 not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
            import PyPDF2
            print("✓ PyPDF2 installed successfully")
            return True
        except Exception as e:
            print(f"✗ Failed to install PyPDF2: {e}")
            return False


def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF using PyPDF2.
    
    Business Logic:
    1. Open PDF file
    2. Iterate through all pages
    3. Extract text from each page
    4. Combine with page markers
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text content as string
    """
    
    import PyPDF2
    
    try:
        text_blocks = []
        
        # Open PDF file
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            total_pages = len(pdf_reader.pages)
            print(f"Processing {total_pages} pages...")
            
            # Extract text from each page
            for page_num, page in enumerate(pdf_reader.pages, start=1):
                text = page.extract_text()
                
                if text.strip():
                    # Add page marker
                    text_blocks.append(f"\n--- Page {page_num} ---\n")
                    text_blocks.append(text.strip())
                    
                # Progress indicator
                if page_num % 10 == 0:
                    print(f"  Processed {page_num}/{total_pages} pages")
            
            print(f"✓ Extracted text from {total_pages} pages")
            
        return '\n\n'.join(text_blocks)
        
    except Exception as e:
        return f"ERROR: Failed to extract text from PDF - {str(e)}"


def save_as_markdown(text_content, md_path):
    """Save extracted text as Markdown file"""
    try:
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        return True
    except Exception as e:
        print(f"ERROR: Failed to write file - {str(e)}")
        return False


def main():
    """Main execution flow"""
    
    if len(sys.argv) != 3:
        print("Usage: python3 extract_pdf_to_md.py <input.pdf> <output.md>")
        print("Example: python3 extract_pdf_to_md.py document.pdf document.md")
        sys.exit(1)
    
    # Ensure PyPDF2 is installed
    if not ensure_pypdf2_installed():
        print("\nAlternative: Install manually with: pip3 install PyPDF2")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    md_path = sys.argv[2]
    
    # Validate input
    if not Path(pdf_path).exists():
        print(f"ERROR: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    # Extract text
    print(f"\nExtracting text from: {pdf_path}")
    text_content = extract_text_from_pdf(pdf_path)
    
    if text_content.startswith("ERROR:"):
        print(text_content)
        sys.exit(1)
    
    # Save
    print(f"Saving to: {md_path}")
    if save_as_markdown(text_content, md_path):
        print(f"✓ SUCCESS: Markdown file created")
        print(f"  File size: {len(text_content)} characters")
        return 0
    else:
        print(f"✗ FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
