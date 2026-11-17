"""
Launch script for NeuroSched Web Showcase.
Starts the server and automatically opens http://localhost:5000 in your browser.
"""
import os
import sys
import threading
import time
import webbrowser

def open_browser(port):
    time.sleep(1.2)
    url = f"http://localhost:{port}"
    print(f"\n[Launcher] Opening browser at {url} ...")
    webbrowser.open(url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Launch browser in separate thread
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    
    # Run Flask server
    from app import app
    print(f"==================================================================")
    print(f"  NeuroSched: ML-Based CPU Scheduler Web Showcase")
    print(f"  Running at http://localhost:{port}")
    print(f"  Press Ctrl+C to stop the server")
    print(f"==================================================================")
    app.run(host="0.0.0.0", port=port, debug=False)
