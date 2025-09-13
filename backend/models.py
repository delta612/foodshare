from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, Time, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(10))
    profile_picture = Column(String(255))
    bio = Column(Text)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    food_posts = relationship("FoodPost", foreign_keys="FoodPost.user_id", back_populates="user")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    reviews_given = relationship("Review", foreign_keys="Review.reviewer_id", back_populates="reviewer")
    reviews_received = relationship("Review", foreign_keys="Review.reviewed_user_id", back_populates="reviewed_user")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    food_posts = relationship("FoodPost", back_populates="category")

class FoodPost(Base):
    __tablename__ = "food_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    quantity = Column(String(100))
    expiry_date = Column(Date)
    pickup_location = Column(Text, nullable=False)
    pickup_time_start = Column(Time)
    pickup_time_end = Column(Time)
    is_available = Column(Boolean, default=True)
    is_claimed = Column(Boolean, default=False)
    claimed_by = Column(Integer, ForeignKey("users.id"))
    claimed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="food_posts")
    category = relationship("Category", back_populates="food_posts")
    claimed_by_user = relationship("User", foreign_keys=[claimed_by])
    images = relationship("FoodImage", back_populates="food_post", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="food_post")

class FoodImage(Base):
    __tablename__ = "food_images"
    
    id = Column(Integer, primary_key=True, index=True)
    food_post_id = Column(Integer, ForeignKey("food_posts.id"), nullable=False)
    image_path = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    food_post = relationship("FoodPost", back_populates="images")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_post_id = Column(Integer, ForeignKey("food_posts.id"))
    subject = Column(String(200))
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    food_post = relationship("FoodPost", back_populates="messages")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewed_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_post_id = Column(Integer, ForeignKey("food_posts.id"))
    rating = Column(Integer, CheckConstraint("rating >= 1 AND rating <= 5"))
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviews_given")
    reviewed_user = relationship("User", foreign_keys=[reviewed_user_id], back_populates="reviews_received")
    food_post = relationship("FoodPost")
    
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),
    )
