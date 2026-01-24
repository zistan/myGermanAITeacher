# Deployment Checklist

Use this checklist to ensure all deployment steps are completed correctly.

## Pre-Deployment

- [ ] Ubuntu server is accessible via SSH
- [ ] You have sudo/root access
- [ ] Server has minimum 2GB RAM and 20GB disk space
- [ ] You have your Anthropic API key ready
- [ ] Domain name is configured (if using one)

## Step 1: Server Setup

- [ ] SSH into server: `ssh user@your-server-ip`
- [ ] Update system: `sudo apt update && sudo apt upgrade -y`
- [ ] Add Python 3.11 repository (deadsnakes PPA):
  ```bash
  sudo apt install -y software-properties-common
  sudo add-apt-repository ppa:deadsnakes/ppa -y
  sudo apt update
  ```
- [ ] Install dependencies:
  ```bash
  sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip postgresql postgresql-contrib nginx git curl
  ```
- [ ] Verify installations:
  - [ ] Python 3.11+: `python3.11 --version`
  - [ ] PostgreSQL: `psql --version`
  - [ ] Nginx: `nginx -v`

## Step 2: Database Configuration

- [ ] Switch to postgres user: `sudo -u postgres psql`
- [ ] Create database: `CREATE DATABASE german_learning;`
- [ ] Create user with strong password:
  ```sql
  CREATE USER german_app_user WITH PASSWORD 'your_secure_password';
  ```
- [ ] Grant privileges:
  ```sql
  GRANT ALL PRIVILEGES ON DATABASE german_learning TO german_app_user;
  ```
- [ ] Exit psql: `\q`
- [ ] Test connection:
  ```bash
  psql -U german_app_user -d german_learning -h localhost -W
  ```

## Step 3: Application Setup

- [ ] Create app directory:
  ```bash
  sudo mkdir -p /opt/german-learning-app
  sudo chown $USER:$USER /opt/german-learning-app
  cd /opt/german-learning-app
  ```

- [ ] Transfer code to server (choose one method):
  - [ ] Git: `git clone <your-repo-url> .`
  - [ ] SCP: Copy from local to server
  - [ ] Rsync: Sync files from local

- [ ] Navigate to backend: `cd /opt/german-learning-app/backend`

- [ ] Create virtual environment:
  ```bash
  python3.11 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  ```

- [ ] Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Step 4: Environment Configuration

- [ ] Create .env file: `nano /opt/german-learning-app/backend/.env`
- [ ] Add required variables (use deploy/.env.production as template):
  - [ ] DATABASE_URL (with actual password)
  - [ ] ANTHROPIC_API_KEY
  - [ ] SECRET_KEY (generate with: `openssl rand -hex 32`)
  - [ ] Set DEBUG=False
  - [ ] Set ENVIRONMENT=production
  - [ ] Update CORS_ORIGINS with your domain
- [ ] Set permissions: `chmod 600 .env`

## Step 5: Database Migration & Seeding

- [ ] Activate venv: `source venv/bin/activate`
- [ ] Run migrations: `alembic upgrade head`
- [ ] Seed contexts: `python scripts/seed_contexts.py`
- [ ] Seed grammar: `python scripts/seed_grammar_data.py`
- [ ] Seed vocabulary: `python scripts/seed_vocabulary_data.py`
- [ ] Seed achievements: `python scripts/seed_achievements.py`

## Step 6: Test Application

- [ ] Start test server:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```
- [ ] Test health endpoint:
  ```bash
  curl http://your-server-ip:8000/api/health
  ```
- [ ] Expected response: `{"status": "healthy"}`
- [ ] Stop test server: `Ctrl+C`

## Step 7: Systemd Service Setup

- [ ] Copy service file:
  ```bash
  sudo cp /opt/german-learning-app/backend/deploy/german-learning.service /etc/systemd/system/
  ```
- [ ] Edit service file to replace placeholders:
  ```bash
  sudo nano /etc/systemd/system/german-learning.service
  ```
  - [ ] Replace `REPLACE_WITH_YOUR_USERNAME` with your username
- [ ] Reload systemd: `sudo systemctl daemon-reload`
- [ ] Enable service: `sudo systemctl enable german-learning`
- [ ] Start service: `sudo systemctl start german-learning`
- [ ] Check status: `sudo systemctl status german-learning`
- [ ] Verify it's running: `curl http://localhost:8000/api/health`

## Step 8: Nginx Configuration

- [ ] Copy nginx config:
  ```bash
  sudo cp /opt/german-learning-app/backend/deploy/nginx-german-learning.conf /etc/nginx/sites-available/german-learning
  ```
- [ ] Edit config to replace placeholders:
  ```bash
  sudo nano /etc/nginx/sites-available/german-learning
  ```
  - [ ] Replace `REPLACE_WITH_YOUR_DOMAIN` with your actual domain
- [ ] Create symbolic link:
  ```bash
  sudo ln -s /etc/nginx/sites-available/german-learning /etc/nginx/sites-enabled/
  ```
- [ ] Test nginx config: `sudo nginx -t`
- [ ] If test passes, reload: `sudo systemctl reload nginx`

## Step 9: Firewall Setup

- [ ] Enable UFW: `sudo ufw enable`
- [ ] Allow SSH: `sudo ufw allow OpenSSH`
- [ ] Allow HTTP/HTTPS: `sudo ufw allow 'Nginx Full'`
- [ ] Check status: `sudo ufw status`

## Step 10: SSL Setup (Optional but Recommended)

- [ ] Install certbot:
  ```bash
  sudo apt install -y certbot python3-certbot-nginx
  ```
- [ ] Obtain certificate:
  ```bash
  sudo certbot --nginx -d your-domain.com -d www.your-domain.com
  ```
- [ ] Test auto-renewal: `sudo certbot renew --dry-run`

## Step 11: Post-Deployment Verification

- [ ] Access API docs: `http://your-domain.com/docs`
- [ ] Check health endpoint: `curl http://your-domain.com/api/health`
- [ ] Create test user via API:
  ```bash
  curl -X POST http://your-domain.com/api/v1/auth/register \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"testpass123","full_name":"Test User"}'
  ```
- [ ] Login with test user:
  ```bash
  curl -X POST http://your-domain.com/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"testpass123"}'
  ```
- [ ] Test authenticated endpoint with token

## Step 12: Monitoring & Backups

- [ ] Set up log rotation (see DEPLOYMENT_GUIDE.md)
- [ ] Configure database backups (see DEPLOYMENT_GUIDE.md)
- [ ] Set up monitoring (optional)

## Security Checklist

- [ ] Strong PostgreSQL password set
- [ ] SECRET_KEY is randomly generated (not default)
- [ ] ANTHROPIC_API_KEY is kept secure
- [ ] .env file has 600 permissions
- [ ] DEBUG=False in production
- [ ] Firewall (UFW) is enabled
- [ ] SSL/HTTPS is configured
- [ ] PostgreSQL only accepts local connections
- [ ] Application runs as non-root user

## Troubleshooting

If something doesn't work:

1. **Check service logs:**
   ```bash
   sudo journalctl -u german-learning -n 50
   ```

2. **Check nginx logs:**
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

3. **Verify database connection:**
   ```bash
   psql -U german_app_user -d german_learning -h localhost -W
   ```

4. **Check if port is in use:**
   ```bash
   sudo lsof -i :8000
   ```

5. **Restart services:**
   ```bash
   sudo systemctl restart german-learning
   sudo systemctl restart nginx
   ```

## Common Issues

**Issue: Service won't start**
- Check logs: `sudo journalctl -u german-learning -xe`
- Verify .env file exists and has correct values
- Check venv path in service file

**Issue: Database connection failed**
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check DATABASE_URL in .env
- Test connection manually

**Issue: Nginx 502 Bad Gateway**
- Check if app is running: `sudo systemctl status german-learning`
- Verify port 8000 is listening: `sudo lsof -i :8000`
- Check nginx config: `sudo nginx -t`

**Issue: CORS errors**
- Update CORS_ORIGINS in .env with correct domain
- Restart service after .env changes

---

**Deployment Status**: _____ of _____ steps completed

**Deployment Date**: __________

**Deployed By**: __________

**Server IP/Domain**: __________
