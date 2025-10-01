#!/usr/bin/env python3
import psutil
import logging
from datetime import datetime

# ================================
# Configuration
# ================================
CPU_THRESHOLD = 80        # in %
MEMORY_THRESHOLD = 80     # in %
DISK_THRESHOLD = 80       # in %
PROCESS_THRESHOLD = 300   # max number of processes

LOG_FILE = "/var/log/system_health.log"

# ================================
# Logging setup
# ================================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log_alert(message):
    print(f"[ALERT] {message}")
    logging.warning(message)

def log_info(message):
    print(f"[INFO] {message}")
    logging.info(message)

# ================================
# System health checks
# ================================
def check_cpu():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        log_alert(f"High CPU usage detected: {cpu_usage}%")
    else:
        log_info(f"CPU usage: {cpu_usage}%")

def check_memory():
    memory = psutil.virtual_memory()
    if memory.percent > MEMORY_THRESHOLD:
        log_alert(f"High Memory usage detected: {memory.percent}%")
    else:
        log_info(f"Memory usage: {memory.percent}%")

def check_disk():
    disk = psutil.disk_usage('/')
    if disk.percent > DISK_THRESHOLD:
        log_alert(f"High Disk usage detected: {disk.percent}%")
    else:
        log_info(f"Disk usage: {disk.percent}%")

def check_processes():
    processes = len(psutil.pids())
    if processes > PROCESS_THRESHOLD:
        log_alert(f"Too many running processes: {processes}")
    else:
        log_info(f"Running processes: {processes}")

# ================================
# Main function
# ================================
def main():
    log_info("===== System Health Check Started =====")
    check_cpu()
    check_memory()
    check_disk()
    check_processes()
    log_info("===== System Health Check Completed =====\n")

if __name__ == "__main__":
    main()
