import psutil
import time
from datetime import datetime
import csv
# File to log the time intervals
log_file = "vscode_log.txt"

def log_event(start_time=None, end_time=None, event=""):
    # Check if the file exists and write headers if it's a new file
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        # Write headers if the file is new
        if f.tell() == 0:
            writer.writerow(["Start", "End", "Event"])
        # Write the actual event log
        writer.writerow([start_time, end_time, event])

# def log_event(event):
#     with open(log_file, "a") as f:
#         f.write(f"{event} at {datetime.now()}\n")

def is_vscode_running():
    """Check if VS Code (code.exe or code) is running."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and 'code' in proc.info['name'].lower():
            return True
    return False

def track_vscode():
    vscode_was_running = False
    i = 0
    while True:
        print(f"Checking... {i}")
        i+=1
        vscode_running = is_vscode_running()

        if vscode_running and not vscode_was_running:
            # VS Code just started
            log_event(datetime.now(),'',"VS Code opened")
            vscode_was_running = True

        elif not vscode_running and vscode_was_running:
            # VS Code just closed
            log_event('',datetime.now(),"VS Code closed")
            vscode_was_running = False

        time.sleep(10)  # Check every 10 seconds to reduce CPU usage

if __name__ == "__main__":
    # log_event("Script started") 
    track_vscode()
