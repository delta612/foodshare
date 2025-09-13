from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime, date, time

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    bio: Optional[str] = None

class UserResponse(UserBase):
    id: int
    profile_picture: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Food Image Schemas
class FoodImageBase(BaseModel):
    image_path: str
    is_primary: bool = False

class FoodImageCreate(FoodImageBase):
    pass

class FoodImageResponse(FoodImageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Food Post Schemas
class FoodPostBase(BaseModel):
    title: str
    description: str
    category_id: Optional[int] = None
    quantity: Optional[str] = None
    expiry_date: Optional[date] = None
    pickup_location: str
    pickup_time_start: Optional[time] = None
    pickup_time_end: Optional[time] = None

class FoodPostCreate(FoodPostBase):
    images: Optional[List[FoodImageCreate]] = []

class FoodPostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    quantity: Optional[str] = None
    expiry_date: Optional[date] = None
    pickup_location: Optional[str] = None
    pickup_time_start: Optional[time] = None
    pickup_time_end: Optional[time] = None
    is_available: Optional[bool] = None

class FoodPostResponse(FoodPostBase):
    id: int
    user_id: int
    is_available: bool
    is_claimed: bool
    claimed_by: Optional[int] = None
    claimed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    user: UserResponse
    category: Optional[CategoryResponse] = None
    images: List[FoodImageResponse] = []
    
    class Config:
        from_attributes = True

class FoodPostListResponse(BaseModel):
    id: int
    title: str
    description: str
    quantity: Optional[str] = None
    expiry_date: Optional[date] = None
    pickup_location: str
    is_available: bool
    is_claimed: bool
    created_at: datetime
    user: UserResponse
    category: Optional[CategoryResponse] = None
    primary_image: Optional[FoodImageResponse] = None
    
    class Config:
        from_attributes = True

# Message Schemas
class MessageBase(BaseModel):
    receiver_id: int
    food_post_id: Optional[int] = None
    subject: Optional[str] = None
    message: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    sender_id: int
    is_read: bool
    created_at: datetime
    sender: UserResponse
    receiver: UserResponse
    food_post: Optional[FoodPostListResponse] = None
    
    class Config:
        from_attributes = True

# Review Schemas
class ReviewBase(BaseModel):
    reviewed_user_id: int
    food_post_id: Optional[int] = None
    rating: int
    comment: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    reviewer_id: int
    created_at: datetime
    reviewer: UserResponse
    reviewed_user: UserResponse
    food_post: Optional[FoodPostListResponse] = None
    
    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Search and Filter Schemas
class FoodPostSearch(BaseModel):
    query: Optional[str] = None
    category_id: Optional[int] = None
    city: Optional[str] = None
    state: Optional[str] = None
    is_available: Optional[bool] = True
    limit: int = 20
    offset: int = 0

class MessageSearch(BaseModel):
    limit: int = 20
    offset: int = 0

# Upload Schema
class FileUploadResponse(BaseModel):
    filename: str
    file_path: str
    file_size: int
