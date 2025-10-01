#!/usr/bin/env python3

import os
import sys
import time
import subprocess
from datetime import datetime


try:
    from backup import backup
    from file import analyze_log
    from health import check_application
    from system import check_cpu, check_memory, check_disk, check_processes
    
    print("Successfully imported all modules")
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def print_header(title):
    """Print a formatted header for each section"""
    print("\n" + "=" * 50)
    print(f" {title}")
    print("=" * 50)

def run_system_checks():
    """Run all system health checks"""
    print_header("SYSTEM HEALTH CHECKS")
    check_cpu()
    check_memory()
    check_disk()
    check_processes()

def run_application_check():
    """Run application health check"""
    print_header("APPLICATION HEALTH CHECK")
    status = check_application()
    print(f"Application Status: {'UP' if status else 'DOWN'}")

def run_backup():
    """Run backup process"""
    print_header("BACKUP PROCESS")
    success = backup()
    print(f"Backup Status: {'SUCCESS' if success else 'FAILED'}")

def run_log_analysis():
    """Run log file analysis"""
    print_header("LOG FILE ANALYSIS")
    # Check if the default log file exists, otherwise skip
    log_file = "/var/log/nginx/access.log"
    if not os.path.exists(log_file):
        print(f"Warning: {log_file} not found. Log analysis skipped.")
        return

    if os.path.exists(log_file):
        analyze_log(log_file)
    else:
        print(f"Error: Log file {log_file} does not exist.")

def check_log_setup():
    """Check if the required log files exist and have right permissions"""
    required_logs = [
        "/var/log/backup_report.log",
        "/var/log/app_health.log", 
        "/var/log/system_health.log",
        "/var/log/nginx/access.log"
    ]
    
    missing_logs = [log for log in required_logs if not os.path.exists(log)]
    
    if missing_logs:
        print("\nWARNING: The following required log files are missing:")
        for log in missing_logs:
            print(f"  - {log}")
        
        # Auto-run setup script if available
        setup_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setup_logs.sh")
        if os.path.exists(setup_script):
            print("\nAttempting to run setup script automatically...")
            try:
                subprocess.run(["sudo", "bash", setup_script], check=True)
                print("\nLog setup completed. Continuing...")
            except subprocess.CalledProcessError:
                print("\nError running the setup script. Some functions may not work properly.")
                print("Continuing with available logs...")
                return False
        else:
            print(f"\nSetup script not found. Some functions may not work properly.")
            return False
    
    return True

def main():
    """Main function to run all components in a continuous loop"""
    print_header(f"SYSTEM UTILITY - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if logs are set up once at startup
    if not check_log_setup():
        print("Some log files are missing. Continuing with available functionality...")
    
    print("\nStarting continuous monitoring loop...")
    print("Press Ctrl+C to stop the monitoring")
    
    cycle_count = 0
    
    while True:
        try:
            cycle_count += 1
            print(f"\n{'='*60}")
            print(f" MONITORING CYCLE #{cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}")
            
            # Run all checks automatically
            run_system_checks()
            time.sleep(2)  # Brief pause between checks
            
            run_application_check()
            time.sleep(2)
            
            run_log_analysis()
            time.sleep(2)
            
            # Skip backup in loop mode to avoid continuous backup attempts
            print_header("BACKUP STATUS")
            print("Backup skipped in monitoring mode (would run continuously)")
            
            print(f"\n{'='*60}")
            print(f" CYCLE #{cycle_count} COMPLETED")
            print(f"{'='*60}")
            
            # Wait 10 seconds before next cycle
            time.sleep(10)
            
        except KeyboardInterrupt:
            print(f"\n\nMonitoring stopped after {cycle_count} cycles")
            print("Exiting gracefully...")
            break
        except Exception as e:
            print(f"\nError in monitoring cycle #{cycle_count}: {e}")
            print("Continuing to next cycle...")
            time.sleep(10)  

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")