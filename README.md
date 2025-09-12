# FoodShare - Food Sharing Platform

A community-driven platform that connects people to share surplus food and reduce waste. Built with FastAPI (backend) and vanilla JavaScript (frontend).

## 🌟 Features

- **User Authentication**: Secure registration and login system
- **Food Sharing**: Post surplus food with photos, descriptions, and pickup details
- **Food Discovery**: Browse available food by category, location, and search terms
- **Real-time Communication**: Message system for coordinating food pickups
- **User Reviews**: Rate and review other users to build community trust
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices

## 🏗️ Architecture

- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: MySQL
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **Authentication**: JWT tokens
- **File Storage**: Local file system (configurable for cloud storage)

## 📋 Prerequisites

- Python 3.8+
- MySQL 5.7+
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd foodshare

# Start the application with Docker Compose
docker-compose up -d

# The application will be available at:
# - Frontend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### 1. Database Setup

```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE foodshare;
exit

# Run the SQL initialization script
mysql -u root -p foodshare < backend/sql_init.sql
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="mysql+pymysql://username:password@localhost:3306/foodshare"
export SECRET_KEY="your-secret-key-here"

# Run the server
python main.py
```

The API will be available at `http://localhost:8000`

#### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Serve the frontend (using Python's built-in server)
python -m http.server 3000
```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database Configuration
DB_USER=root
DB_PASSWORD=your_secure_password_here
DB_HOST=localhost
DB_PORT=3306
DB_NAME=foodshare

# Security - REQUIRED
SECRET_KEY=your-super-secret-key-change-in-production-must-be-at-least-32-characters-long

# Application Settings
DEBUG=False
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database Configuration

The database connection is now configured through environment variables. No need to modify `backend/database.py` directly.

## 📱 API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints

- `POST /register` - User registration
- `POST /login` - User login
- `GET /food-posts` - List food posts
- `POST /food-posts` - Create food post
- `GET /food-posts/{id}` - Get specific food post
- `POST /food-posts/{id}/claim` - Claim food post
- `GET /categories` - List food categories

## 🌐 Production Deployment

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using a VPS

1. **Set up server** (Ubuntu 20.04+ recommended)
2. **Install dependencies**:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip mysql-server nginx
   ```

3. **Deploy application**:

   ```bash
   git clone your-repo
   cd foodshare/backend
   pip3 install -r requirements.txt
   ```

4. **Configure Nginx**:

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /uploads {
           alias /path/to/your/app/uploads;
       }
   }
   ```

5. **Set up SSL** (Let's Encrypt):
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## 🔒 Security Considerations

### Critical Security Requirements:

- **MUST** set a strong `SECRET_KEY` environment variable (minimum 32 characters)
- **MUST** use strong database passwords
- **MUST** use HTTPS in production
- **MUST** set `DEBUG=False` in production

### Security Features Implemented:

- ✅ Environment variable configuration (no hardcoded secrets)
- ✅ JWT token authentication with configurable expiration
- ✅ Admin-only endpoints for category management
- ✅ Input validation and sanitization
- ✅ SQL injection protection via SQLAlchemy ORM
- ✅ File upload validation and size limits
- ✅ Race condition protection for food claiming
- ✅ Proper error handling without information leakage

### Additional Recommendations:

- Implement rate limiting for API endpoints
- Use a reverse proxy (nginx) in production
- Regularly update dependencies
- Monitor logs for suspicious activity
- Implement backup and recovery procedures

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**:

   - Check MySQL is running
   - Verify database credentials
   - Ensure database exists

2. **File Upload Issues**:

   - Check uploads directory permissions
   - Verify file size limits
   - Check CORS settings

3. **Authentication Issues**:
   - Verify JWT secret key
   - Check token expiration
   - Ensure proper headers

### Getting Help

- Check the API documentation at `/docs`
- Review the logs for error messages
- Open an issue on GitHub

## 🔮 Future Enhancements

- [ ] Real-time notifications
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced search filters
- [ ] Food expiration alerts
- [ ] Integration with food banks
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Cloud storage integration

---

**Made with ❤️ for reducing food waste and building stronger communities.**
