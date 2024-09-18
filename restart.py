#!/usr/bin/env python3
import subprocess
import time

command = ["python", "dawn.py"]  
while True:
    try:
        process = subprocess.Popen(command)
        process.wait()
    except KeyboardInterrupt:
        print("\nScript stopping manually.")
        break
    except Exception as e:
        print(f"\nError: {e}")
        print("Restarting...")
        time.sleep(1)
