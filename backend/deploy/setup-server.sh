#!/bin/bash

# German Learning Application - Server Setup Script
# This script automates the initial server setup on Ubuntu
# Run this script on your Ubuntu server after SSH login

set -e  # Exit on error

echo "=========================================="
echo "German Learning App - Server Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then
   echo -e "${RED}ERROR: Please do not run this script as root${NC}"
   exit 1
fi

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Step 1: Update system
echo "Step 1: Updating system packages..."
sudo apt update
sudo apt upgrade -y
print_status "System updated"

# Step 2: Install dependencies
echo ""
echo "Step 2: Installing dependencies..."
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    postgresql \
    postgresql-contrib \
    nginx \
    git \
    curl \
    htop \
    ufw

print_status "Dependencies installed"

# Verify installations
echo ""
echo "Verifying installations..."
python3.11 --version
psql --version
nginx -v
print_status "All tools installed successfully"

# Step 3: Configure firewall
echo ""
echo "Step 3: Configuring firewall..."
read -p "Do you want to configure UFW firewall? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo ufw allow OpenSSH
    sudo ufw allow 'Nginx Full'
    sudo ufw --force enable
    print_status "Firewall configured"
else
    print_warning "Skipping firewall configuration"
fi

# Step 4: Create application directory
echo ""
echo "Step 4: Creating application directory..."
APP_DIR="/opt/german-learning-app"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR
print_status "Created directory: $APP_DIR"

# Step 5: PostgreSQL setup
echo ""
echo "Step 5: PostgreSQL database setup..."
read -p "Do you want to configure PostgreSQL database now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    DB_NAME="german_learning"
    DB_USER="german_app_user"

    echo "Enter a strong password for database user '$DB_USER':"
    read -s DB_PASSWORD
    echo
    echo "Confirm password:"
    read -s DB_PASSWORD_CONFIRM
    echo

    if [ "$DB_PASSWORD" != "$DB_PASSWORD_CONFIRM" ]; then
        print_error "Passwords do not match!"
        exit 1
    fi

    # Create database and user
    sudo -u postgres psql <<EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\q
EOF

    print_status "Database '$DB_NAME' and user '$DB_USER' created"

    # Save database URL to a temp file
    echo "DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost/$DB_NAME" > /tmp/db_config.txt
    print_status "Database URL saved to /tmp/db_config.txt (use this in .env file)"
else
    print_warning "Skipping database configuration"
fi

# Step 6: Generate SECRET_KEY
echo ""
echo "Step 6: Generating SECRET_KEY..."
SECRET_KEY=$(openssl rand -hex 32)
echo "SECRET_KEY=$SECRET_KEY" > /tmp/secret_key.txt
print_status "SECRET_KEY generated and saved to /tmp/secret_key.txt"

# Step 7: Summary
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Transfer your code to: $APP_DIR"
echo "2. Create .env file with:"
if [ -f /tmp/db_config.txt ]; then
    echo "   - Database URL: $(cat /tmp/db_config.txt)"
fi
if [ -f /tmp/secret_key.txt ]; then
    echo "   - Secret Key: $(cat /tmp/secret_key.txt)"
fi
echo "   - ANTHROPIC_API_KEY: <your-api-key>"
echo "3. Create virtual environment: cd $APP_DIR/backend && python3.11 -m venv venv"
echo "4. Install dependencies: source venv/bin/activate && pip install -r requirements.txt"
echo "5. Run migrations: alembic upgrade head"
echo "6. Seed data: Run seed scripts"
echo "7. Configure systemd service"
echo "8. Configure nginx"
echo ""
echo "Detailed instructions: See DEPLOYMENT_GUIDE.md"
echo ""

# Cleanup temp files after showing them
read -p "Press Enter to clear temporary credential files..."
rm -f /tmp/db_config.txt /tmp/secret_key.txt
print_status "Temporary files cleared"

echo ""
echo "Server setup complete! Follow the deployment guide for remaining steps."
