#!/bin/bash

# Crypto Streaming Pipeline Setup Script
# This script automates the local development setup

set -e

echo "🚀 Crypto Streaming Pipeline Setup"
echo "===================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11+ required. Found: $python_version"
    exit 1
fi
echo "✅ Python $python_version"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Dependencies installed"
echo ""

# Create .env file
echo "⚙️  Setting up configuration..."
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping .env creation"
    else
        cp .env.example .env
        echo "✅ .env file created"
    fi
else
    cp .env.example .env
    echo "✅ .env file created"
fi
echo ""

# Prompt for credentials
echo "🔑 Configuration Setup"
echo "----------------------"
echo "Please enter your credentials (or press Enter to skip):"
echo ""

read -p "Kafka Bootstrap Servers: " kafka_servers
read -p "Kafka Username: " kafka_username
read -sp "Kafka Password: " kafka_password
echo ""
read -p "Database URL: " database_url
echo ""

# Update .env file if credentials provided
if [ ! -z "$kafka_servers" ]; then
    sed -i.bak "s|KAFKA_BOOTSTRAP_SERVERS=.*|KAFKA_BOOTSTRAP_SERVERS=$kafka_servers|" .env
    sed -i.bak "s|KAFKA_USERNAME=.*|KAFKA_USERNAME=$kafka_username|" .env
    sed -i.bak "s|KAFKA_PASSWORD=.*|KAFKA_PASSWORD=$kafka_password|" .env
    sed -i.bak "s|DATABASE_URL=.*|DATABASE_URL=$database_url|" .env
    rm .env.bak
    echo "✅ Configuration updated"
fi
echo ""

# Setup database
if [ ! -z "$database_url" ]; then
    echo "🗄️  Setting up database..."
    python scripts/setup_database.py
    echo ""
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
echo "✅ Directories created"
echo ""

# Summary
echo "✨ Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials (if not done)"
echo "2. Run database setup: python scripts/setup_database.py"
echo "3. Start producer: python src/producer.py"
echo "4. Start consumer: python src/consumer.py"
echo "5. Start dashboard: streamlit run src/dashboard.py"
echo ""
echo "For deployment instructions, see DEPLOYMENT.md"
echo ""
