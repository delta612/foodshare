-- Food Sharing Application Database Schema
-- This creates all necessary tables for a food sharing platform

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS foodshare;
USE foodshare;

-- Users table for authentication and profiles
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    profile_picture VARCHAR(255),
    bio TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Food categories table
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Food posts table
CREATE TABLE food_posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category_id INT,
    quantity VARCHAR(100),
    expiry_date DATE,
    pickup_location TEXT NOT NULL,
    pickup_time_start TIME,
    pickup_time_end TIME,
    is_available BOOLEAN DEFAULT TRUE,
    is_claimed BOOLEAN DEFAULT FALSE,
    claimed_by INT NULL,
    claimed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (claimed_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Food post images table
CREATE TABLE food_images (
    id INT PRIMARY KEY AUTO_INCREMENT,
    food_post_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_post_id) REFERENCES food_posts(id) ON DELETE CASCADE
);

-- Messages table for communication between users
CREATE TABLE messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    food_post_id INT,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_post_id) REFERENCES food_posts(id) ON DELETE SET NULL
);

-- Reviews/ratings table
CREATE TABLE reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reviewer_id INT NOT NULL,
    reviewed_user_id INT NOT NULL,
    food_post_id INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_post_id) REFERENCES food_posts(id) ON DELETE SET NULL,
    UNIQUE KEY unique_review (reviewer_id, reviewed_user_id, food_post_id)
);

-- Insert default categories
INSERT INTO categories (name, description, icon) VALUES
('Fruits', 'Fresh fruits and berries', '🍎'),
('Vegetables', 'Fresh vegetables and greens', '🥬'),
('Grains', 'Rice, pasta, bread, cereals', '🍞'),
('Dairy', 'Milk, cheese, yogurt, eggs', '🥛'),
('Meat', 'Chicken, beef, pork, fish', '🥩'),
('Prepared Food', 'Cooked meals, leftovers', '🍽️'),
('Baked Goods', 'Bread, pastries, desserts', '🧁'),
('Pantry Items', 'Canned goods, spices, condiments', '🥫'),
('Beverages', 'Drinks, juices, coffee, tea', '☕'),
('Other', 'Miscellaneous food items', '📦');

-- Create indexes for better performance
CREATE INDEX idx_food_posts_user_id ON food_posts(user_id);
CREATE INDEX idx_food_posts_category_id ON food_posts(category_id);
CREATE INDEX idx_food_posts_is_available ON food_posts(is_available);
CREATE INDEX idx_food_posts_created_at ON food_posts(created_at);
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_messages_receiver_id ON messages(receiver_id);
CREATE INDEX idx_reviews_reviewed_user_id ON reviews(reviewed_user_id);
