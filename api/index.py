"""
Vercel serverless function handler for Flask app
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import Flask app
from backend.app import app

# Export the Flask app as the handler for Vercel
handler = app
