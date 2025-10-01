#!/bin/bash

# Setup script for log files with proper permissions

# Get the actual user (not root when using sudo)
if [ ! -z "$SUDO_USER" ]; then
    USER="$SUDO_USER"
else
    USER=$(whoami)
fi
echo "Setting up log files for user: $USER"

# Create log directories
sudo mkdir -p /var/log/nginx

# Create and set permissions for log files
LOG_FILES=(
    "/var/log/backup_report.log"
    "/var/log/app_health.log"
    "/var/log/system_health.log"
    "/var/log/nginx/access.log"
)

for log_file in "${LOG_FILES[@]}"; do
    echo "Creating and setting up: $log_file"
    sudo touch "$log_file"
    sudo chown "$USER:$USER" "$log_file"
    sudo chmod 664 "$log_file"
done

# Also set write permissions on the parent directories
sudo chmod 775 /var/log
sudo chmod 775 /var/log/nginx

# Add sample content to nginx access log
echo "Adding sample content to nginx access log..."
cat > /tmp/nginx_sample.log << 'EOL'
192.168.1.10 - - [01/Oct/2025:10:10:10 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
192.168.1.20 - - [01/Oct/2025:10:11:15 +0000] "GET /about.html HTTP/1.1" 200 2345 "-" "Mozilla/5.0"
192.168.1.30 - - [01/Oct/2025:10:12:20 +0000] "GET /contact.html HTTP/1.1" 200 3456 "-" "Mozilla/5.0"
192.168.1.10 - - [01/Oct/2025:10:13:25 +0000] "GET /products.html HTTP/1.1" 200 4567 "-" "Mozilla/5.0"
192.168.1.40 - - [01/Oct/2025:10:14:30 +0000] "GET /services.html HTTP/1.1" 200 5678 "-" "Mozilla/5.0"
192.168.1.50 - - [01/Oct/2025:10:15:35 +0000] "GET /nonexistent.html HTTP/1.1" 404 789 "-" "Mozilla/5.0"
192.168.1.60 - - [01/Oct/2025:10:16:40 +0000] "GET /another-missing.html HTTP/1.1" 404 789 "-" "Mozilla/5.0"
192.168.1.10 - - [01/Oct/2025:10:17:45 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
192.168.1.20 - - [01/Oct/2025:10:18:50 +0000] "GET /about.html HTTP/1.1" 200 2345 "-" "Mozilla/5.0"
192.168.1.30 - - [01/Oct/2025:10:19:55 +0000] "GET /contact.html HTTP/1.1" 200 3456 "-" "Mozilla/5.0"
EOL

# Copy sample content to actual log file
sudo cp /tmp/nginx_sample.log /var/log/nginx/access.log
sudo chown "$USER:$USER" /var/log/nginx/access.log
sudo chmod 664 /var/log/nginx/access.log
rm /tmp/nginx_sample.log

# Create backup data directory
echo "Creating backup data directory..."
sudo mkdir -p /home/user/data
sudo chown "$USER:$USER" /home/user/data
sudo chmod 755 /home/user/data
echo "Sample data file for backup testing" | sudo tee /home/user/data/sample.txt > /dev/null
sudo chown "$USER:$USER" /home/user/data/sample.txt

# Make main.py executable
echo "Making main.py executable..."
chmod +x /home/cybernet/tranee/problem2/main.py

# Install dependencies if pip is available
if command -v pip3 &> /dev/null; then
    echo "Installing required Python packages..."
    pip3 install --user psutil requests 2>/dev/null || echo "Note: Install psutil and requests manually if needed"
fi

echo ""
echo "Log setup completed!"
echo "Log files created with proper permissions:"
for log_file in "${LOG_FILES[@]}"; do
    echo "  - $log_file"
done
echo ""
echo "You can now run: python3 main.py"