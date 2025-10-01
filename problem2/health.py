#!/usr/bin/env python3
import requests
import logging
import time

# ================================
# Configuration
# ================================
URL = "http://localhost:8080"   # Application URL
CHECK_INTERVAL = 30             # seconds between checks
LOG_FILE = "/var/log/app_health.log"

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
# Health Check Function
# ================================
def check_application():
    try:
        response = requests.get(URL, timeout=5)
        if response.status_code == 200:
            log_info(f"Application is UP ✅ ({response.status_code})")
            return True
        else:
            log_error(f"Application is DOWN ❌ (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        log_error(f"Application is DOWN ❌ (Error: {e})")
        return False


