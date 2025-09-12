from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
from typing import List, Optional
import os

# Import our modules
from database import get_db, engine, Base
from models import User, Category, FoodPost, FoodImage, Message, Review
from schemas import (
    UserCreate, UserResponse, UserLogin, UserUpdate,
    CategoryResponse, CategoryCreate,
    FoodPostCreate, FoodPostResponse, FoodPostUpdate, FoodPostListResponse, FoodPostSearch,
    FoodImageCreate, FoodImageResponse,
    MessageCreate, MessageResponse, MessageSearch,
    ReviewCreate, ReviewResponse,
    Token, FileUploadResponse
)
from auth import (
    authenticate_user, create_access_token, create_user,
    get_current_user, get_current_active_user, get_current_admin_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from utils import (
    save_uploaded_file, delete_file, save_food_images, delete_food_images,
    get_primary_image, validate_image_file, format_file_size
)

# Create database tables
print("🔄 Initializing database...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created!")

# Create test users if they don't exist
def create_test_users():
    """Create hardcoded test users for development/testing."""
    from sqlalchemy.orm import Session
    from auth import get_password_hash
    from sqlalchemy.exc import OperationalError
    
    try:
        db = Session(bind=engine)
        
        # Check if test user already exists
        test_user = db.query(User).filter(User.username == "testuser").first()
        if not test_user:
            # Create test user
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
            db.commit()
            print("✅ Test user created: username='testuser', email='test@example.com', password='password123'")
        else:
            print("ℹ️  Test user already exists")
        
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            # Create admin user
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
            print("✅ Admin user created: username='admin', email='admin@example.com', password='admin123'")
        else:
            print("ℹ️  Admin user already exists")
        
        db.close()
    except OperationalError as e:
        print(f"⚠️  Database not ready yet: {e}")
        print("ℹ️  Test users will be created when the database is initialized")

app = FastAPI(title="Food Sharing API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    """Initialize database and create test users on startup."""
    print("🚀 Starting FoodShare API...")
    create_test_users()

# Initialize test users after app creation
create_test_users()

# Ensure uploads folder exists
os.makedirs("uploads", exist_ok=True)

# Serve static files (uploaded images)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def home():
    return {"message": "Food Sharing API is running!", "version": "1.0.0"}

# Authentication endpoints
@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if username already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    return create_user(db, user.dict())

@app.post("/login", response_model=Token)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token."""
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user

@app.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user information."""
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

# Category endpoints
@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Get all food categories."""
    return db.query(Category).all()

@app.post("/categories", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new food category (admin only)."""
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Food Post endpoints
@app.get("/food-posts", response_model=List[FoodPostListResponse])
def get_food_posts(
    search: FoodPostSearch = Depends(),
    db: Session = Depends(get_db)
):
    """Get food posts with optional filtering."""
    query = db.query(FoodPost)
    
    # Apply filters
    if search.query:
        query = query.filter(
            FoodPost.title.contains(search.query) |
            FoodPost.description.contains(search.query)
        )
    
    if search.category_id:
        query = query.filter(FoodPost.category_id == search.category_id)
    
    if search.city:
        query = query.join(User).filter(User.city == search.city)
    
    if search.state:
        query = query.join(User).filter(User.state == search.state)
    
    if search.is_available is not None:
        query = query.filter(FoodPost.is_available == search.is_available)
    
    # Apply pagination and load relationships
    posts = query.options(
        joinedload(FoodPost.user),
        joinedload(FoodPost.category)
    ).offset(search.offset).limit(search.limit).all()
    
    # Add primary image to each post
    result = []
    for post in posts:
        post_dict = post.__dict__.copy()
        primary_image = get_primary_image(post)
        post_dict['primary_image'] = primary_image
        result.append(FoodPostListResponse(**post_dict))
    
    return result

@app.post("/food-posts", response_model=FoodPostResponse)
def create_food_post(
    title: str = Form(...),
    description: str = Form(...),
    category_id: Optional[int] = Form(None),
    quantity: Optional[str] = Form(None),
    expiry_date: Optional[str] = Form(None),
    pickup_location: str = Form(...),
    pickup_time_start: Optional[str] = Form(None),
    pickup_time_end: Optional[str] = Form(None),
    images: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new food post."""
    # Validate images
    for image in images:
        if not validate_image_file(image):
            raise HTTPException(
                status_code=400,
                detail="Invalid image file. Only JPG, PNG, GIF, WEBP files up to 10MB are allowed."
            )
    
    # Create food post
    food_post_data = {
        "user_id": current_user.id,
        "title": title,
        "description": description,
        "category_id": category_id,
        "quantity": quantity,
        "pickup_location": pickup_location,
        "pickup_time_start": None,
        "pickup_time_end": None
    }
    
    if expiry_date:
        food_post_data["expiry_date"] = datetime.strptime(expiry_date, "%Y-%m-%d").date()
    
    # Convert time strings to Python time objects
    if pickup_time_start:
        food_post_data["pickup_time_start"] = datetime.strptime(pickup_time_start, "%H:%M").time()
    
    if pickup_time_end:
        food_post_data["pickup_time_end"] = datetime.strptime(pickup_time_end, "%H:%M").time()
    
    db_food_post = FoodPost(**food_post_data)
    db.add(db_food_post)
    db.commit()
    db.refresh(db_food_post)
    
    # Save images
    save_food_images(db, db_food_post.id, images)
    
    # Refresh to get images
    db.refresh(db_food_post)
    return db_food_post

@app.get("/food-posts/{post_id}", response_model=FoodPostResponse)
def get_food_post(post_id: int, db: Session = Depends(get_db)):
    """Get a specific food post."""
    food_post = db.query(FoodPost).filter(FoodPost.id == post_id).first()
    if not food_post:
        raise HTTPException(status_code=404, detail="Food post not found")
    return food_post

@app.put("/food-posts/{post_id}", response_model=FoodPostResponse)
def update_food_post(
    post_id: int,
    food_post_update: FoodPostUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a food post."""
    food_post = db.query(FoodPost).filter(FoodPost.id == post_id).first()
    if not food_post:
        raise HTTPException(status_code=404, detail="Food post not found")
    
    if food_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    for field, value in food_post_update.dict(exclude_unset=True).items():
        setattr(food_post, field, value)
    
    db.commit()
    db.refresh(food_post)
    return food_post

@app.delete("/food-posts/{post_id}")
def delete_food_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a food post."""
    food_post = db.query(FoodPost).filter(FoodPost.id == post_id).first()
    if not food_post:
        raise HTTPException(status_code=404, detail="Food post not found")
    
    if food_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    try:
        # Delete associated images first
        images_deleted = delete_food_images(db, post_id)
        if not images_deleted:
            # Log warning but continue with deletion
            print(f"Warning: Failed to delete some images for post {post_id}")
        
        # Delete the post
        db.delete(food_post)
        db.commit()
        return {"message": "Food post deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete food post: {str(e)}")

@app.post("/food-posts/{post_id}/claim")
def claim_food_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Claim a food post."""
    # Use SELECT FOR UPDATE to prevent race conditions
    food_post = db.query(FoodPost).filter(
        FoodPost.id == post_id,
        FoodPost.is_available == True,
        FoodPost.is_claimed == False
    ).with_for_update().first()
    
    if not food_post:
        raise HTTPException(status_code=404, detail="Food post not found or no longer available")
    
    if food_post.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot claim your own post")
    
    # Double-check conditions after acquiring lock
    if not food_post.is_available or food_post.is_claimed:
        raise HTTPException(status_code=400, detail="Food post is no longer available")
    
    food_post.is_claimed = True
    food_post.claimed_by = current_user.id
    food_post.claimed_at = datetime.utcnow()
    
    db.commit()
    return {"message": "Food post claimed successfully"}

# Message endpoints
@app.get("/messages", response_model=List[MessageResponse])
def get_messages(
    search: MessageSearch = Depends(),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get messages for current user with pagination."""
    messages = db.query(Message).filter(
        (Message.sender_id == current_user.id) |
        (Message.receiver_id == current_user.id)
    ).order_by(Message.created_at.desc()).offset(search.offset).limit(search.limit).all()
    return messages

@app.post("/messages", response_model=MessageResponse)
def send_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Send a message to another user."""
    db_message = Message(
        sender_id=current_user.id,
        **message.dict()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# Review endpoints
@app.post("/reviews", response_model=ReviewResponse)
def create_review(
    review: ReviewCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a review for a user."""
    db_review = Review(
        reviewer_id=current_user.id,
        **review.dict()
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/users/{user_id}/reviews", response_model=List[ReviewResponse])
def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
    """Get reviews for a specific user."""
    reviews = db.query(Review).filter(Review.reviewed_user_id == user_id).all()
    return reviews

# File upload endpoint
@app.post("/upload", response_model=FileUploadResponse)
def upload_file(file: UploadFile = File(...)):
    """Upload a file."""
    if not validate_image_file(file):
        raise HTTPException(
            status_code=400,
            detail="Invalid file. Only image files up to 10MB are allowed."
        )
    
    file_path = save_uploaded_file(file)
    file_size = os.path.getsize(file_path)
    
    return FileUploadResponse(
        filename=file.filename,
        file_path=file_path,
        file_size=file_size
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)