"""
WSGI entry point for Vercel
"""
import os
import sys
import traceback

# Ensure the app module can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("🚀 VERCEL WSGI HANDLER STARTING")
print("="*60)

try:
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"📁 Script directory: {sys.path[0]}")
    print("📦 Importing Flask app...")
    
    from app import app
    application = app
    
    print("✅ WSGI app loaded successfully for Vercel")
    print("="*60)
    
except Exception as e:
    print(f"❌ CRITICAL ERROR: Failed to load app")
    print(f"❌ Error type: {type(e).__name__}")
    print(f"❌ Error message: {e}")
    print(f"❌ Full traceback:")
    traceback.print_exc()
    print("="*60)
    
    # Create a minimal error handler app
    from flask import Flask
    error_app = Flask(__name__)
    
    @error_app.route('/')
    def error_index():
        return {
            "error": "Application failed to initialize",
            "type": type(e).__name__,
            "message": str(e)
        }, 500
    
    application = error_app
    print("✅ Fallback error app loaded")

if __name__ == '__main__':
    app.run()
