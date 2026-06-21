import subprocess
import os

# Guarantee Chrome PATH is set before spinning up Streamlit subprocess
chrome_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".chrome", "chrome-win64"))
chrome_exe = os.path.join(chrome_dir, "chrome.exe")
if os.path.exists(chrome_dir):
    if chrome_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = chrome_dir + os.pathsep + os.environ.get("PATH", "")
    os.environ["CHROME_EXECUTABLE"] = chrome_exe
    os.environ["CHROME_PATH"] = chrome_exe

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
