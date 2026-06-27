import sys
from pathlib import Path
import subprocess
import os

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Dummy WSGI app to satisfy Vercel's @vercel/python builder
def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"Streamlit is starting on Vercel..."]

port = os.environ.get("PORT", "8501")

# Use Popen instead of run() to prevent blocking Vercel's builder during deployment
subprocess.Popen([
    "streamlit",
    "run",
    "src/app/main.py",
    "--server.port",
    port,
    "--server.address",
    "0.0.0.0"
])
