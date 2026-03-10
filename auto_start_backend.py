import subprocess
import sys
import time
import requests
import os

def check_backend_running():
    """Check if backend is running on port 8000"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Start the backend server"""
    print("🚀 Starting HireLens Backend Server...")
    
    # Change to project directory
    os.chdir(r"d:\Windsurf\Hire lens FYP\hire_lens-dev")
    
    # Start the server
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    except KeyboardInterrupt:
        print("\n👋 Backend server stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

if __name__ == "__main__":
    if not check_backend_running():
        print("⚠️ Backend not running, starting it now...")
        start_backend()
    else:
        print("✅ Backend is already running!")
