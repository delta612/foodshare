import os
import uuid
import logging
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from models import FoodImage, FoodPost

# Set up logging
logger = logging.getLogger(__name__)

def save_uploaded_file(file: UploadFile, upload_dir: str = "uploads") -> str:
    """Save an uploaded file and return the file path."""
    try:
        # Create upload directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        
        logger.info(f"File saved successfully: {file_path}")
        return file_path
    except OSError as e:
        logger.error(f"Failed to save file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error saving file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save file")

def delete_file(file_path: str) -> bool:
    """Delete a file from the filesystem."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted successfully: {file_path}")
            return True
        logger.warning(f"File not found for deletion: {file_path}")
        return False
    except OSError as e:
        logger.error(f"Failed to delete file {file_path}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error deleting file {file_path}: {str(e)}")
        return False

def save_food_images(db: Session, food_post_id: int, images: List[UploadFile], upload_dir: str = "uploads") -> List[FoodImage]:
    """Save multiple food images and create database records."""
    saved_images = []
    
    try:
        for i, image in enumerate(images):
            file_path = save_uploaded_file(image, upload_dir)
            
            db_image = FoodImage(
                food_post_id=food_post_id,
                image_path=file_path,
                is_primary=(i == 0)  # First image is primary
            )
            db.add(db_image)
            saved_images.append(db_image)
        
        db.commit()
        logger.info(f"Saved {len(saved_images)} images for food post {food_post_id}")
        return saved_images
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save images for food post {food_post_id}: {str(e)}")
        # Clean up any files that were saved before the error
        for image in saved_images:
            delete_file(image.image_path)
        raise HTTPException(status_code=500, detail="Failed to save images")

def delete_food_images(db: Session, food_post_id: int) -> bool:
    """Delete all images associated with a food post."""
    try:
        images = db.query(FoodImage).filter(FoodImage.food_post_id == food_post_id).all()
        deleted_count = 0
        
        for image in images:
            if delete_file(image.image_path):
                deleted_count += 1
            db.delete(image)
        
        db.commit()
        logger.info(f"Deleted {deleted_count}/{len(images)} images for food post {food_post_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete images for food post {food_post_id}: {str(e)}")
        return False

def get_primary_image(food_post: FoodPost) -> FoodImage:
    """Get the primary image for a food post."""
    primary_image = next((img for img in food_post.images if img.is_primary), None)
    if not primary_image and food_post.images:
        primary_image = food_post.images[0]
    return primary_image

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_image_file(file: UploadFile) -> bool:
    """Validate that the uploaded file is an image."""
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        return False
    
    # Check file size (max 10MB)
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > 10 * 1024 * 1024:  # 10MB
        return False
    
    return True

def clean_old_files(upload_dir: str = "uploads", days_old: int = 30) -> int:
    """Clean up old uploaded files that are no longer referenced."""
    import time
    from datetime import datetime, timedelta
    
    cutoff_time = time.time() - (days_old * 24 * 60 * 60)
    deleted_count = 0
    
    try:
        if not os.path.exists(upload_dir):
            logger.warning(f"Upload directory does not exist: {upload_dir}")
            return 0
            
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)
                if file_time < cutoff_time:
                    if delete_file(file_path):
                        deleted_count += 1
                        
        logger.info(f"Cleaned up {deleted_count} old files from {upload_dir}")
        return deleted_count
    except OSError as e:
        logger.error(f"Failed to clean old files from {upload_dir}: {str(e)}")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error cleaning old files: {str(e)}")
        return 0
