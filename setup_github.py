#!/usr/bin/env python3
"""
GitHub Setup Script for Reasoning Extraction Model

This script helps set up and push the Reasoning Extraction Model to GitHub.
It performs the following steps:
1. Initializes a Git repository if not already initialized
2. Adds all files to the repository
3. Creates an initial commit
4. Adds the specified remote repository
5. Pushes the code to the remote repository

Usage:
    python setup_github.py [--remote REMOTE_URL] [--branch BRANCH_NAME]

Example:
    python setup_github.py --remote https://github.com/Devashish262/Reasoning-extraction-model.git --branch main
"""

import os
import argparse
import subprocess
import sys

def run_command(command, error_message=None):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if error_message:
            print(f"Error: {error_message}")
            print(f"Command output: {e.stderr}")
        return None

def is_git_repo():
    """Check if the current directory is a git repository."""
    return os.path.isdir('.git')

def setup_git_repo(remote_url, branch_name):
    """Set up a git repository and push to GitHub."""
    # Step 1: Initialize git repository if not already initialized
    if not is_git_repo():
        print("Initializing git repository...")
        run_command("git init", "Failed to initialize git repository")
    else:
        print("Git repository already initialized.")
    
    # Step 2: Add all files
    print("Adding files to git...")
    run_command("git add .", "Failed to add files to git")
    
    # Step 3: Create initial commit
    print("Creating initial commit...")
    run_command('git commit -m "Initial commit of Reasoning Extraction Model"', 
               "Failed to create initial commit")
    
    # Step 4: Add remote repository
    print(f"Adding remote repository: {remote_url}")
    # Check if remote already exists
    remotes = run_command("git remote", "Failed to get remotes")
    if remotes and "origin" in remotes.split():
        run_command("git remote remove origin", "Failed to remove existing origin")
    
    run_command(f"git remote add origin {remote_url}", 
               f"Failed to add remote repository: {remote_url}")
    
    # Step 5: Push to GitHub
    print(f"Pushing to GitHub ({branch_name} branch)...")
    result = run_command(f"git push -u origin {branch_name}", 
                        f"Failed to push to GitHub. Make sure the repository exists and you have the right permissions.")
    
    if result is not None:
        print("\nSuccessfully pushed to GitHub!")
        print(f"Repository URL: {remote_url}")
    else:
        print("\nFailed to push to GitHub. Please check the error messages above.")

def main():
    parser = argparse.ArgumentParser(description="Set up and push Reasoning Extraction Model to GitHub")
    parser.add_argument("--remote", default="https://github.com/Devashish262/Reasoning-extraction-model.git",
                        help="GitHub repository URL")
    parser.add_argument("--branch", default="main",
                        help="Branch name to push to")
    
    args = parser.parse_args()
    
    # Check if git is installed
    if run_command("git --version", "Git is not installed. Please install git before continuing.") is None:
        sys.exit(1)
    
    # Check if .env file exists and warn user
    if os.path.exists('.env'):
        print("\nWARNING: A .env file was detected in your directory.")
        print("This file may contain sensitive API keys and should not be pushed to GitHub.")
        print("The .gitignore file should prevent this, but please verify after pushing.")
        
        response = input("\nDo you want to continue? (y/n): ").strip().lower()
        if response != 'y':
            print("Setup aborted.")
            sys.exit(0)
    
    # Set up and push to GitHub
    setup_git_repo(args.remote, args.branch)

if __name__ == "__main__":
    main() 