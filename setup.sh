#!/bin/bash
# Installation and setup script for Uber Driver Profit Maximizer Dashboard

echo "=================================="
echo "Uber Driver Profit Maximizer Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python installation..."
python --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Run tests
echo ""
echo "Running pipeline tests..."
python test_pipeline.py

echo ""
echo "=================================="
echo "Setup complete!"
echo "=================================="
echo ""
echo "To run the dashboard:"
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo ""
