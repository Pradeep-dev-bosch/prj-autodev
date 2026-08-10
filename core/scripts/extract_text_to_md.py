#!/usr/bin/env python3
"""
Business Logic: Process text and markdown files - validate and optionally format
"""

import sys
from pathlib import Path
import re


def process_text_file(file_path, output_format='md'):
    """
    Read and process text/markdown files.
    
    Business Logic:
    1. Read the file with UTF-8 encoding
    2. Normalize line endings
    3. Optionally add markdown formatting
    4. Return processed content
    
    Args:
        file_path: Path to text/markdown file
        output_format: 'md' for markdown, 'txt' for plain text
        
    Returns:
        Processed text content
    """
    
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Normalize line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # If input is .txt and output is .md, add basic markdown structure
        if file_path.endswith('.txt') and output_format == 'md':
            # Detect potential headings (UPPERCASE lines or lines ending with :)
            lines = content.split('\n')
            formatted_lines = []
            
            for line in lines:
                stripped = line.strip()
                
                # Convert UPPERCASE lines to headings
                if stripped and stripped.isupper() and len(stripped) < 100:
                    formatted_lines.append(f"## {stripped.title()}")
                # Convert lines ending with : to headings
                elif stripped.endswith(':') and len(stripped) < 100:
                    formatted_lines.append(f"### {stripped[:-1]}")
                else:
                    formatted_lines.append(line)
            
            content = '\n'.join(formatted_lines)
        
        return content
        
    except Exception as e:
        return f"ERROR: Failed to read text file - {str(e)}"


def save_output(content, output_path):
    """Save processed content"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"ERROR: Failed to write file - {str(e)}")
        return False


def main():
    """Main execution flow"""
    
    if len(sys.argv) not in [2, 3]:
        print("Usage: python3 extract_text_to_md.py <input.txt|input.md> [output.md]")
        print("\nExamples:")
        print("  python3 extract_text_to_md.py document.txt document.md")
        print("  python3 extract_text_to_md.py document.md  # outputs to same name")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    # Determine output path
    if len(sys.argv) == 3:
        output_path = sys.argv[2]
    else:
        # Replace extension with .md
        output_path = str(Path(input_path).with_suffix('.md'))
    
    # Validate input
    if not Path(input_path).exists():
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)
    
    # Detect output format
    output_format = 'md' if output_path.endswith('.md') else 'txt'
    
    # Process file
    print(f"Processing: {input_path}")
    content = process_text_file(input_path, output_format)
    
    if content.startswith("ERROR:"):
        print(content)
        sys.exit(1)
    
    # Count statistics
    lines = [l for l in content.split('\n') if l.strip()]
    chars = len(content)
    
    print(f"✓ Processed {len(lines)} lines, {chars} characters")
    
    # Save
    print(f"Saving to: {output_path}")
    if save_output(content, output_path):
        print(f"✓ SUCCESS: File created")
        return 0
    else:
        print(f"✗ FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
