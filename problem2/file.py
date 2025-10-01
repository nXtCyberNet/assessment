from collections import Counter
import sys

LOG_FILE = "/var/log/nginx/access.log"     
TOP_N = 10  

def analyze_log(file_path):
    ip_counter = Counter()
    page_counter = Counter()
    error_404_count = 0
    total_requests = 0

    with open(file_path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 9:
                continue  

            ip = parts[0]
            status = parts[8]  
            url = parts[6] if len(parts) > 6 else "-"

            total_requests += 1
            ip_counter[ip] += 1
            page_counter[url] += 1

            if status == "404":
                error_404_count += 1

    print("\n===== Web Server Log Analysis Report =====")
    print(f"Total Requests: {total_requests}")
    print(f"Total 404 Errors: {error_404_count}\n")

    print(f"Top {TOP_N} Requested Pages:")
    for page, count in page_counter.most_common(TOP_N):
        print(f"{page}: {count} requests")

    print(f"\nTop {TOP_N} IP Addresses:")
    for ip, count in ip_counter.most_common(TOP_N):
        print(f"{ip}: {count} requests")

    print("==========================================\n")
