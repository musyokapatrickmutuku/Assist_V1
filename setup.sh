#!/bin/bash

# Assist AI - Simplified Setup Script
# This script sets up the simplified MVP demo environment

echo "🏥 Welcome to Assist AI - Simplified Demo Setup!"
echo "================================================="
echo "This simplified version removes complex dependencies"
echo "and focuses on core functionality for MVP demo."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    echo "Visit: https://python.org/downloads/"
    exit 1
fi

# Determine Python command
PYTHON_CMD="python3"
if command -v python &> /dev/null && python --version 2>&1 | grep -q "Python 3"; then
    PYTHON_CMD="python"
fi

echo "✅ Python is installed"

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Determine pip command
PIP_CMD="pip3"
if command -v pip &> /dev/null; then
    PIP_CMD="pip"
fi

echo "✅ pip is installed"

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend_service
$PIP_CMD install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install backend dependencies"
    exit 1
fi
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend/streamlit_app
$PIP_CMD install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi
cd ../..

echo "✅ All dependencies installed successfully"
echo ""

# Create simplified database
echo "🗄️  Initializing simplified database..."
$PYTHON_CMD backend_service/patient_db.py

echo "✅ Database initialized"
echo ""

echo "🎉 Setup Complete!"
echo "=================="
echo "Choose your preferred startup method:"
echo ""
echo "📱 Option 1: Quick Start (Windows - Recommended)"
echo "   1. Double-click: run_simple_backend.bat"
echo "   2. Double-click: run_simple_frontend.bat"
echo "   3. Browser will open automatically"
echo ""
echo "💻 Option 2: Manual Start (All platforms)"
echo "   Terminal 1 (Backend):"
echo "   cd backend_service && $PYTHON_CMD main_simple.py"
echo ""
echo "   Terminal 2 (Frontend):"
echo "   cd frontend/streamlit_app"
echo "   export BACKEND_URL=http://localhost:8002  # Linux/Mac"
echo "   set BACKEND_URL=http://localhost:8002     # Windows"
echo "   streamlit run app_simple.py --server.port 8506"
echo ""
echo "🌐 Access Points:"
echo "   Frontend: http://localhost:8506"
echo "   Backend:  http://localhost:8002"
echo ""
echo "📚 Demo Flow:"
echo "1. Login as Patient: Select 'Sarah Johnson' → Login"
echo "2. Submit Question: Type medical question → Send to Doctor"
echo "3. Login as Doctor: Logout → Select 'Doctor' → Login"
echo "4. Review & Respond: See question → Write response → Send"
echo "5. Verify: Login as patient → Check 'My Questions' tab"
echo ""
echo "✨ Key Features Working:"
echo "   ✅ Question submission with confirmation"
echo "   ✅ Doctor review interface"
echo "   ✅ Response sending"
echo "   ✅ Real-time status updates"
echo "   ✅ Urgency prioritization"
echo "   ✅ Complete patient-doctor workflow"
echo ""
echo "🔧 No External Dependencies:"
echo "   ✅ No API keys required"
echo "   ✅ No Docker needed"
echo "   ✅ No LangGraph complexity"
echo "   ✅ Simple SQLite database"
echo ""
echo "📖 For detailed instructions, see: README_SIMPLE.md"
echo ""
echo "Happy testing! 🚀"