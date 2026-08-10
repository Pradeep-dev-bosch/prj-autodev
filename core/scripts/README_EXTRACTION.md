# Document Extraction Scripts

Comprehensive business logic for extracting text from various document formats and converting to Markdown for the ComponentSetup agent.

## Available Scripts

| Script | Purpose | Input Formats | Dependencies |
|--------|---------|---------------|--------------|
| `extract_document.py` | **Unified entry point** - auto-detects format | All formats below | Calls other scripts |
| `extract_docx_to_md.py` | Word document extraction | `.docx` | Python stdlib (zipfile, xml) |
| `extract_pdf_to_md.py` | PDF extraction | `.pdf` | PyPDF2 (auto-installs) |
| `extract_text_to_md.py` | Text/Markdown processing | `.txt`, `.md` | Python stdlib |
| `extract_image_to_md.py` | Image OCR extraction | `.jpg`, `.png`, `.bmp`, `.tiff` | Pillow, pytesseract, tesseract-ocr |

---

## Quick Start

### Option 1: Unified Extractor (Recommended)

```bash
# Auto-detects format and extracts
python3 core/scripts/extract_document.py "input_file.pdf"
python3 core/scripts/extract_document.py "document.docx" "output.md"
python3 core/scripts/extract_document.py "scan.jpg"
```

### Option 2: Specific Extractors

```bash
# Word documents
python3 core/scripts/extract_docx_to_md.py "document.docx" "output.md"

# PDF documents
python3 core/scripts/extract_pdf_to_md.py "report.pdf" "report.md"

# Text files
python3 core/scripts/extract_text_to_md.py "notes.txt" "notes.md"

# Images (OCR)
python3 core/scripts/extract_image_to_md.py "scan.jpg" "scan.md"
```

---

## Business Logic Details

### 1. Word Document Extraction (`extract_docx_to_md.py`)

**Algorithm:**
```
1. Open .docx as ZIP archive
2. Read word/document.xml
3. Parse XML using ElementTree
4. Extract text from:
   - Paragraphs (<w:p> elements)
   - Tables (<w:tbl> elements)
   - Text runs (<w:t> elements)
5. Detect and format headings
6. Combine into structured Markdown
7. Save output file
```

**Features:**
- ✓ No external dependencies (uses Python stdlib)
- ✓ Preserves document structure
- ✓ Extracts tables
- ✓ Converts headings to markdown format
- ✓ Handles complex Word XML namespace

**Example Output:**
```markdown
# Heading 1

Paragraph text...

**Table:**
Cell 1 | Cell 2 | Cell 3
Cell 4 | Cell 5 | Cell 6
```

---

### 2. PDF Extraction (`extract_pdf_to_md.py`)

**Algorithm:**
```
1. Check for PyPDF2, install if missing
2. Open PDF file
3. Iterate through pages
4. Extract text from each page
5. Add page markers
6. Combine all pages
7. Save as Markdown
```

**Features:**
- ✓ Auto-installs PyPDF2 if missing
- ✓ Page-by-page extraction
- ✓ Progress indicators for large PDFs
- ✓ Handles multi-page documents
- ✓ Pure Python implementation

**Example Output:**
```markdown
--- Page 1 ---

First page content...

--- Page 2 ---

Second page content...
```

---

### 3. Text Processing (`extract_text_to_md.py`)

**Algorithm:**
```
1. Read text file with UTF-8 encoding
2. Normalize line endings
3. Detect potential headings:
   - UPPERCASE lines → ## Headings
   - Lines ending with : → ### Headings
4. Apply markdown formatting
5. Save formatted output
```

**Features:**
- ✓ Handles various encodings
- ✓ Normalizes line endings
- ✓ Auto-detects headings
- ✓ Cleans up whitespace
- ✓ Preserves original structure

---

### 4. Image OCR Extraction (`extract_image_to_md.py`)

**Algorithm:**
```
1. Check dependencies (Pillow, pytesseract)
2. Verify tesseract binary is installed
3. Load image with PIL
4. Convert to RGB if needed
5. Run Tesseract OCR
6. Clean and format extracted text
7. Save with metadata
```

**Features:**
- ✓ Auto-installs Python dependencies
- ✓ Supports multiple image formats
- ✓ Automatic image conversion
- ✓ Text cleanup and formatting
- ✓ Metadata headers in output

**System Requirements:**
Must install Tesseract OCR engine:
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Verify installation
tesseract --version
```

---

## Integration with ComponentSetup Agent

The ComponentSetup agent uses these scripts to automatically convert documents:

### Workflow Integration

```python
# ComponentSetup detects Word document
file_path = "core/docs/components/dtv-service/design-docs/SWCDD_DTV Service.docx"

# Route to unified extractor
run_in_terminal(
    command=f'python3 core/scripts/extract_document.py "{file_path}"',
    goal="Extract text from design document",
    isBackground=False,
    timeout=15000
)

# Reads the generated .md file
content = read_file(f"{file_path}.md")

# Proceeds with extraction and analysis
```

### Error Handling

All scripts implement consistent error handling:

1. **Missing dependencies** → Auto-install or provide instructions
2. **File not found** → Clear error message with file path
3. **Conversion failure** → Detailed error with recovery options
4. **Empty output** → Warning with suggestions

Example error flow:
```
if tool_missing:
    offer_installation()
    if install_fails:
        suggest_manual_conversion()
        offer_copy_paste_alternative()
        offer_skip_to_manual_interview()
```

---

## Installation & Dependencies

### Python Dependencies

All Python libraries auto-install when needed:

```bash
# PDF extraction
pip3 install PyPDF2

# Image OCR
pip3 install Pillow pytesseract
```

### System Dependencies

Only required for image OCR:

```bash
# Tesseract OCR engine
sudo apt-get install tesseract-ocr        # Debian/Ubuntu
brew install tesseract                    # macOS
choco install tesseract                   # Windows
```

---

## Output Format

All extractors output clean Markdown with:

- **Headings** — Properly formatted (`#`, `##`, `###`)
- **Paragraphs** — Clean line breaks
- **Tables** — Pipe-separated format
- **Metadata** — Source file info (for OCR)
- **Page markers** — For multi-page PDFs

Example output structure:
```markdown
# Document Title

## Section 1

Paragraph text...

### Subsection

More content...

**Table:**
Col1 | Col2 | Col3
Data1 | Data2 | Data3
```

---

## Testing

Test each extractor:

```bash
# Create test directory
mkdir -p test_docs

# Test Word extraction
python3 core/scripts/extract_docx_to_md.py test_docs/test.docx test_docs/test_word.md

# Test PDF extraction
python3 core/scripts/extract_pdf_to_md.py test_docs/test.pdf test_docs/test_pdf.md

# Test text processing
python3 core/scripts/extract_text_to_md.py test_docs/test.txt test_docs/test_text.md

# Test image OCR
python3 core/scripts/extract_image_to_md.py test_docs/test.jpg test_docs/test_image.md

# Test unified extractor
python3 core/scripts/extract_document.py test_docs/test.docx
```

---

## Troubleshooting

### Word Document Issues

**Problem:** "Invalid .docx file"
- **Solution:** File may be corrupted or not a valid .docx format
- Try opening in Word and saving again

### PDF Issues

**Problem:** "No text extracted"
- **Solution:** PDF may contain scanned images, not actual text
- Use OCR script on PDF screenshots instead

### OCR Issues

**Problem:** "Tesseract not found"
- **Solution:** Install system binaries: `sudo apt-get install tesseract-ocr`

**Problem:** "No text extracted from image"
- **Solution:** Image quality may be too low or text too small
- Try increasing image resolution

---

## Performance

Typical processing times (estimates):

| Format | File Size | Time |
|--------|-----------|------|
| Word (.docx) | 1 MB | <1 sec |
| PDF | 10 pages | 2-5 sec |
| PDF | 100 pages | 20-30 sec |
| Image OCR | 1 image | 5-10 sec |
| Text | Any size | <1 sec |

---

## Future Enhancements

Potential additions:
- [ ] PowerPoint extraction (`.pptx`)
- [ ] Excel spreadsheet extraction (`.xlsx`)
- [ ] RTF document support
- [ ] HTML to Markdown conversion
- [ ] Multi-language OCR support
- [ ] Batch processing mode
- [ ] PDF with image fallback (if no text, try OCR)

---

## License & Credits

- **PyPDF2** - PDF extraction library
- **Pillow** - Python Imaging Library
- **Tesseract OCR** - Open source OCR engine
- **Python stdlib** - zipfile, xml.etree, pathlib

---

**Last Updated:** April 22, 2026
**Component:** ComponentSetup Document Extraction
**Status:** Production Ready ✓
