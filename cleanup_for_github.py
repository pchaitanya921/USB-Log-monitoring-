#!/usr/bin/env python3
"""
Cleanup script for USB HawkEye project before GitHub upload.
This script removes temporary files, build artifacts, and sensitive data.
"""

import os
import shutil
import json
from pathlib import Path

def cleanup_project():
    """Clean up the project directory for GitHub upload."""
    
    print("🧹 Cleaning up USB HawkEye project for GitHub upload...")
    
    # Files and directories to remove
    items_to_remove = [
        'dist/',
        'build/',
        'temp_diskpart.txt',
        'users.json',
        'USB/',
        'cinematic_hacker_loop.py',
        'hacker_loop.py',
        'cyberpunk_tracking.py',
        'download_world_map.py',
        '__pycache__/',
        '*.pyc',
        '*.pyo',
        '*.log'
    ]
    
    # Remove items
    for item in items_to_remove:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
                print(f"✅ Removed directory: {item}")
            else:
                os.remove(item)
                print(f"✅ Removed file: {item}")
    
    # Remove Python cache files
    for root, dirs, files in os.walk('.'):
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            shutil.rmtree(cache_dir)
            print(f"✅ Removed cache directory: {cache_dir}")
        
        # Remove .pyc and .pyo files
        for file in files:
            if file.endswith(('.pyc', '.pyo')):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"✅ Removed cache file: {file_path}")
    
    # Create sample configuration files
    create_sample_configs()
    
    print("\n🎉 Project cleanup completed!")
    print("📋 Next steps:")
    print("1. Review the cleaned project")
    print("2. Initialize git repository: git init")
    print("3. Add files: git add .")
    print("4. Commit: git commit -m 'Initial commit'")
    print("5. Create repository on GitHub")
    print("6. Push: git remote add origin <your-repo-url>")
    print("7. Push: git push -u origin main")

def create_sample_configs():
    """Create sample configuration files for GitHub."""
    
    # Sample config.json
    sample_config = {
        "app_name": "USB HawkEye",
        "version": "1.0.0",
        "email_settings": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "use_tls": True,
            "sender_email": "your-email@gmail.com",
            "sender_password": "your-app-password"
        },
        "alert_settings": {
            "email_alerts": True,
            "sms_alerts": False,
            "device_insertion": True,
            "device_removal": True,
            "threat_detection": True
        },
        "ui_settings": {
            "theme": "cyberpunk",
            "animations": True,
            "session_timeout": 30
        }
    }
    
    with open('config_sample.json', 'w') as f:
        json.dump(sample_config, f, indent=4)
    print("✅ Created sample config: config_sample.json")
    
    # Sample users.json
    sample_users = {
        "users": [
            {
                "username": "admin",
                "email": "admin@example.com",
                "password_hash": "sample_hash_here",
                "role": "admin",
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]
    }
    
    with open('users_sample.json', 'w') as f:
        json.dump(sample_users, f, indent=4)
    print("✅ Created sample users: users_sample.json")

if __name__ == "__main__":
    cleanup_project() 