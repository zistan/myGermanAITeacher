# Deployment Guide - German Learning Application

## Overview
This guide walks through deploying the German Learning Application backend on an Ubuntu server with:
- FastAPI (Python 3.11+)
- PostgreSQL 15+
- Uvicorn (ASGI server)
- Nginx (reverse proxy)
- Systemd (process management)

## Prerequisites

### Server Requirements
- Ubuntu 20.04 LTS or newer
- Minimum 2GB RAM
- 20GB disk space
- Root or sudo access
- Open ports: 80 (HTTP), 443 (HTTPS), 8000 (temporary testing)

### Local Requirements
- Git installed
- SSH access to Ubuntu server
- Your Anthropic API key

---

## Deployment Steps

### 1. Update System and Install Dependencies

SSH into your Ubuntu server:
```bash
ssh user@your-server-ip
```

Update system packages:
```bash
sudo apt update && sudo apt upgrade -y
```

Add deadsnakes PPA for Python 3.11 (required for Ubuntu):
```bash
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
```

Install Python 3.11 and required packages:
```bash
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip postgresql postgresql-contrib nginx git curl
```

Verify installations:
```bash
python3.11 --version  # Should be 3.11+
psql --version        # Should be PostgreSQL 12+ (15+ preferred)
nginx -v              # Should show nginx version
```

**Note**: If PostgreSQL 15 is not available in your Ubuntu version's default repos, you can use PostgreSQL 12+ or add the official PostgreSQL repository.

### 2. Configure PostgreSQL Database

Switch to postgres user and create database:
```bash
sudo -u postgres psql
```

In PostgreSQL shell, run:
```sql
-- Create database
CREATE DATABASE german_learning;

-- Create user with password (CHANGE THIS PASSWORD!)
CREATE USER german_app_user WITH PASSWORD 'your_secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE german_learning TO german_app_user;

-- Exit
\q
```

Test connection:
```bash
psql -U german_app_user -d german_learning -h localhost -W
# Enter password when prompted, then \q to exit
```

### 3. Set Up Application Directory

Create application directory:
```bash
sudo mkdir -p /opt/german-learning-app
sudo chown $USER:$USER /opt/german-learning-app
cd /opt/german-learning-app
```

### 4. Transfer Code to Server

**Option A: Using Git (Recommended)**
```bash
# If you have a Git repository
git clone https://github.com/yourusername/myGermanAITeacher.git .

# Or if pushing from local machine:
# On your local Windows machine, push to a Git repo first
# Then clone on the server
```

**Option B: Using SCP (from your Windows machine)**
```bash
# From Windows (using PowerShell or WSL):
scp -r C:\Users\zista\PycharmProjects\myGermanAITeacher\backend user@your-server-ip:/opt/german-learning-app/
```

**Option C: Using rsync (more efficient)**
```bash
# From Windows WSL or Git Bash:
rsync -avz --exclude='__pycache__' --exclude='*.pyc' --exclude='.env' \
  /mnt/c/Users/zista/PycharmProjects/myGermanAITeacher/backend/ \
  user@your-server-ip:/opt/german-learning-app/backend/
```

### 5. Set Up Python Virtual Environment

```bash
cd /opt/german-learning-app/backend

# Create virtual environment with Python 3.11
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create production `.env` file:
```bash
nano /opt/german-learning-app/backend/.env
```

Add the following content (UPDATE THE VALUES):
```bash
# Database
DATABASE_URL=postgresql://german_app_user:your_secure_password_here@localhost/german_learning

# AI Services
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here

# Security (GENERATE NEW SECRET KEY!)
SECRET_KEY=generate-a-long-random-secret-key-here-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=German Learning App
DEBUG=False
ENVIRONMENT=production
CORS_ORIGINS=http://your-domain.com,https://your-domain.com

# Server
HOST=0.0.0.0
PORT=8000
```

**Generate a secure SECRET_KEY:**
```bash
openssl rand -hex 32
# Copy the output and paste it as SECRET_KEY value
```

**Set proper permissions:**
```bash
chmod 600 /opt/german-learning-app/backend/.env
```

### 7. Run Database Migrations

```bash
cd /opt/german-learning-app/backend
source venv/bin/activate

# Run migrations
alembic upgrade head
```

### 8. Seed Initial Data

```bash
# Still in backend directory with venv activated
python scripts/seed_contexts.py
python scripts/seed_grammar_data.py
python scripts/seed_vocabulary_data.py
python scripts/seed_achievements.py
```

### 9. Test the Application

Test that the app runs:
```bash
cd /opt/german-learning-app/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

In another terminal or browser, test:
```bash
curl http://your-server-ip:8000/api/health
# Should return: {"status": "healthy"}
```

**Stop the test server with Ctrl+C**

### 10. Create Systemd Service

Create systemd service file:
```bash
sudo nano /etc/systemd/system/german-learning.service
```

Add the following content:
```ini
[Unit]
Description=German Learning Application
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=notify
User=your-username
Group=your-username
WorkingDirectory=/opt/german-learning-app/backend
Environment="PATH=/opt/german-learning-app/backend/venv/bin"
ExecStart=/opt/german-learning-app/backend/venv/bin/uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info \
    --access-log

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**IMPORTANT: Replace `your-username` with your actual username:**
```bash
whoami  # This shows your username
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable german-learning
sudo systemctl start german-learning
```

Check service status:
```bash
sudo systemctl status german-learning
```

View logs:
```bash
sudo journalctl -u german-learning -f
```

### 11. Configure Nginx Reverse Proxy

Create Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/german-learning
```

Add the following content:
```nginx
# HTTP configuration
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;  # UPDATE THIS

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Client body size (for file uploads if needed)
    client_max_body_size 10M;

    # API endpoints
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint (optional - bypass auth)
    location /api/health {
        proxy_pass http://127.0.0.1:8000;
        access_log off;
    }
}
```

Enable the site:
```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/german-learning /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# If test passes, reload Nginx
sudo systemctl reload nginx
```

### 12. Configure Firewall (UFW)

```bash
# Enable UFW
sudo ufw enable

# Allow SSH (IMPORTANT - don't lock yourself out!)
sudo ufw allow OpenSSH

# Allow HTTP and HTTPS
sudo ufw allow 'Nginx Full'

# Check status
sudo ufw status
```

### 13. Set Up SSL with Let's Encrypt (Optional but Recommended)

Install Certbot:
```bash
sudo apt install -y certbot python3-certbot-nginx
```

Obtain SSL certificate:
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Follow the prompts. Certbot will automatically:
- Obtain the certificate
- Modify your Nginx configuration
- Set up auto-renewal

Test auto-renewal:
```bash
sudo certbot renew --dry-run
```

### 14. Set Up Log Rotation

Create log rotation config:
```bash
sudo nano /etc/logrotate.d/german-learning
```

Add:
```
/var/log/german-learning/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload german-learning > /dev/null 2>&1 || true
    endscript
}
```

Create log directory:
```bash
sudo mkdir -p /var/log/german-learning
sudo chown www-data:www-data /var/log/german-learning
```

---

## Post-Deployment Tasks

### 1. Create First User Account

Use the API to register:
```bash
curl -X POST http://your-domain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-secure-password",
    "full_name": "Your Name"
  }'
```

### 2. Verify All Endpoints

Check API documentation:
- Swagger UI: http://your-domain.com/docs
- ReDoc: http://your-domain.com/redoc

### 3. Set Up Monitoring (Optional)

Monitor service status:
```bash
# Check if service is running
sudo systemctl status german-learning

# View recent logs
sudo journalctl -u german-learning -n 100

# Follow logs in real-time
sudo journalctl -u german-learning -f
```

### 4. Set Up Backups

Create backup script:
```bash
nano ~/backup-german-learning.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/home/$USER/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U german_app_user german_learning > $BACKUP_DIR/db_backup_$DATE.sql

# Backup application files
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz /opt/german-learning-app/backend

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

Make executable and add to crontab:
```bash
chmod +x ~/backup-german-learning.sh

# Run daily at 2 AM
crontab -e
# Add: 0 2 * * * /home/your-username/backup-german-learning.sh
```

---

## Troubleshooting

### Service Won't Start
```bash
# Check logs
sudo journalctl -u german-learning -n 50

# Check if port 8000 is in use
sudo lsof -i :8000

# Check permissions
ls -la /opt/german-learning-app/backend
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U german_app_user -d german_learning -h localhost -W

# Check DATABASE_URL in .env
cat /opt/german-learning-app/backend/.env | grep DATABASE_URL
```

### Nginx Issues
```bash
# Test configuration
sudo nginx -t

# Check logs
sudo tail -f /var/log/nginx/error.log

# Restart Nginx
sudo systemctl restart nginx
```

### Check Application Logs
```bash
# View all logs
sudo journalctl -u german-learning -n 100

# Follow logs
sudo journalctl -u german-learning -f

# Filter by date
sudo journalctl -u german-learning --since "1 hour ago"
```

---

## Updating the Application

When you need to update the code:

```bash
cd /opt/german-learning-app/backend

# Pull latest changes (if using Git)
git pull origin master

# Activate virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Run new migrations
alembic upgrade head

# Restart service
sudo systemctl restart german-learning

# Check status
sudo systemctl status german-learning
```

---

## Security Checklist

- [ ] Strong PostgreSQL password set
- [ ] SECRET_KEY is randomly generated (not default)
- [ ] ANTHROPIC_API_KEY is kept secret
- [ ] .env file has 600 permissions
- [ ] DEBUG=False in production
- [ ] Firewall (UFW) is enabled
- [ ] SSL/HTTPS is configured
- [ ] Regular backups are scheduled
- [ ] PostgreSQL only accepts local connections
- [ ] Application runs as non-root user
- [ ] Logs are rotated

---

## Useful Commands

```bash
# Service management
sudo systemctl start german-learning
sudo systemctl stop german-learning
sudo systemctl restart german-learning
sudo systemctl status german-learning

# View logs
sudo journalctl -u german-learning -f

# Database access
psql -U german_app_user -d german_learning -h localhost

# Nginx management
sudo systemctl reload nginx
sudo nginx -t

# Check disk space
df -h

# Check memory usage
free -h

# Monitor processes
htop
```

---

## Performance Tuning

### Uvicorn Workers
The service is configured with 4 workers. Adjust based on your server:
```bash
# Rule of thumb: (2 x CPU cores) + 1
# Edit systemd service file
sudo nano /etc/systemd/system/german-learning.service

# Change --workers value
# Then reload
sudo systemctl daemon-reload
sudo systemctl restart german-learning
```

### PostgreSQL Configuration
For production, tune PostgreSQL settings:
```bash
sudo nano /etc/postgresql/15/main/postgresql.conf

# Suggested changes (adjust based on RAM):
shared_buffers = 256MB          # 25% of RAM
effective_cache_size = 1GB      # 50-75% of RAM
maintenance_work_mem = 64MB
work_mem = 4MB
```

After changes:
```bash
sudo systemctl restart postgresql
```

---

## Next Steps

1. **Frontend Deployment**: When Phase 7 is complete, deploy React frontend
2. **Monitoring**: Set up Prometheus/Grafana for metrics
3. **Error Tracking**: Integrate Sentry or similar
4. **CDN**: Use Cloudflare for static assets (future frontend)
5. **Load Balancing**: If scaling beyond one server

---

**Deployment Complete!** Your German Learning Application is now live at http://your-domain.com
