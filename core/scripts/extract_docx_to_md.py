#!/usr/bin/env python3
"""
Business Logic: Extract text from Word (.docx) documents and save as Markdown
Uses only Python standard library - no external dependencies required
"""

import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import re

def extract_text_from_docx(docx_path):
    """
    Extract text from a .docx file by parsing its internal XML structure.
    
    Business Logic:
    1. .docx files are ZIP archives containing XML files
    2. Main content is in word/document.xml
    3. Parse XML to extract text from <w:t> elements
    4. Process paragraphs, tables, and formatting
    
    Args:
        docx_path: Path to the .docx file
        
    Returns:
        Extracted text content as string
    """
    
    try:
        # Step 1: Open .docx as ZIP archive
        with zipfile.ZipFile(docx_path, 'r') as docx_zip:
            
            # Step 2: Read the main document XML
            try:
                xml_content = docx_zip.read('word/document.xml')
            except KeyError:
                return "ERROR: Invalid .docx file - missing word/document.xml"
            
            # Step 3: Parse XML
            root = ET.fromstring(xml_content)
            
            # Define namespace (Word uses Office Open XML namespace)
            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
                'v': 'urn:schemas-microsoft-com:vml',
                'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
            }
            
            # Step 4: Extract text blocks
            text_blocks = []
            
            # Extract paragraphs
            paragraphs = root.findall('.//w:p', namespaces)
            
            for para in paragraphs:
                # Get all text elements in the paragraph
                text_elements = para.findall('.//w:t', namespaces)
                para_text = ''.join([t.text for t in text_elements if t.text])
                
                if para_text.strip():
                    # Check if this is a heading (basic detection)
                    style = para.find('.//w:pStyle', namespaces)
                    if style is not None:
                        style_val = style.get('{' + namespaces['w'] + '}val', '')
                        if 'Heading' in style_val or 'heading' in style_val:
                            # Convert to markdown heading
                            level = 1
                            if 'Heading1' in style_val or 'heading1' in style_val:
                                level = 1
                            elif 'Heading2' in style_val or 'heading2' in style_val:
                                level = 2
                            elif 'Heading3' in style_val or 'heading3' in style_val:
                                level = 3
                            para_text = '#' * level + ' ' + para_text
                    
                    text_blocks.append(para_text)
            
            # Step 5: Extract tables
            tables = root.findall('.//w:tbl', namespaces)
            
            for table in tables:
                text_blocks.append('\n**Table:**\n')
                rows = table.findall('.//w:tr', namespaces)
                
                for row in rows:
                    cells = row.findall('.//w:tc', namespaces)
                    cell_texts = []
                    
                    for cell in cells:
                        text_elements = cell.findall('.//w:t', namespaces)
                        cell_text = ''.join([t.text for t in text_elements if t.text])
                        cell_texts.append(cell_text.strip())
                    
                    if any(cell_texts):
                        row_text = ' | '.join(cell_texts)
                        text_blocks.append(row_text)
                
                text_blocks.append('')  # Empty line after table
            
            # Step 6: Combine all text blocks
            return '\n\n'.join(text_blocks)
    
    except zipfile.BadZipFile:
        return "ERROR: File is not a valid .docx (ZIP) file"
    except Exception as e:
        return f"ERROR: Failed to extract text - {str(e)}"


def save_as_markdown(text_content, md_path):
    """
    Save extracted text as a Markdown file.
    
    Args:
        text_content: Extracted text string
        md_path: Output markdown file path
    """
    try:
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        return True
    except Exception as e:
        print(f"ERROR: Failed to write markdown file - {str(e)}")
        return False


def main():
    """
    Main execution flow:
    1. Validate input arguments
    2. Extract text from Word document
    3. Save as Markdown file
    4. Report success/failure
    """
    
    if len(sys.argv) != 3:
        print("Usage: python3 extract_docx_to_md.py <input.docx> <output.md>")
        print("Example: python3 extract_docx_to_md.py document.docx document.md")
        sys.exit(1)
    
    docx_path = sys.argv[1]
    md_path = sys.argv[2]
    
    # Validate input file exists
    if not Path(docx_path).exists():
        print(f"ERROR: Input file not found: {docx_path}")
        sys.exit(1)
    
    # Extract text
    print(f"Extracting text from: {docx_path}")
    text_content = extract_text_from_docx(docx_path)
    
    if text_content.startswith("ERROR:"):
        print(text_content)
        sys.exit(1)
    
    # Count extracted content
    lines = text_content.split('\n')
    non_empty_lines = [l for l in lines if l.strip()]
    print(f"✓ Extracted {len(non_empty_lines)} text blocks")
    
    # Save as markdown
    print(f"Saving to: {md_path}")
    if save_as_markdown(text_content, md_path):
        print(f"✓ SUCCESS: Markdown file created")
        print(f"  File size: {len(text_content)} characters")
        return 0
    else:
        print(f"✗ FAILED: Could not save markdown file")
        return 1


if __name__ == "__main__":
    sys.exit(main())
