#!/usr/bin/env python3
import requests
import json

def test_backend():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Backend Endpoints...")
    print("=" * 40)
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Root endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test categories endpoint
    try:
        response = requests.get(f"{base_url}/categories")
        print(f"✅ Categories endpoint: {response.status_code}")
        if response.status_code == 200:
            categories = response.json()
            print(f"   Found {len(categories)} categories")
    except Exception as e:
        print(f"❌ Categories endpoint error: {e}")
    
    # Test food-posts endpoint
    try:
        response = requests.get(f"{base_url}/food-posts")
        print(f"✅ Food-posts endpoint: {response.status_code}")
        if response.status_code == 200:
            posts = response.json()
            print(f"   Found {len(posts)} food posts")
        else:
            print(f"   Error response: {response.text}")
    except Exception as e:
        print(f"❌ Food-posts endpoint error: {e}")
    
    print("=" * 40)

if __name__ == "__main__":
    test_backend()
