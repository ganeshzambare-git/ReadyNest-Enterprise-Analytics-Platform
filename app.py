import sys
from pathlib import Path
import subprocess
import os

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

port = os.environ.get("PORT", "8501")

subprocess.run([
    "streamlit",
    "run",
    "src/app/main.py",
    "--server.port",
    port,
    "--server.address",
    "0.0.0.0"
])
