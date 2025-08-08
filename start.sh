#!/bin/bash

# AI App Builder - Startup Script
# This script helps you get the application running quickly

set -e

echo "🚀 Starting AI App Builder..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from .env.example..."
    cp .env.example .env
    print_warning "Please edit .env file with your API keys before continuing."
    echo
    echo "Required API keys:"
    echo "  - OPENAI_API_KEY: Get from https://platform.openai.com/api-keys"
    echo "  - ANTHROPIC_API_KEY: Get from https://console.anthropic.com/ (optional)"
    echo
    read -p "Press Enter to continue after updating .env file..."
fi

# Check if Docker is available
if command -v docker-compose >/dev/null 2>&1; then
    print_status "Docker Compose found. Starting with Docker..."
    
    # Create necessary directories
    mkdir -p projects deployments logs
    
    # Start services
    print_status "Building and starting containers..."
    docker-compose up -d
    
    print_success "All services started successfully!"
    echo
    echo "🌐 Access URLs:"
    echo "  Frontend:     http://localhost:3000"
    echo "  FastAPI:      http://localhost:8000"
    echo "  Django Admin: http://localhost:8001/admin"
    echo
    echo "📊 Container Status:"
    docker-compose ps
    
elif command -v docker >/dev/null 2>&1; then
    print_error "Docker found but docker-compose is missing."
    print_status "Please install docker-compose or use manual setup."
    exit 1
else
    print_warning "Docker not found. Starting manual setup..."
    
    # Check Python
    if ! command -v python3 >/dev/null 2>&1; then
        print_error "Python 3 is required but not installed."
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node >/dev/null 2>&1; then
        print_error "Node.js is required but not installed."
        exit 1
    fi
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Install Node.js dependencies
    print_status "Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
    
    # Create necessary directories
    mkdir -p projects deployments logs django_backend/logs
    
    print_success "Manual setup completed!"
    echo
    echo "To start the services manually:"
    echo "  1. Terminal 1: cd src && python main.py"
    echo "  2. Terminal 2: cd django_backend && python manage.py runserver 8001"
    echo "  3. Terminal 3: cd frontend && npm start"
    echo
fi

echo
print_success "🎉 AI App Builder is ready!"
echo
echo "📚 Quick Start:"
echo "  1. Visit http://localhost:3000"
echo "  2. Create an account or login"
echo "  3. Describe your app idea"
echo "  4. Watch AI generate your app!"
echo
echo "🔧 Development:"
echo "  - API Documentation: http://localhost:8000/docs"
echo "  - Django Admin: http://localhost:8001/admin"
echo "  - Logs: Check ./logs/ directory"
echo
echo "❓ Need help? Check the README.md file or visit our documentation."