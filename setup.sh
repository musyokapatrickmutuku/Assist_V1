#!/bin/bash

# Assist AI - Quick Setup Script
# This script helps set up the demo environment quickly

echo "🏥 Welcome to Assist AI Setup!"
echo "================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env file if it doesn't exist
if [ ! -f backend_service/.env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example backend_service/.env
    
    echo ""
    echo "⚠️  IMPORTANT: Please add your DeepSeek API key to backend_service/.env"
    echo "   Edit the file and replace 'your_deepseek_api_key_here' with your actual key"
    echo "   Get your API key from: https://platform.deepseek.com/"
    echo ""
    read -p "Press Enter once you've added your API key..."
fi

# Initialize the database
echo "🗄️  Initializing database..."
python3 backend_service/patient_db.py

# Build and start containers
echo "🚀 Building and starting containers..."
docker-compose build
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if curl -f http://localhost:8000/ &> /dev/null; then
    echo "✅ Backend service is running"
else
    echo "❌ Backend service failed to start. Check logs with: docker-compose logs backend"
fi

if curl -f http://localhost:8501/ &> /dev/null; then
    echo "✅ Frontend service is running"
else
    echo "❌ Frontend service failed to start. Check logs with: docker-compose logs frontend"
fi

echo ""
echo "🎉 Setup complete!"
echo "================================"
echo "Access the application at:"
echo "🌐 Frontend: http://localhost:8501"
echo "🔧 Backend API: http://localhost:8000"
echo ""
echo "📚 Demo Accounts:"
echo "Patients: Sarah Johnson (P001), Michael Thompson (P002), etc."
echo "Doctors: Dr. Emily Chen (D001), Dr. Michael Roberts (D002)"
echo "Password: demo123"
echo ""
echo "📖 View logs: docker-compose logs -f"
echo "🛑 Stop services: docker-compose down"
echo ""
echo "Happy hacking! 🚀" 