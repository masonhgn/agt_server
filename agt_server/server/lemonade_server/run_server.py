#!/usr/bin/env python3
"""
Run the lemonade competition server
"""

import os
import sys

# Add the parent directories to the path so we can import core modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def main():
    print("Lemonade Competition Server")
    print("=" * 40)
    
    # Check if we have the required dependencies
    try:
        import flask
        print("Flask found")
    except ImportError:
        print("Flask not found. Install with: pip install flask")
        return
    
    try:
        import requests
        print("Requests found")
    except ImportError:
        print("Requests not found. Install with: pip install requests")
        return
    
    # Import our modules
    try:
        from lemonade_competition import LemonadeCompetition
        from lemonade_web import app
        print("Lemonade competition modules loaded")
    except ImportError as e:
        print(f"Error loading modules: {e}")
        return
    
    print("\nStarting web server...")
    print("Web interface: http://localhost:8083")
    print("Agents directory: agents/")
    print("Press Ctrl+C to stop")
    print("-" * 40)
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=8083, debug=True)

if __name__ == "__main__":
    main()
