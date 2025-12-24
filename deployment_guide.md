# AWS Deployment Guide: CORTEXA (3-Server Load Balanced)

This guide walks you through deploying CORTEXA on AWS using **3 Ubuntu EC2 Instances** and **Nginx** as a Load Balancer + Reverse Proxy.

## 🏗️ Architecture (3 Servers)

*   **Server 1 (Gateway)**: `t3.micro`
    *   **Role**: Load Balancer (Nginx) + Frontend Host.
    *   **Public Access**: Ports 80 (HTTP), 443 (HTTPS), 22 (SSH).
*   **Server 2 (App Node)**: `t3.medium`
    *   **Role**: Backend API + Database (PostgreSQL).
    *   **Public Access**: None (Private Only ideally, or Restricted SSH).
    *   **Private Access**: Port 8000 (API), 5432 (DB).
*   **Server 3 (App Node)**: `t3.medium`
    *   **Role**: Backend API (Replica).
    *   **Public Access**: None.
    *   **Private Access**: Port 8000 (API).

---

## 🚀 Step 1: Provision Infrastructure

1.  Launch **3 EC2 Instances** (Ubuntu 24.04 LTS).
2.  **Security Groups**:
    *   **Gateway SG**: Allow Inbound HTTP (80), HTTPS (443), SSH (22).
    *   **Internal SG** (for Servers 2 & 3): Allow Inbound TCP 8000 and 5432 **ONLY from Gateway SG Group ID**.

## 🚀 Step 2: Configure Application Servers (Servers 2 & 3)

**Perform these steps on BOTH Server 2 and Server 3.**

1.  **System Setup**:
    ```bash
    sudo apt update && sudo apt install -y python3-venv python3-pip git postgresql-client
    ```

2.  **Clone Code**:
    ```bash
    git clone https://github.com/PS-04-emmanuel/CORTEXA.git
    cd CORTEXA/backend
    ```

3.  **Setup Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install gunicorn
    ```

4.  **Configure Env**:
    *   Create `.env` file from the example.
    *   **Server 2 ONLY**: Install PostgreSQL locally if not using RDS.
        *   `sudo apt install postgresql postgresql-contrib`
        *   Create DB and User.
    *   **Both Servers**: Update `.env` to point `DATABASE_URL` to Server 2's Private IP.

5.  **Setup Systemd Service**:
    *   Copy the service file we generated:
    ```bash
    sudo cp ../infra/systemd/cortexa-backend.service /etc/systemd/system/
    sudo systemctl start cortexa-backend
    sudo systemctl enable cortexa-backend
    ```

---

## 🚀 Step 3: Configure Gateway Server (Server 1)

1.  **Install Nginx & Node.js**:
    ```bash
    sudo apt update
    sudo apt install -y nginx nodejs npm
    ```

2.  **Build Frontend**:
    ```bash
    git clone https://github.com/PS-04-emmanuel/CORTEXA.git
    cd CORTEXA/frontend
    npm install
    # Update .env to point to Public IP if needed, or /api relative path
    npm run build
    ```

3.  **Deploy Static Files**:
    ```bash
    sudo mkdir -p /var/www/cortexa/frontend
    sudo cp -r dist/* /var/www/cortexa/frontend/
    ```

4.  **Configure Nginx Load Balancer**:
    *   Edit `/etc/nginx/nginx.conf` (or `/etc/nginx/sites-available/default`).
    *   Paste the content of `infra/nginx.conf`.
    *   **IMPORTANT**: Update `<PRIVATE_IP_SERVER_2>` and `<PRIVATE_IP_SERVER_3>` with the actual AWS Private IPs.

5.  **Restart Nginx**:
    ```bash
    sudo nginx -t
    sudo systemctl restart nginx
    ```

## ✅ Verification

1.  Open your browser to the **Public IP of Server 1**.
2.  The Frontend should load.
3.  Any API request (e.g., Login) will count as a connection.
4.  Nginx will round-robin these requests between Server 2 and Server 3.
