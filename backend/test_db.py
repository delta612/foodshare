#!/usr/bin/env python3
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from database import engine, Base
    from models import User, Category
    from auth import get_password_hash
    from sqlalchemy.orm import Session
    
    print("✅ All imports successful!")
    
    # Create tables
    print("🔄 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created!")
    
    # Test database connection
    db = Session(bind=engine)
    print("✅ Database connection successful!")
    
    # Create test user
    test_user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        full_name="Test User",
        is_active=True,
        is_admin=False
    )
    db.add(test_user)
    db.commit()
    print("✅ Test user created!")
    
    db.close()
    print("🎉 Database initialization completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
