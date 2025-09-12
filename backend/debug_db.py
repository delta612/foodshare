#!/usr/bin/env python3
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🔄 Testing database connection...")
    from database import engine, Base
    from models import FoodPost, User, Category
    
    print("✅ Imports successful!")
    
    # Test database connection
    with engine.connect() as conn:
        print("✅ Database connection successful!")
        
        # Check if tables exist using SQLAlchemy text
        from sqlalchemy import text
        
        result = conn.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result.fetchall()]
        print(f"📋 Tables in database: {tables}")
        
        # Check food_posts table
        if 'food_posts' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM food_posts"))
            count = result.scalar()
            print(f"🍎 Found {count} food posts in database")
        else:
            print("❌ food_posts table not found!")
            
        # Check users table
        if 'users' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar()
            print(f"👥 Found {count} users in database")
        else:
            print("❌ users table not found!")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
