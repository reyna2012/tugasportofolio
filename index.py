"""
WSGI entry point for Vercel deployment.
This file is the main entry point for Vercel's serverless functions.
"""
import os
import sys
import traceback
from pathlib import Path

# Add current directory to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

# Set environment for Vercel
os.environ.setdefault('FLASK_ENV', 'production')

def create_app():
    """Create Flask application with error handling for Vercel."""
    try:
        # Import Flask app
        from app import app as flask_app
        print("✅ Flask app loaded successfully")
        return flask_app
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Failed to load Flask app: {e}")
        traceback.print_exc()
        
    # Fallback app if main app fails
    from flask import Flask
    fallback_app = Flask(__name__)

    @fallback_app.route('/')
    @fallback_app.route('/<path:path>')
    def fallback_handler(path=None):
        return {
            "error": "Application failed to initialize",
            "message": str(e),
            "hint": "Check Vercel function logs for details"
        }, 500

    return fallback_app


# Create the application
app = application = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
