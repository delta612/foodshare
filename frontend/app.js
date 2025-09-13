// API Configuration
const API_BASE_URL = "http://localhost:8000";

// Global state
let currentUser = null;
let categories = [];
let foodPosts = [];

// DOM Elements
const navAuth = document.getElementById("nav-auth");
const navUser = document.getElementById("nav-user");
const userName = document.getElementById("user-name");

// Initialize the app
document.addEventListener("DOMContentLoaded", function () {
  initializeApp();
  setupEventListeners();
  loadCategories();
  checkAuthStatus();
});

function initializeApp() {
  // Setup navigation
  setupNavigation();

  // Setup forms
  setupForms();

  // Load initial data
  loadFoodPosts();
}

function setupEventListeners() {
  // File upload preview
  const fileInput = document.getElementById("food-images");
  if (fileInput) {
    fileInput.addEventListener("change", handleFilePreview);
  }

  // Search functionality
  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    searchInput.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        searchFood();
      }
    });
  }
}

function setupNavigation() {
  const navToggle = document.getElementById("nav-toggle");
  const navMenu = document.getElementById("nav-menu");
  const navLinks = document.querySelectorAll(".nav-link");

  // Mobile menu toggle
  if (navToggle) {
    navToggle.addEventListener("click", function () {
      navMenu.classList.toggle("active");
    });
  }

  // Navigation links
  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const sectionId = this.getAttribute("href").substring(1);
      showSection(sectionId);

      // Update active link
      navLinks.forEach((l) => l.classList.remove("active"));
      this.classList.add("active");

      // Close mobile menu
      navMenu.classList.remove("active");
    });
  });
}

function setupForms() {
  // Login form
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
  }

  // Register form
  const registerForm = document.getElementById("register-form");
  if (registerForm) {
    registerForm.addEventListener("submit", handleRegister);
  }

  // Share form
  const shareForm = document.getElementById("share-form");
  if (shareForm) {
    shareForm.addEventListener("submit", handleShareFood);
  }
}

// Authentication functions
async function checkAuthStatus() {
  const token = localStorage.getItem("token");
  if (token) {
    try {
      const response = await fetch(`${API_BASE_URL}/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        currentUser = await response.json();
        updateAuthUI();
      } else {
        localStorage.removeItem("token");
      }
    } catch (error) {
      console.error("Auth check failed:", error);
      localStorage.removeItem("token");
    }
  }
}

function updateAuthUI() {
  if (currentUser) {
    navAuth.style.display = "none";
    navUser.style.display = "flex";
    userName.textContent = currentUser.username;
  } else {
    navAuth.style.display = "flex";
    navUser.style.display = "none";
  }
}

async function handleLogin(e) {
  e.preventDefault();

  const formData = new FormData(e.target);
  const loginData = {
    username: formData.get("username"),
    password: formData.get("password"),
  };

  try {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(loginData),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("token", data.access_token);
      await checkAuthStatus();
      closeModal("login-modal");
      showToast("Login successful!", "success");
      e.target.reset();
    } else {
      const error = await response.json();
      showToast(error.detail || "Login failed", "error");
    }
  } catch (error) {
    showToast("Login failed. Please try again.", "error");
  }
}

async function handleRegister(e) {
  e.preventDefault();

  const formData = new FormData(e.target);
  const registerData = {
    username: formData.get("username"),
    email: formData.get("email"),
    password: formData.get("password"),
    full_name: formData.get("full_name"),
    city: formData.get("city"),
    bio: formData.get("bio"),
  };

  try {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(registerData),
    });

    if (response.ok) {
      closeModal("register-modal");
      showToast("Account created successfully! Please login.", "success");
      e.target.reset();
      setTimeout(() => showLogin(), 1000);
    } else {
      const error = await response.json();
      showToast(error.detail || "Registration failed", "error");
    }
  } catch (error) {
    showToast("Registration failed. Please try again.", "error");
  }
}

function logout() {
  localStorage.removeItem("token");
  currentUser = null;
  updateAuthUI();
  showToast("Logged out successfully", "success");
  showSection("home");
}

// Category functions
async function loadCategories() {
  try {
    const response = await fetch(`${API_BASE_URL}/categories`);
    if (response.ok) {
      categories = await response.json();
      populateCategorySelects();
    }
  } catch (error) {
    console.error("Failed to load categories:", error);
  }
}

function populateCategorySelects() {
  const categoryFilter = document.getElementById("category-filter");
  const foodCategory = document.getElementById("food-category");

  categories.forEach((category) => {
    const option1 = new Option(category.name, category.id);
    const option2 = new Option(category.name, category.id);

    if (categoryFilter) categoryFilter.appendChild(option1);
    if (foodCategory) foodCategory.appendChild(option2);
  });
}

// Food post functions
async function loadFoodPosts() {
  const loading = document.getElementById("loading");
  const foodGrid = document.getElementById("food-grid");

  if (loading) loading.style.display = "block";

  try {
    const response = await fetch(`${API_BASE_URL}/food-posts`);
    if (response.ok) {
      foodPosts = await response.json();
      displayFoodPosts(foodPosts);
    }
  } catch (error) {
    console.error("Failed to load food posts:", error);
    showToast("Failed to load food posts", "error");
  } finally {
    if (loading) loading.style.display = "none";
  }
}

function displayFoodPosts(posts) {
  const foodGrid = document.getElementById("food-grid");
  if (!foodGrid) return;

  if (posts.length === 0) {
    foodGrid.innerHTML = `
            <div class="no-food">
                <i class="fas fa-utensils"></i>
                <p>No food posts available at the moment.</p>
            </div>
        `;
    return;
  }

  foodGrid.innerHTML = posts
    .map(
      (post) => `
        <div class="food-card" onclick="showFoodDetail(${post.id})">
            <img src="${
              post.primary_image
                ? `${API_BASE_URL}/${post.primary_image.image_path}`
                : "/placeholder-food.jpg"
            }" 
                 alt="${post.title}" class="food-card-image">
            <div class="food-card-content">
                <h3 class="food-card-title">${post.title}</h3>
                <p class="food-card-description">${post.description}</p>
                <div class="food-card-meta">
                    <div class="food-card-location">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>${post.pickup_location}</span>
                    </div>
                    <div class="food-card-time">
                        <i class="fas fa-clock"></i>
                        <span>${formatDate(post.created_at)}</span>
                    </div>
                </div>
            </div>
        </div>
    `
    )
    .join("");
}

async function showFoodDetail(postId) {
  try {
    const response = await fetch(`${API_BASE_URL}/food-posts/${postId}`);
    if (response.ok) {
      const post = await response.json();
      displayFoodDetailModal(post);
    }
  } catch (error) {
    showToast("Failed to load food details", "error");
  }
}

function displayFoodDetailModal(post) {
  const modal = document.getElementById("food-detail-modal");
  const title = document.getElementById("food-detail-title");
  const content = document.getElementById("food-detail-content");

  title.textContent = post.title;

  const primaryImage =
    post.images.find((img) => img.is_primary) || post.images[0];

  content.innerHTML = `
        ${
          primaryImage
            ? `<img src="${API_BASE_URL}/${primaryImage.image_path}" alt="${post.title}" class="food-detail-image">`
            : ""
        }
        
        <div class="food-detail-info">
            <div>
                <i class="fas fa-tag"></i>
                <span>${
                  post.category ? post.category.name : "No category"
                }</span>
            </div>
            <div>
                <i class="fas fa-weight"></i>
                <span>${post.quantity || "Not specified"}</span>
            </div>
            <div>
                <i class="fas fa-calendar"></i>
                <span>${
                  post.expiry_date
                    ? formatDate(post.expiry_date)
                    : "No expiry date"
                }</span>
            </div>
            <div>
                <i class="fas fa-map-marker-alt"></i>
                <span>${post.pickup_location}</span>
            </div>
        </div>
        
        <div class="food-detail-description">
            <h4>Description</h4>
            <p>${post.description}</p>
        </div>
        
        <div class="food-detail-user">
            <div class="user-avatar">
                ${post.user.username.charAt(0).toUpperCase()}
            </div>
            <div>
                <h4>${post.user.username}</h4>
                <p>${post.user.city || "Location not specified"}</p>
            </div>
        </div>
        
        ${
          currentUser && currentUser.id !== post.user_id
            ? `
            <button class="btn btn-primary btn-large" onclick="claimFood(${post.id})">
                <i class="fas fa-hand-holding-heart"></i> Claim This Food
            </button>
        `
            : ""
        }
    `;

  showModal("food-detail-modal");
}

async function claimFood(postId) {
  if (!currentUser) {
    showLogin();
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/food-posts/${postId}/claim`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (response.ok) {
      showToast("Food claimed successfully!", "success");
      closeModal("food-detail-modal");
      loadFoodPosts(); // Refresh the list
    } else {
      const error = await response.json();
      showToast(error.detail || "Failed to claim food", "error");
    }
  } catch (error) {
    showToast("Failed to claim food", "error");
  }
}

// Share food functions
async function handleShareFood(e) {
  e.preventDefault();

  if (!currentUser) {
    showToast("Please login to share food", "error");
    showLogin();
    return;
  }

  const formData = new FormData(e.target);
  const images = formData.getAll("images");

  if (images.length === 0) {
    showToast("Please select at least one image", "error");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/food-posts`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: formData,
    });

    if (response.ok) {
      showToast("Food shared successfully!", "success");
      e.target.reset();
      clearImagePreview();
      loadFoodPosts(); // Refresh the list
    } else {
      const error = await response.json();
      showToast(error.detail || "Failed to share food", "error");
    }
  } catch (error) {
    showToast("Failed to share food", "error");
  }
}

function handleFilePreview(e) {
  const files = Array.from(e.target.files);
  const preview = document.getElementById("image-preview");

  preview.innerHTML = "";

  files.forEach((file) => {
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const img = document.createElement("img");
        img.src = e.target.result;
        img.className = "preview-image";
        preview.appendChild(img);
      };
      reader.readAsDataURL(file);
    }
  });
}

function clearImagePreview() {
  const preview = document.getElementById("image-preview");
  if (preview) {
    preview.innerHTML = "";
  }
}

// Search functions
function searchFood() {
  const searchInput = document.getElementById("search-input");
  const categoryFilter = document.getElementById("category-filter");
  const locationFilter = document.getElementById("location-filter");

  const query = searchInput ? searchInput.value : "";
  const categoryId = categoryFilter ? categoryFilter.value : "";
  const location = locationFilter ? locationFilter.value : "";

  // Filter posts based on search criteria
  let filteredPosts = foodPosts;

  if (query) {
    filteredPosts = filteredPosts.filter(
      (post) =>
        post.title.toLowerCase().includes(query.toLowerCase()) ||
        post.description.toLowerCase().includes(query.toLowerCase())
    );
  }

  if (categoryId) {
    filteredPosts = filteredPosts.filter(
      (post) => post.category && post.category.id == categoryId
    );
  }

  if (location) {
    filteredPosts = filteredPosts.filter(
      (post) =>
        post.user.city &&
        post.user.city.toLowerCase().includes(location.toLowerCase())
    );
  }

  displayFoodPosts(filteredPosts);
}

// Utility functions
function showSection(sectionId) {
  // Hide all sections
  document.querySelectorAll(".section").forEach((section) => {
    section.classList.remove("active");
  });

  // Show target section
  const targetSection = document.getElementById(sectionId);
  if (targetSection) {
    targetSection.classList.add("active");
  }

  // Load data for specific sections
  if (sectionId === "browse") {
    loadFoodPosts();
  }
}

function showModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "block";
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "none";
  }
}

function showLogin() {
  closeModal("register-modal");
  showModal("login-modal");
}

function showRegister() {
  closeModal("login-modal");
  showModal("register-modal");
}

function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;

  container.appendChild(toast);

  // Auto remove after 3 seconds
  setTimeout(() => {
    if (toast.parentNode) {
      toast.parentNode.removeChild(toast);
    }
  }, 3000);
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

// Close modals when clicking outside
window.addEventListener("click", function (e) {
  if (e.target.classList.contains("modal")) {
    e.target.style.display = "none";
  }
});
