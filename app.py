import subprocess
import os
import sys

port = os.environ.get("PORT", "8501")

env = os.environ.copy()
project_root = os.path.abspath(os.path.dirname(__file__))
if "PYTHONPATH" in env:
    env["PYTHONPATH"] = f"{project_root}{os.pathsep}{env['PYTHONPATH']}"
else:
    env["PYTHONPATH"] = project_root

subprocess.run([
    sys.executable,
    "-m",
    "streamlit",
    "run",
    "src/app/main.py",
    "--server.port",
    port,
    "--server.address",
    "0.0.0.0"
], env=env)
