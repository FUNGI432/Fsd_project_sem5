"""
Vercel serverless function wrapper for Flask app
"""

from backend.app import app

# Export the Flask app as the handler for Vercel
handler = app
