#!/usr/bin/env python3
"""
Main entry point for the AI-Based Question Paper Moderation System
This script initializes and runs both the Flask backend server
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import Flask app
from backend.app import app, db

def initialize_application():
    """Initialize the application"""
    print("Initializing AI-Based Question Paper Moderation System...")
    
    # Create necessary directories
    directories = [
        'data',
        'uploads',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory '{directory}' ready")
    
    # Initialize database
    print("Initializing database...")
    db.initialize()
    print("✓ Database initialized")
    
    print("\nApplication initialized successfully!")
    print("=" * 70)

def main():
    """Main function to run the application"""
    initialize_application()
    
    # Get configuration from environment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"\nStarting server on {host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"\nAccess the application at:")
    print(f"  Local:   http://localhost:{port}")
    print(f"  Network: http://127.0.0.1:{port}")
    print("\nPress CTRL+C to stop the server")
    print("=" * 70)
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        db.close()
        print("Application stopped")

if __name__ == '__main__':
    main()
