#!/usr/bin/env python3
import os
import subprocess
import logging
from datetime import datetime

# ================================
# Configuration
# ================================
SOURCE_DIR = "/home/user/data"         # Local directory to backup
REMOTE_USER = "username"               # Remote server username
REMOTE_HOST = "192.168.1.100"          # Remote server IP or hostname
REMOTE_DIR = "/home/username/backup"   # Remote backup directory

LOG_FILE = "/var/log/backup_report.log"

# ================================
# Logging Setup
# ================================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log_info(message):
    print(f"[INFO] {message}")
    logging.info(message)

def log_error(message):
    print(f"[ERROR] {message}")
    logging.error(message)

# ================================
# Backup Function
# ================================
def backup():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    remote_path = f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_DIR}/backup_{timestamp}"

    log_info(f"Starting backup of {SOURCE_DIR} to {remote_path}")

    try:
        # rsync command for efficient transfer
        result = subprocess.run(
            ["rsync", "-avz", SOURCE_DIR, remote_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        log_info(f"Backup successful! {SOURCE_DIR} → {remote_path}")
        return True

    except subprocess.CalledProcessError as e:
        log_error(f"Backup failed: {e.stderr.decode('utf-8')}")
        return False


