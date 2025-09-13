#!/bin/bash

# Frontend Server Startup Script
echo "🚀 Starting FoodShare Frontend Server..."

# Navigate to frontend directory
cd /Users/dtorredo/Code/foodshare/frontend

# Kill any existing server on port 3000
echo "🔄 Checking for existing servers..."
lsof -ti:3000 | xargs kill -9 2>/dev/null || echo "No existing server found"

# Start the frontend server
echo "🌐 Starting frontend server on http://localhost:3000"
echo "📱 Open your browser and go to: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "----------------------------------------"

python3 -m http.server 3000
