#!/usr/bin/env python3
"""
Database initialization script for FoodShare application.
This script creates all necessary tables and inserts default data.
"""

from database import engine, Base
from models import User, Category, FoodPost, FoodImage, Message, Review
from auth import get_password_hash
from sqlalchemy.orm import Session

def init_database():
    """Initialize the database with tables and default data."""
    print("🔄 Creating database tables...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    
    # Create a session to insert data
    db = Session(bind=engine)
    
    try:
        # Check if categories already exist by trying to query them
        try:
            category_count = db.query(Category).count()
        except Exception:
            # If query fails, assume no categories exist
            category_count = 0
            
        if category_count == 0:
            print("🔄 Inserting default categories...")
            
            # Insert default categories
            categories = [
                Category(name="Fruits", description="Fresh fruits and berries", icon="🍎"),
                Category(name="Vegetables", description="Fresh vegetables and greens", icon="🥬"),
                Category(name="Grains", description="Rice, pasta, bread, cereals", icon="🍞"),
                Category(name="Dairy", description="Milk, cheese, yogurt, eggs", icon="🥛"),
                Category(name="Meat", description="Chicken, beef, pork, fish", icon="🥩"),
                Category(name="Prepared Food", description="Cooked meals, leftovers", icon="🍽️"),
                Category(name="Baked Goods", description="Bread, pastries, desserts", icon="🧁"),
                Category(name="Pantry Items", description="Canned goods, spices, condiments", icon="🥫"),
                Category(name="Beverages", description="Drinks, juices, coffee, tea", icon="☕"),
                Category(name="Other", description="Miscellaneous food items", icon="📦"),
            ]
            
            for category in categories:
                db.add(category)
            
            db.commit()
            print("✅ Default categories inserted!")
        else:
            print("ℹ️  Categories already exist, skipping...")
        
        # Check if test users already exist
        try:
            test_user = db.query(User).filter(User.username == "testuser").first()
        except Exception:
            test_user = None
            
        if not test_user:
            print("🔄 Creating test user...")
            
            test_user = User(
                username="testuser",
                email="test@example.com",
                password_hash=get_password_hash("password123"),
                full_name="Test User",
                phone="555-0123",
                address="123 Test Street",
                city="Test City",
                state="Test State",
                zip_code="12345",
                bio="This is a test user for development purposes",
                is_active=True,
                is_admin=False
            )
            db.add(test_user)
            print("✅ Test user created: username='testuser', email='test@example.com', password='password123'")
        else:
            print("ℹ️  Test user already exists")
        
        # Check if admin user already exists
        try:
            admin_user = db.query(User).filter(User.username == "admin").first()
        except Exception:
            admin_user = None
            
        if not admin_user:
            print("🔄 Creating admin user...")
            
            admin_user = User(
                username="admin",
                email="admin@example.com",
                password_hash=get_password_hash("admin123"),
                full_name="Admin User",
                phone="555-0124",
                address="456 Admin Avenue",
                city="Admin City",
                state="Admin State",
                zip_code="54321",
                bio="This is an admin user for testing admin functionality",
                is_active=True,
                is_admin=True
            )
            db.add(admin_user)
            print("✅ Admin user created: username='admin', email='admin@example.com', password='admin123'")
        else:
            print("ℹ️  Admin user already exists")
        
        db.commit()
        print("🎉 Database initialization completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during database initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
