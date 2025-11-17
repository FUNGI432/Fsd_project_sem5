#!/bin/bash

echo "==============================================="
echo "AI-Based Question Paper Moderation System"
echo "Installation Script for Linux/Mac"
echo "==============================================="
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo ""
echo "Step 2: Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python dependencies"
    exit 1
fi

echo ""
echo "Step 3: Creating necessary directories..."
mkdir -p data uploads logs

echo ""
echo "Step 4: Initializing database..."
python -c "from core.database import Database; db = Database(); db.initialize(); print('Database initialized successfully')"

echo ""
echo "==============================================="
echo "Backend installation complete!"
echo "==============================================="
echo ""
echo "To install the frontend, run:"
echo "  cd frontend"
echo "  npm install"
echo "  npm run build"
echo ""
echo "To start the application:"
echo "  python run.py"
echo ""
