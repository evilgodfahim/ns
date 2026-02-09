#!/bin/bash

# New Scientist RSS Scraper - Setup Script
# This script helps you set up the project quickly

set -e

echo "=================================="
echo "New Scientist RSS Scraper Setup"
echo "=================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Git found: $(git --version)"
echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run the scraper locally: python scraper.py"
echo "2. Validate the feed: python validate_feed.py"
echo "3. Push to GitHub and enable Actions"
echo "4. Enable GitHub Pages in repository settings"
echo ""
echo "To activate the virtual environment in the future:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  source venv/Scripts/activate"
else
    echo "  source venv/bin/activate"
fi
echo ""
