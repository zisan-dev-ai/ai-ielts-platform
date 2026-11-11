"""
AI IELTS - Local Server Runner
Run this script to start the local AI IELTS platform on http://127.0.0.1:8000
"""

import os
import sys
import subprocess
import socket

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0

def get_free_port(preferred: int = 8000) -> int:
    if not is_port_in_use(preferred):
        return preferred
    for p in [8000, 8001, 8080, 8081, 5000]:
        if not is_port_in_use(p):
            return p
    return preferred

def main():
    preferred_port = int(os.environ.get("PORT", 8000))
    port = get_free_port(preferred_port)
    
    if port != preferred_port:
        print(f"⚠️ Port {preferred_port} is currently in use.")
        print(f"👉 AI IELTS will start on alternative port: http://127.0.0.1:{port}\n")
    
    os.environ["PORT"] = str(port)

    print("=" * 65)
    print("  🎓 Starting AI IELTS — Cambridge 9-Band Platform")
    print(f"  👉 Open your browser at: http://127.0.0.1:{port}")
    print("  👉 Live 1-on-1 AI Teacher, CBT Simulator & Analytics ready")
    print("  Press Ctrl+C to stop the server.")
    print("=" * 65)
    
    cmd = [
        sys.executable, "-m", "uvicorn",
        "main:app",
        "--host", "127.0.0.1",
        "--port", str(port),
        "--reload"
    ]
    try:
        subprocess.run(cmd, cwd=ROOT_DIR)
    except KeyboardInterrupt:
        print("\n[AI IELTS] Server stopped successfully.")

if __name__ == "__main__":
    main()
