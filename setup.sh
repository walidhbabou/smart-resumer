#!/bin/bash

# SmartResume Analyzer - Local Setup Script
# This script helps set up the development environment

set -e

echo "🚀 SmartResume Analyzer - Setup Script"
echo "======================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✓ Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker Compose is installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your API keys."
else
    echo "✓ .env file already exists"
fi

# Create backend .env if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env file..."
    cp backend/.env.example backend/.env
    echo "✓ backend/.env file created"
else
    echo "✓ backend/.env file already exists"
fi

# Create frontend .env if it doesn't exist
if [ ! -f frontend/.env ]; then
    echo "📝 Creating frontend/.env file..."
    cp frontend/.env.example frontend/.env
    echo "✓ frontend/.env file created"
else
    echo "✓ frontend/.env file already exists"
fi

echo ""
echo "======================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env files with your configuration"
echo "2. Run: docker-compose up --build"
echo "3. Access application at http://localhost:3000"
echo "4. Access API docs at http://localhost:8000/api/docs"
echo ""
echo "For local development without Docker:"
echo "  Backend: cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload"
echo "  Frontend: cd frontend && npm install && npm run dev"
echo ""
