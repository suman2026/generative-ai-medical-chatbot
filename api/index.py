# 🏥 Vercel Serverless Entry Point for Medical Chatbot
from flask import Flask
import sys
import os

# Add the parent directory to the path so we can import from app.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app

# This is the entry point for Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

# For local development
if __name__ == "__main__":
    app.run(debug=True)