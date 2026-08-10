#!/bin/bash
##############################################################################
# Autodev Setup Script
# Installs Python dependencies required for document conversion and automation
##############################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "════════════════════════════════════════════════════════════════"
echo "  Autodev Setup — Installing Python Dependencies"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: python3 not found"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Python detected: $PYTHON_VERSION"
echo ""

# Check pip3 is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ ERROR: pip3 not found"
    echo "Please install pip3"
    exit 1
fi

echo "Installing Python dependencies from requirements.txt..."
echo "────────────────────────────────────────────────────────────────"

cd "$PROJECT_ROOT"

# Install with user flag (no sudo needed)
pip3 install --user -r requirements.txt

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  ✅ Setup Complete!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Dependencies installed:"
echo "  • python-docx — Enhanced DOCX to Markdown conversion"
echo ""
echo "Optional system packages (install if needed):"
echo "  • poppler-utils — For PDF conversion support"
echo "    Install: sudo apt-get install poppler-utils"
echo ""
echo "You can now run ComponentSetup to register IVI components."
echo ""
