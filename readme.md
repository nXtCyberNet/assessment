# DevOps & Scripting Project Readme

## Problem Statement 1: Containerisation and Deployment of Wisecow Application on Kubernetes

**Title:** Containerisation and Deployment of Wisecow Application on Kubernetes  
**Project Repository:** [https://github.com/nyrahul/wisecow](https://github.com/nyrahul/wisecow)  
**Objective:** Containerize and deploy the Wisecow application on a Kubernetes environment (e.g., Kind/Minikube) with secure TLS communication.  

### Approach:
- Created a Dockerfile for building the Wisecow application container image.  
- Added self-signed SSL for TLS communication (local environment; no static IP available for certbot HTTP-01 authentication).  
- Implemented CI/CD in a local Kubernetes environment using a custom GitHub Actions runner.  
- Used the Kubernetes API to rollout pods directly because `kubectl` installation in the runner was challenging.  

### Deliverables:
- Dockerfile for the Wisecow application  
- Kubernetes manifest files (Deployment, Service, etc.)  
- GitHub Actions workflow file for CI/CD  
- Runner deployment files and RHDS authentication & registration file  

---

## Problem Statement 2: Automation Scripts

**Title:** Linux System Automation Scripts  
**Objective:** Chose the following two objectives:  
1. System Health Monitoring Script  
2. Application Health Checker  

### Approach:
- Developed Python scripts to monitor system metrics (CPU, memory, disk space, running processes) and check application uptime/status via HTTP status codes.  
- Created a shell script to set required permissions and configure the setup.  
- Added a systemd service file for continuous running of scripts in the background.  

### Deliverables:
- Python scripts for monitoring and application health check  
- Shell script for permissions and setup  
- `tool.service` systemd file  

---

## Problem Statement 3: KubeArmor Policy Implementation

**Title:** Security Policy Enforcement with KubeArmor  
**Objective:** Implement a zero-trust KubeArmor policy for workload security  

### Approach:
- **Not implemented:** Minikube environment does not support the KubeArmor addon, so policy deployment was not possible.  

### Deliverables:
- N/A

