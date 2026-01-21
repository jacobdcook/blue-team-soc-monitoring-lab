#!/usr/bin/env python3
"""
Brute Force Attack Simulator for SOC Lab

This script simulates failed authentication attempts that Wazuh will detect.
It generates failed login attempts that appear in /var/log/auth.log,
which Wazuh monitors for security events.

Run this after Wazuh is up and running to test detection capabilities.
"""

import subprocess
import time
import random
import sys
from datetime import datetime

LOG_FILE = "attack_log.txt"

def log_attempt(username, timestamp, success=False):
    """Log each authentication attempt to a file"""
    status = "SUCCESS" if success else "FAILED"
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - Username: {username}, Status: {status}\n")

def simulate_failed_login(username="nonexistentuser", password="wrongpass123"):
    """
    Simulate a failed login attempt using su command.
    This will generate entries in /var/log/auth.log that Wazuh monitors.
    """
    try:
        # Try to login with wrong credentials - this creates auth.log entries
        result = subprocess.run(
            ["sudo", "su", "-", username, "-c", "exit"],
            input=f"{password}\n".encode(),
            capture_output=True,
            timeout=2,
            stderr=subprocess.PIPE
        )
        return False  # Always fails with wrong credentials
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        # Expected to fail - that's the point!
        return False

def simulate_brute_force(num_attempts=20, delay_range=(1, 2)):
    """
    Simulate a brute-force attack by generating multiple failed login attempts.
    
    Args:
        num_attempts: Number of login attempts to make
        delay_range: Tuple of (min, max) seconds between attempts
    """
    print(f"\n{'='*60}")
    print(f"BRUTE FORCE ATTACK SIMULATOR")
    print(f"{'='*60}")
    print(f"Attempts: {num_attempts}")
    print(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"This will generate failed login attempts in /var/log/auth.log")
    print(f"Wazuh will detect these and generate security alerts!")
    print(f"{'='*60}\n")
    
    # Clear previous log file
    with open(LOG_FILE, "w") as f:
        f.write(f"Brute Force Attack Simulation - Started: {datetime.now()}\n")
        f.write(f"{'='*60}\n")
    
    failed_attempts = 0
    common_usernames = ["admin", "root", "user", "test", "administrator", 
                       "guest", "demo", "admin123", "password", "test123"]
    
    for i in range(1, num_attempts + 1):
        # Randomly select username
        username = random.choice(common_usernames)
        password = f"wrongpass{i}"
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Simulate failed login attempt
        success = simulate_failed_login(username, password)
        
        if not success:
            failed_attempts += 1
        
        # Log the attempt
        log_attempt(username, timestamp, success)
        
        # Print progress
        if i % 5 == 0 or i == num_attempts:
            print(f"[{i}/{num_attempts}] Failed login attempts: {failed_attempts} | Latest: {username}")
        
        # Random delay between attempts (simulates real attacker behavior)
        if i < num_attempts:
            delay = random.uniform(delay_range[0], delay_range[1])
            time.sleep(delay)
    
    print(f"\n{'='*60}")
    print(f"ATTACK SIMULATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total attempts: {num_attempts}")
    print(f"Failed attempts: {failed_attempts}")
    print(f"Attack log saved to: {LOG_FILE}")
    print(f"\n✅ Now check your Wazuh Dashboard!")
    print(f"   Go to: Security events or Alerts section")
    print(f"   Look for alerts about failed authentication attempts")
    print(f"   Rule IDs to look for: 5503, 5710, or similar")
    print(f"{'='*60}\n")

def main():
    """Main function"""
    print("\n" + "="*60)
    print("Wazuh SOC Lab - Brute Force Attack Simulator")
    print("="*60)
    print("\nThis script will simulate a brute-force attack by generating")
    print("multiple failed authentication attempts. These will appear in")
    print("/var/log/auth.log, which Wazuh monitors for security events.\n")
    print("⚠️  NOTE: You may need to enter your sudo password")
    print("   (This is needed to generate authentication attempts)\n")
    
    try:
        num_attempts = input("Enter number of login attempts to simulate (default 20, press Enter): ").strip()
        if not num_attempts:
            num_attempts = 20
        else:
            num_attempts = int(num_attempts)
        
        if num_attempts < 1:
            print("Error: Number of attempts must be at least 1")
            sys.exit(1)
    except (ValueError, KeyboardInterrupt):
        print("\nUsing default: 20 attempts")
        num_attempts = 20
    
    print(f"\n⚠️  Starting simulation in 3 seconds...")
    print(f"   Make sure your Wazuh Dashboard is open in your browser!")
    time.sleep(3)
    
    simulate_brute_force(num_attempts)

if __name__ == "__main__":
    main()
