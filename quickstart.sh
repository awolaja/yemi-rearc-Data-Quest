#!/bin/bash

# Quick Start Script for Rearc Data Quest
# This script provides an interactive setup experience

set -e

echo "╔════════════════════════════════════════════════════╗"
echo "║   Rearc Data Quest - Quick Start Setup            ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher from python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python found: $PYTHON_VERSION"

# Validate Python version is 3.8 or higher
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "❌ Error: Python 3.8 or higher is required"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies (this may take a few minutes)..."
if ! pip install --upgrade pip -q; then
    echo "⚠ Warning: Failed to upgrade pip"
fi

if pip install -r requirements.txt -q; then
    echo "✓ Dependencies installed successfully"
else
    echo "⚠ Warning: Some dependencies may not have installed correctly"
    echo "You may need to install them manually with: pip install -r requirements.txt"
fi

# Create data directory
mkdir -p data
echo "✓ Data directory ready"

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║   Setup Complete!                                  ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "You can now run the pipeline with:"
echo "  ./run_pipeline.sh"
echo ""
echo "Or run individual scripts:"
echo "  python3 scripts/fetch_data.py    # Fetch data from BLS API"
echo "  python3 scripts/process_data.py  # Process the data"
echo "  python3 scripts/analyze_data.py  # Analyze the data"
echo ""
echo "To view all available commands:"
echo "  make help"
echo ""
echo "For more information, see:"
echo "  - README.md          - Project overview"
echo "  - docs/SETUP.md      - Detailed setup guide"
echo "  - docs/API.md        - API documentation"
echo ""
echo "Happy coding! 🚀"
