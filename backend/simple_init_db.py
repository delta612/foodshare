#!/usr/bin/env python3
"""
Simple database initialization script for FoodShare application.
"""

from database import engine, Base
from models import User, Category
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
        
        db.commit()
        print("✅ Test users created!")
        print("🎉 Database initialization completed successfully!")
        print("\n📋 Test Users Created:")
        print("   Regular User: username='testuser', email='test@example.com', password='password123'")
        print("   Admin User: username='admin', email='admin@example.com', password='admin123'")
        
    except Exception as e:
        print(f"❌ Error during database initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
