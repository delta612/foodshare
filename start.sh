#!/bin/bash

# FoodShare Startup Script
echo "🍎 Starting FoodShare Application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if MySQL is running
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL is not installed. Please install MySQL first."
    exit 1
fi

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Please create one with your database credentials."
    echo "Example:"
    echo "DATABASE_URL=mysql+pymysql://username:password@localhost:3306/foodshare"
    echo "SECRET_KEY=your-secret-key-here"
    exit 1
fi

# Start the server
echo "🚀 Starting FoodShare server..."
echo "📱 Frontend will be available at: http://localhost:8000"
echo "📚 API documentation at: http://localhost:8000/docs"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python main.py
