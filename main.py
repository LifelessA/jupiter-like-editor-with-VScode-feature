import streamlit as st
import subprocess
import os

# Function to run the server
def run_server():
    # Ensure the server is not already running
    try:
        # This is a simple check, more robust methods might be needed for production
        with open("server.pid", "r") as f:
            pid = int(f.read())
            # Check if the process is running
            # This command works on Windows, for Linux/macOS use "ps -p {pid}"
            subprocess.check_output(f"tasklist /FI \"PID eq {pid}\"")
            return
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError):
        # PID file not found, invalid, or process is not running
        pass

    # Start the server as a background process
    process = subprocess.Popen(["python", "server.py"])
    with open("server.pid", "w") as f:
        f.write(str(process.pid))

# Run the server
run_server()

# Read the HTML file
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# Display the HTML in Streamlit
st.set_page_config(layout="wide")
st.components.v1.html(html_code, height=1000, scrolling=True)

# Clean up the PID file on exit
def cleanup():
    if os.path.exists("server.pid"):
        with open("server.pid", "r") as f:
            pid = int(f.read())
            # Terminate the process
            # This command works on Windows, for Linux/macOS use "kill {pid}"
            subprocess.run(f"taskkill /F /PID {pid}", check=False)
        os.remove("server.pid")

# Register the cleanup function
import atexit
atexit.register(cleanup)
