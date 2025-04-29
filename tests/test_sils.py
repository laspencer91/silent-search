#!/usr/bin/env python3
"""
Test script for SilentSearch (sils)
This script runs various test commands to verify the functionality of SilentSearch.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Add the parent directory to the path so we can import sils
sys.path.insert(0, str(Path(__file__).parent.parent))

# Path to the sils script
SILS_SCRIPT = Path(__file__).parent.parent / "sils.py"

# Path to the test config
TEST_CONFIG = Path(__file__).parent / "config" / "config.toml"

# Path to the test files
TEST_FILES = Path(__file__).parent / "test_files"

# Temporary directory for test outputs
TEMP_DIR = Path(__file__).parent / "temp_output"
TEMP_DIR.mkdir(exist_ok=True)

def run_command(args):
    """Run a command and return the output."""
    # Set the config file path as an environment variable
    env = os.environ.copy()
    env["SILS_CONFIG"] = str(TEST_CONFIG)
    
    # Run the command
    cmd = [sys.executable, str(SILS_SCRIPT)] + args
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return None

def test_basic_search():
    """Test basic search functionality."""
    print("\n=== Testing Basic Search ===")
    output = run_command(["-n", "main"])
    print(output)

def test_file_type_filtering():
    """Test file type filtering."""
    print("\n=== Testing File Type Filtering ===")
    
    # Test image search
    print("\n--- Image Search ---")
    output = run_command(["-t", "img", "-n", "texture"])
    print(output)
    
    # Test code search
    print("\n--- Code Search ---")
    output = run_command(["-t", "code", "-n", "main"])
    print(output)
    
    # Test custom type search
    print("\n--- Custom Type Search ---")
    output = run_command(["-t", "web", "-n", "site"])
    print(output)

def test_path_and_recursive():
    """Test path and recursive options."""
    print("\n=== Testing Path and Recursive Options ===")
    
    # Test specific path
    print("\n--- Specific Path ---")
    output = run_command(["-p", str(TEST_FILES / "images"), "-n", "texture"])
    print(output)
    
    # Test non-recursive search
    print("\n--- Non-Recursive Search ---")
    output = run_command(["--no-recursive", "-n", "main"])
    print(output)

def test_copy_files():
    """Test copying files."""
    print("\n=== Testing Copy Files ===")
    
    # Create a temporary directory for copied files
    copy_dir = TEMP_DIR / "copied_files"
    copy_dir.mkdir(exist_ok=True)
    
    # Copy files
    print("\n--- Copy Files ---")
    output = run_command(["-t", "img", "-n", "texture", "-c", str(copy_dir)])
    print(output)
    
    # List copied files
    print("\n--- Copied Files ---")
    for file in copy_dir.glob("*"):
        print(f"  {file.name}")

def test_open_explorer():
    """Test opening file explorer."""
    print("\n=== Testing Open Explorer ===")
    print("Note: This will open your file explorer. Press Ctrl+C to skip.")
    try:
        output = run_command(["-t", "code", "-n", "main", "-o"])
        print(output)
    except KeyboardInterrupt:
        print("Skipped opening file explorer.")

def cleanup():
    """Clean up temporary files."""
    print("\n=== Cleaning Up ===")
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
        print(f"Removed {TEMP_DIR}")

def main():
    """Run all tests."""
    print("=== SilentSearch Test Suite ===")
    
    try:
        test_basic_search()
        test_file_type_filtering()
        test_path_and_recursive()
        test_copy_files()
        test_open_explorer()
    finally:
        cleanup()
    
    print("\n=== Tests Completed ===")

if __name__ == "__main__":
    main() 