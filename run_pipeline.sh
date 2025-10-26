#!/bin/bash

# Rearc Data Quest - Data Pipeline Runner
# This script runs the complete data pipeline

set -e  # Exit on error

echo "=========================================="
echo "Rearc Data Quest - Data Pipeline"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create data directory if it doesn't exist
mkdir -p data

# Step 1: Fetch data
echo ""
echo "Step 1: Fetching data from BLS API..."
python3 scripts/fetch_data.py

# Step 2: Process data
echo ""
echo "Step 2: Processing data..."
python3 scripts/process_data.py

# Step 3: Analyze data
echo ""
echo "Step 3: Analyzing data..."
python3 scripts/analyze_data.py

echo ""
echo "=========================================="
echo "Pipeline completed successfully!"
echo "=========================================="
echo "Check the 'data' directory for output files."
