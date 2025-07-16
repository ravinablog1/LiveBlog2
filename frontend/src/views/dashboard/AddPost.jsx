import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function AddPost() {
    const [post, setPost] = useState({
        title: "",
        description: "",
        category: "",
        tags: "",
        status: "Draft",
        image: null
    });
    const [categories, setCategories] = useState([]);
    const [imagePreview, setImagePreview] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    // Fetch real categories from your Django API
    useEffect(() => {
        fetchCategories();
    }, []);

    const fetchCategories = async () => {
        try {
            // Try different possible endpoints
            let response;
            try {
                response = await apiInstance.get('post/category/list/');
            } catch (err) {
                console.log("Trying alternative category endpoint...");
                response = await apiInstance.get('category/list/');
            }
            
            const data = response.data;
            setCategories(data);
        } catch (error) {
            console.error('Error fetching categories:', error);
            // Fallback to mock data
            setCategories([
                { id: 1, title: "Technology" },
                { id: 2, title: "Lifestyle" },
                { id: 3, title: "Business" },
                { id: 4, title: "Health" },
                { id: 5, title: "Education" }
            ]);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setPost(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setPost(prev => ({
                ...prev,
                image: file
            }));
            
            const reader = new FileReader();
            reader.onload = () => {
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        // Validation
        if (!post.title || !post.description || !post.category) {
            alert("Please fill in all required fields");
            setIsLoading(false);
            return;
        }

        // Create FormData for API call
        const formData = new FormData();
        formData.append('title', post.title);
        formData.append('description', post.description);
        formData.append('category', post.category);
        formData.append('tags', post.tags);
        formData.append('status', post.status);
        
        if (post.image) {
            formData.append('image', post.image);
        }

        // Debug: Log what we're sending
        console.log("Form data being sent:");
        for (let [key, value] of formData.entries()) {
            console.log(key, value);
        }

        try {
            const token = localStorage.getItem('access_token');
            
            const response = await fetch('http://127.0.0.1:8000/api/post/author/dashboard/post-create/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                alert("Post created successfully!");
                navigate("/");
            } else {
                // Get detailed error information
                const errorData = await response.json().catch(() => response.text());
                console.error("Error response:", errorData);
                
                if (typeof errorData === 'object') {
                    // Show specific validation errors
                    const errors = Object.entries(errorData).map(([field, messages]) => 
                        `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
                    ).join('\n');
                    alert(`Validation errors:\n${errors}`);
                } else {
                    alert(`Failed to create post. Status: ${response.status}\nError: ${errorData}`);
                }
            }
        } catch (error) {
            console.error("Error creating post:", error);
            alert(`Network error: ${error.message}`);
        }

        setIsLoading(false);
    };

    const testConnection = async () => {
        try {
            console.log("Testing connection to Django backend...");
            const response = await fetch('http://127.0.0.1:8000/api/post/category/list/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                }
            });
          
            if (response.ok) {
                const data = await response.json();
                alert("✅ Connection successful! Backend is working.");
                console.log("Categories:", data);
            } else {
                alert(`❌ Backend responded with status: ${response.status}`);
            }
        } catch (error) {
            console.error("Connection test failed:", error);
            alert("❌ Cannot connect to Django backend. Make sure it's running on http://127.0.0.1:8000");
        }
    };

    return (
        <div style={{ padding: "20px", backgroundColor: "#f8f9fa", minHeight: "100vh" }}>
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-lg-8">
                        <div className="card shadow">
                            <div className="card-header bg-primary text-white">
                                <h2 className="mb-0">Create New Blog Post</h2>
                                <p className="mb-0">Share your thoughts with the world</p>
                            </div>
                            <div className="card-body">
                                <form onSubmit={handleSubmit}>
                                    {/* Image Preview */}
                                    <div className="mb-4">
                                        <label className="form-label">Post Image Preview</label>
                                        <div className="text-center">
                                            <img 
                                                src={imagePreview || "https://via.placeholder.com/600x300?text=Upload+Image"} 
                                                alt="Preview" 
                                                style={{ 
                                                    width: "100%", 
                                                    height: "250px", 
                                                    objectFit: "cover", 
                                                    borderRadius: "8px",
                                                    border: "2px dashed #dee2e6"
                                                }}
                                            />
                                        </div>
                                    </div>

                                    {/* Image Upload */}
                                    <div className="mb-3">
                                        <label htmlFor="image" className="form-label">
                                            Upload Image <span className="text-muted">(Optional)</span>
                                        </label>
                                        <input 
                                            type="file" 
                                            className="form-control" 
                                            id="image"
                                            accept="image/*"
                                            onChange={handleImageChange}
                                        />
                                        <small className="text-muted">Supported formats: JPG, PNG, GIF (Max 5MB)</small>
                                    </div>

                                    {/* Title */}
                                    <div className="mb-3">
                                        <label htmlFor="title" className="form-label">
                                            Post Title <span className="text-danger">*</span>
                                        </label>
                                        <input 
                                            type="text" 
                                            className="form-control" 
                                            id="title"
                                            name="title"
                                            value={post.title}
                                            onChange={handleInputChange}
                                            placeholder="Enter an engaging title for your post"
                                            maxLength="200"
                                            required
                                        />
                                        <small className="text-muted">
                                            {post.title.length}/200 characters (minimum 5 required)
                                        </small>
                                    </div>

                                    {/* Category */}
                                    <div className="mb-3">
                                        <label htmlFor="category" className="form-label">
                                            Category <span className="text-danger">*</span>
                                        </label>
                                        <select 
                                            className="form-select" 
                                            id="category"
                                            name="category"
                                            value={post.category}
                                            onChange={handleInputChange}
                                            required
                                        >
                                            <option value="">Select a category</option>
                                            {categories.map(cat => (
                                                <option key={cat.id} value={cat.id}>
                                                    {cat.title}
                                                </option>
                                            ))}
                                        </select>
                                        <small className="text-muted">Choose the most relevant category</small>
                                    </div>

                                    {/* Description/Content */}
                                    <div className="mb-3">
                                        <label htmlFor="description" className="form-label">
                                            Post Content <span className="text-danger">*</span>
                                        </label>
                                        <textarea 
                                            className="form-control" 
                                            id="description"
                                            name="description"
                                            value={post.description}
                                            onChange={handleInputChange}
                                            rows="10"
                                            placeholder="Write your post content here... Share your thoughts, experiences, or knowledge."
                                            required
                                        ></textarea>
                                        <small className="text-muted">
                                            {post.description.length} characters (minimum 20 required)
                                        </small>
                                    </div>

                                    {/* Tags */}
                                    <div className="mb-3">
                                        <label htmlFor="tags" className="form-label">Tags</label>
                                        <input 
                                            type="text" 
                                            className="form-control" 
                                            id="tags"
                                            name="tags"
                                            value={post.tags}
                                            onChange={handleInputChange}
                                            placeholder="technology, programming, web development"
                                        />
                                        <small className="text-muted">
                                            Separate tags with commas to help readers find your post
                                        </small>
                                    </div>

                                    {/* Status */}
                                    <div className="mb-4">
                                        <label htmlFor="status" className="form-label">Publication Status</label>
                                        <select 
                                            className="form-select" 
                                            id="status"
                                            name="status"
                                            value={post.status}
                                            onChange={handleInputChange}
                                        >
                                            <option value="Draft">Draft (Save for later)</option>
                                            <option value="Active">Publish Now</option>
                                            <option value="Disabled">Disabled</option>
                                        </select>
                                        <small className="text-muted">
                                            Draft: Save without publishing | Active: Publish immediately
                                        </small>
                                    </div>

                                    {/* Test Connection Button */}
                                    <div className="mb-3">
                                        <button 
                                            type="button" 
                                            className="btn btn-outline-info"
                                            onClick={testConnection}
                                        >
                                            🔗 Test Backend Connection
                                        </button>
                                        <small className="text-muted d-block mt-1">
                                            Click to check if Django backend is running
                                        </small>
                                    </div>

                                    {/* Submit Buttons */}
                                    <div className="d-grid gap-2 d-md-flex justify-content-md-end">
                                        <button 
                                            type="button" 
                                            className="btn btn-secondary me-md-2"
                                            onClick={() => navigate("/")}
                                        >
                                            Cancel
                                        </button>
                                        <button 
                                            type="submit" 
                                            className="btn btn-primary"
                                            disabled={isLoading}
                                        >
                                            {isLoading ? (
                                                <>
                                                    <span className="spinner-border spinner-border-sm me-2"></span>
                                                    Creating...
                                                </>
                                            ) : (
                                                <>
                                                    <i className="fas fa-save me-2"></i>
                                                    Create Post
                                                </>
                                            )}
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>

                        {/* Info about where posts appear */}
                        <div className="card mt-4">
                            <div className="card-body">
                                <h5>📍 Where will your post appear?</h5>
                                <ul className="mb-0">
                                    <li><strong>Home Page:</strong> Your post will show in the "Latest Blog Posts" section</li>
                                    <li><strong>Featured Posts:</strong> Active posts may appear in the featured section</li>
                                    <li><strong>Search Page:</strong> Users can find your post through search</li>
                                    <li><strong>Category Pages:</strong> Posts appear under their selected category</li>
                                </ul>
                                <div className="mt-3">
                                    <a href="/" className="btn btn-outline-primary btn-sm me-2">
                                        View Home Page
                                    </a>
                                    <a href="/search/" className="btn btn-outline-secondary btn-sm">
                                        Browse All Posts
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AddPost;
