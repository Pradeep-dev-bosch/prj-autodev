#!/usr/bin/env python3
"""
Enhanced DOCX to Markdown converter using python-docx library
Used by ComponentSetup wizard for document upload feature

Business Logic:
- Extracts text, headings, tables, and basic formatting from DOCX files
- Converts to clean Markdown format for easy parsing by BugAnalyst
- Preserves structure: headings, paragraphs, tables, lists

Dependencies:
- python-docx (install: pip3 install python-docx)

Fallback:
- If python-docx is not available, use extract_docx_to_md.py (standard library)
"""

import sys
from pathlib import Path

def convert_docx_to_markdown(docx_path, output_md_path):
    """
    Convert DOCX file to Markdown format.
    
    Args:
        docx_path (str): Path to input .docx file
        output_md_path (str): Path to output .md file
        
    Returns:
        bool: True if successful, False otherwise
    """
    
    try:
        from docx import Document
    except ImportError:
        print("ERROR: python-docx not installed")
        print("Install: pip3 install python-docx")
        print("Or use: extract_docx_to_md.py (standard library alternative)")
        return False
    
    try:
        # Load DOCX document
        doc = Document(docx_path)
        
        # Prepare output
        markdown_lines = []
        
        # Add header
        doc_name = Path(docx_path).name
        markdown_lines.append(f"# {doc_name}\n")
        markdown_lines.append("*Converted from DOCX format*\n")
        markdown_lines.append("---\n")
        
        # Process paragraphs
        for para in doc.paragraphs:
            text = para.text.strip()
            
            if not text:
                markdown_lines.append("")  # Empty line
                continue
            
            # Detect and convert headings
            if para.style.name.startswith('Heading'):
                level = para.style.name.replace('Heading', '').strip()
                if level.isdigit():
                    heading_level = int(level)
                    markdown_lines.append(f"{'#' * heading_level} {text}\n")
                else:
                    markdown_lines.append(f"## {text}\n")
            
            # Handle list items
            elif para.style.name.startswith('List'):
                markdown_lines.append(f"- {text}")
            
            # Regular paragraphs
            else:
                # Check for bold/italic runs
                formatted_text = text
                if para.runs:
                    parts = []
                    for run in para.runs:
                        run_text = run.text
                        if run.bold and run.italic:
                            parts.append(f"***{run_text}***")
                        elif run.bold:
                            parts.append(f"**{run_text}**")
                        elif run.italic:
                            parts.append(f"*{run_text}*")
                        else:
                            parts.append(run_text)
                    formatted_text = ''.join(parts)
                
                markdown_lines.append(f"{formatted_text}\n")
        
        # Process tables
        if doc.tables:
            markdown_lines.append("\n---\n")
            markdown_lines.append("## Tables\n")
            
            for i, table in enumerate(doc.tables, 1):
                markdown_lines.append(f"\n### Table {i}\n")
                
                for row_idx, row in enumerate(table.rows):
                    cells = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
                    
                    # Markdown table row
                    markdown_lines.append("| " + " | ".join(cells) + " |")
                    
                    # Header separator after first row
                    if row_idx == 0:
                        markdown_lines.append("| " + " | ".join(["---"] * len(cells)) + " |")
                
                markdown_lines.append("")  # Empty line after table
        
        # Write to output file
        output_path = Path(output_md_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_lines))
        
        print(f"✓ Converted: {output_md_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error converting {docx_path}: {e}")
        return False


def main():
    """Command-line interface"""
    if len(sys.argv) != 3:
        print("Usage: convert_docx_enhanced.py <input.docx> <output.md>")
        print("Example: convert_docx_enhanced.py document.docx output.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not Path(input_file).exists():
        print(f"ERROR: Input file not found: {input_file}")
        sys.exit(1)
    
    success = convert_docx_to_markdown(input_file, output_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
