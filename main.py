# main.py

import sys
import subprocess
import time
from config import NODES

def start_node(node_id, address):
    """
    Start a Raft node process.
    """
    process = subprocess.Popen(
        [sys.executable, 'node.py', str(node_id), address],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return process

def main():
    processes = {}
    try:
        # Start Raft node processes
        for node_id, address in NODES.items():
            processes[node_id] = start_node(node_id, address)
            print(f"Started Raft node {node_id} at {address}")
        
        # Keep the main process running as long as Raft nodes are running
        while any(proc.poll() is None for proc in processes.values()):
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        # Terminate all processes on exit
        for proc in processes.values():
            proc.terminate()
            proc.wait()

if __name__ == "__main__":
    main()
