# Deployment Files

This directory contains all files needed to deploy the German Learning Application to an Ubuntu server.

## Contents

### 1. **DEPLOYMENT_CHECKLIST.md**
Step-by-step checklist to ensure all deployment tasks are completed.
- Use this to track your deployment progress
- Check off each item as you complete it
- Includes troubleshooting section

### 2. **setup-server.sh**
Automated setup script for initial server configuration.
```bash
# On your Ubuntu server:
chmod +x setup-server.sh
./setup-server.sh
```

This script:
- Updates system packages
- Installs Python 3.11, PostgreSQL, Nginx, and other dependencies
- Configures UFW firewall
- Creates application directory
- Sets up PostgreSQL database (optional)
- Generates SECRET_KEY

### 3. **german-learning.service**
Systemd service file for running the application as a system service.

**To use:**
```bash
# Copy to systemd
sudo cp german-learning.service /etc/systemd/system/

# Edit to replace REPLACE_WITH_YOUR_USERNAME
sudo nano /etc/systemd/system/german-learning.service

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable german-learning
sudo systemctl start german-learning
```

### 4. **nginx-german-learning.conf**
Nginx reverse proxy configuration.

**To use:**
```bash
# Copy to nginx sites-available
sudo cp nginx-german-learning.conf /etc/nginx/sites-available/german-learning

# Edit to replace REPLACE_WITH_YOUR_DOMAIN
sudo nano /etc/nginx/sites-available/german-learning

# Enable site
sudo ln -s /etc/nginx/sites-available/german-learning /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### 5. **.env.production**
Template for production environment variables.

**To use:**
```bash
# Copy to backend directory
cp .env.production /opt/german-learning-app/backend/.env

# Edit with actual values
nano /opt/german-learning-app/backend/.env

# Secure the file
chmod 600 /opt/german-learning-app/backend/.env
```

## Quick Start

### Option 1: Automated Setup (Recommended)

1. **On your local machine**, transfer files to server:
```bash
# Create deploy directory on server
ssh user@your-server-ip "mkdir -p ~/deploy"

# Copy deployment files
scp -r backend/deploy/* user@your-server-ip:~/deploy/

# Or use git if you have a repository
```

2. **On your Ubuntu server**, run setup script:
```bash
cd ~/deploy
chmod +x setup-server.sh
./setup-server.sh
```

3. Follow the prompts to configure database and firewall

4. Transfer your application code:
```bash
# Option A: Git clone
cd /opt/german-learning-app
git clone <your-repo-url> .

# Option B: SCP from local
# (From local machine)
scp -r backend/* user@your-server-ip:/opt/german-learning-app/backend/
```

5. Continue with manual steps (virtual environment, migrations, etc.)

### Option 2: Manual Setup

Follow the detailed instructions in:
- `../../docs/DEPLOYMENT_GUIDE.md` (comprehensive guide)
- `DEPLOYMENT_CHECKLIST.md` (step-by-step checklist)

## File Transfer Methods

### Method 1: Git (Recommended)
```bash
cd /opt/german-learning-app
git clone https://github.com/yourusername/myGermanAITeacher.git .
```

### Method 2: SCP (from Windows)
```bash
# From PowerShell or WSL on Windows:
scp -r C:\Users\zista\PycharmProjects\myGermanAITeacher\backend user@server-ip:/opt/german-learning-app/
```

### Method 3: Rsync (more efficient)
```bash
# From WSL or Git Bash on Windows:
rsync -avz --exclude='__pycache__' --exclude='*.pyc' --exclude='.env' \
  /mnt/c/Users/zista/PycharmProjects/myGermanAITeacher/backend/ \
  user@server-ip:/opt/german-learning-app/backend/
```

## Configuration Values Needed

Before deployment, gather these values:

1. **Database Password**: Strong password for PostgreSQL user
2. **Anthropic API Key**: Your API key from Anthropic
3. **Secret Key**: Generate with `openssl rand -hex 32`
4. **Domain Name**: Your domain (if using one)
5. **Server IP**: Your Ubuntu server IP address

## Post-Deployment

After deployment is complete:

1. **Test the API:**
```bash
curl http://your-domain.com/api/health
curl http://your-domain.com/docs
```

2. **Create first user:**
```bash
curl -X POST http://your-domain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","password":"yourpass","full_name":"Your Name"}'
```

3. **Monitor logs:**
```bash
sudo journalctl -u german-learning -f
```

4. **Set up backups** (see DEPLOYMENT_GUIDE.md)

## Troubleshooting

### Service won't start
```bash
sudo journalctl -u german-learning -xe
```

### Database connection issues
```bash
sudo systemctl status postgresql
psql -U german_app_user -d german_learning -h localhost -W
```

### Nginx issues
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

### Check port 8000
```bash
sudo lsof -i :8000
```

## Security Reminders

- [ ] Never commit .env files with real credentials
- [ ] Use strong, unique passwords
- [ ] Keep ANTHROPIC_API_KEY secure
- [ ] Set .env file permissions to 600
- [ ] Set DEBUG=False in production
- [ ] Enable firewall (UFW)
- [ ] Configure SSL/HTTPS
- [ ] Regular backups

## Support

For detailed deployment instructions, see:
- **Full Guide**: `../../docs/DEPLOYMENT_GUIDE.md`
- **Checklist**: `DEPLOYMENT_CHECKLIST.md`
- **Project Documentation**: `../../.claude/CLAUDE.md`

## Architecture

```
                                    ┌─────────────────┐
                                    │   Users/API     │
                                    │    Clients      │
                                    └────────┬────────┘
                                             │
                                    ┌────────▼────────┐
                                    │  Nginx :80/443  │
                                    │ Reverse Proxy   │
                                    └────────┬────────┘
                                             │
                                    ┌────────▼────────┐
                                    │ Uvicorn :8000   │
                                    │   FastAPI App   │
                                    └────────┬────────┘
                                             │
                         ┌───────────────────┼───────────────────┐
                         │                   │                   │
                ┌────────▼────────┐ ┌────────▼────────┐ ┌───────▼────────┐
                │   PostgreSQL    │ │   Anthropic     │ │   File System  │
                │    Database     │ │   Claude API    │ │     (logs)     │
                └─────────────────┘ └─────────────────┘ └────────────────┘
```

## Next Steps After Deployment

1. **Phase 7: Frontend Development**
   - React + TypeScript + Vite
   - Connect to deployed backend API
   - Deploy frontend (static hosting or same server)

2. **Monitoring & Maintenance**
   - Set up monitoring (optional: Prometheus, Grafana)
   - Configure automated backups
   - Set up error tracking (optional: Sentry)
   - Regular security updates

3. **Scaling Considerations**
   - Add more Uvicorn workers if needed
   - PostgreSQL connection pooling
   - Redis for caching (future enhancement)
   - Load balancer if multiple servers

---

**Last Updated**: 2026-01-17
**For**: German Learning Application v1.0 (Phase 6 Complete)
