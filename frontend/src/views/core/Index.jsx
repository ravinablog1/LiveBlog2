
import { useState, useEffect } from "react";
import Header from "../partials/Header";
import Footer from "../partials/Footer";
import { Link } from "react-router-dom";
import apiInstance from "../../utils/axios";

function Index() {
    const [posts, setPosts] = useState([]);
    const [featuredPosts, setFeaturedPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [stats, setStats] = useState({
        totalPosts: 0,
        totalAuthors: 0,
        totalComments: 0
    });

    // Check if user is logged in
    const isLoggedIn = localStorage.getItem("access_token");

    const fetchPosts = async () => {
        try {
            setLoading(true);
            console.log("Fetching posts...");
            
            // First check if the API is reachable
            try {
                const healthCheck = await apiInstance.get('health-check/');
                console.log("API health check:", healthCheck.data);
            } catch (healthErr) {
                console.error("API health check failed:", healthErr);
                setError('Cannot connect to the API server. Please check your connection.');
                setLoading(false);
                return;
            }
            
            // Try the test endpoint first
            try {
                const testResponse = await apiInstance.get('post/test/');
                console.log("Test API Response:", testResponse.data);
            } catch (testErr) {
                console.error("Test API failed:", testErr);
            }
            
            // Then try the regular endpoint
            const response = await apiInstance.get('post/list/');
            console.log("API Response:", response);
            
            const allPosts = response.data.results || response.data || [];
            console.log("Posts data:", allPosts);
            
            if (allPosts.length === 0) {
                console.log("No posts found");
                // Still set empty posts but don't show error
            }
            
            setPosts(allPosts.slice(0, 6));
            setFeaturedPosts(allPosts.length > 0 ? allPosts.slice(0, 3) : []);
            
            setStats({
                totalPosts: allPosts.length,
                totalAuthors: [...new Set(allPosts.map(p => p.user?.username || p.user?.id || "Unknown"))].length,
                totalComments: allPosts.reduce((sum, post) => sum + (post.comments?.length || 0), 0)
            });
            
            setError(null);
        } catch (err) {
            console.error('Error fetching posts:', err);
            console.error('Error details:', err.response?.data || err.message);
            setError('Failed to load posts. Please try again later.');
            setPosts([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchPosts();
    }, []);

    return (
        <div>
            <Header />
            
            {/* Hero Section */}
            <section className="hero-section bg-primary text-white py-5">
                <div className="container">
                    <div className="row align-items-center">
                        <div className="col-lg-6">
                            <h1 className="display-4 fw-bold mb-4">
                                Welcome to Django React Blog
                            </h1>
                            <p className="lead mb-4">
                                A modern blogging platform where you can share your thoughts, 
                                discover amazing articles, and connect with a vibrant community of writers and readers.
                            </p>
                            <div className="d-flex gap-3">
                                {isLoggedIn ? (
                                    <>
                                        <Link to="/add-post/" className="btn btn-light btn-lg">
                                            <i className="fas fa-plus me-2"></i>
                                            Create Post
                                        </Link>
                                        <Link to="/dashboard/" className="btn btn-outline-light btn-lg">
                                            <i className="fas fa-tachometer-alt me-2"></i>
                                            Dashboard
                                        </Link>
                                    </>
                                ) : (
                                    <>
                                        <Link to="/register/" className="btn btn-light btn-lg">
                                            <i className="fas fa-user-plus me-2"></i>
                                            Get Started
                                        </Link>
                                        <Link to="/login/" className="btn btn-outline-light btn-lg">
                                            <i className="fas fa-sign-in-alt me-2"></i>
                                            Login
                                        </Link>
                                    </>
                                )}
                            </div>
                        </div>
                        <div className="col-lg-6">
                            <div className="text-center">
                                <img 
                                    src="https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=500&h=300&fit=crop" 
                                    alt="Blogging" 
                                    className="img-fluid rounded shadow"
                                    style={{ maxHeight: '400px' }}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Quick Actions Bar for Logged In Users */}
            {isLoggedIn && (
                <section className="py-3 bg-light border-bottom">
                    <div className="container">
                        <div className="d-flex justify-content-center gap-3">
                            <Link to="/add-post/" className="btn btn-primary">
                                <i className="fas fa-plus me-2"></i>
                                Write New Post
                            </Link>
                            <Link to="/posts/" className="btn btn-outline-primary">
                                <i className="fas fa-list me-2"></i>
                                My Posts
                            </Link>
                            <Link to="/dashboard/" className="btn btn-outline-secondary">
                                <i className="fas fa-chart-bar me-2"></i>
                                Analytics
                            </Link>
                        </div>
                    </div>
                </section>
            )}

            {/* Stats Section */}
            <section className="py-4 bg-light">
                <div className="container">
                    <div className="row text-center">
                        <div className="col-md-4">
                            <div className="stat-item">
                                <h3 className="display-6 fw-bold text-primary">{stats.totalPosts}</h3>
                                <p className="text-muted">Blog Posts</p>
                            </div>
                        </div>
                        <div className="col-md-4">
                            <div className="stat-item">
                                <h3 className="display-6 fw-bold text-primary">{stats.totalAuthors}</h3>
                                <p className="text-muted">Active Writers</p>
                            </div>
                        </div>
                        <div className="col-md-4">
                            <div className="stat-item">
                                <h3 className="display-6 fw-bold text-primary">{stats.totalComments}</h3>
                                <p className="text-muted">Comments</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <main className="container py-5">
                {/* Featured Posts Section */}
                {featuredPosts.length > 0 && (
                    <section className="mb-5">
                        <div className="d-flex justify-content-between align-items-center mb-4">
                            <h2 className="h3 fw-bold">Featured Stories</h2>
                            <div className="d-flex gap-2">
                                {isLoggedIn && (
                                    <Link to="/add-post/" className="btn btn-success btn-sm">
                                        <i className="fas fa-plus me-1"></i>
                                        Add New
                                    </Link>
                                )}
                                <Link to="/search/" className="btn btn-outline-primary btn-sm">
                                    View All Posts
                                </Link>
                            </div>
                        </div>
                        
                        <div className="row">
                            {featuredPosts.map((post, index) => (
                                <div key={post.id} className={`col-md-${index === 0 ? '8' : '4'} mb-4`}>
                                    <div className="card h-100 border-0 shadow-sm">
                                        {post.image && (
                                            <img 
                                                src={post.image} 
                                                className="card-img-top" 
                                                alt={post.title}
                                                style={{ 
                                                    height: index === 0 ? '300px' : '200px', 
                                                    objectFit: 'cover' 
                                                }}
                                            />
                                        )}
                                        <div className="card-body">
                                            <div className="d-flex justify-content-between align-items-start mb-2">
                                                <span className="badge bg-primary">Featured</span>
                                                <small className="text-muted">
                                                    {new Date(post.date || post.timestamp).toLocaleDateString()}
                                                </small>
                                            </div>
                                            <h5 className="card-title fw-bold">
                                                {post.title}
                                            </h5>
                                            <p className="card-text text-muted">
                                                {post.content?.substring(0, index === 0 ? 150 : 100) || 
                                                 post.description?.substring(0, index === 0 ? 150 : 100)}...
                                            </p>
                                            <div className="d-flex justify-content-between align-items-center">
                                                <small className="text-muted">
                                                    <i className="fas fa-user me-1"></i>
                                                    {post.user?.username || post.author}
                                                </small>
                                                <Link 
                                                    to={`/${post.slug}/`} 
                                                    className="btn btn-primary btn-sm"
                                                >
                                                    Read More
                                                </Link>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>
                )}

                {/* Latest Posts Section */}
                <section>
                    <div className="d-flex justify-content-between align-items-center mb-4">
                        <h2 className="h3 fw-bold">Latest Blog Posts</h2>
                        <div className="d-flex gap-2">
                            {isLoggedIn && (
                                <Link to="/add-post/" className="btn btn-success">
                                    <i className="fas fa-plus me-2"></i>
                                    Write Article
                                </Link>
                            )}
                            <Link to="/search/" className="text-decoration-none">
                                View All <i className="fas fa-arrow-right ms-1"></i>
                            </Link>
                        </div>
                    </div>
                    
                    {loading && (
                        <div className="text-center py-5">
                            <div className="spinner-border text-primary" role="status">
                                <span className="visually-hidden">Loading...</span>
                            </div>
                            <p className="mt-3 text-muted">Loading posts...</p>
                        </div>
                    )}
                    
                    {error && (
                        <div className="alert alert-danger text-center">
                            <i className="fas fa-exclamation-triangle me-2"></i>
                            {error}
                        </div>
                    )}
                    
                    {!loading && !error && posts.length === 0 && (
                        <div className="text-center py-5">
                            <div className="card border-0">
                                <div className="card-body">
                                    <i className="fas fa-edit fa-3x text-muted mb-3"></i>
                                    <h5 className="card-title">No posts available yet</h5>
                                    <p className="card-text text-muted">
                                        Be the first to create a post and start sharing your thoughts with the community!
                                    </p>
                                    {isLoggedIn ? (
                                        <Link to="/add-post/" className="btn btn-primary">
                                            <i className="fas fa-plus me-2"></i>
                                            Create First Post
                                        </Link>
                                    ) : (
                                        <Link to="/register/" className="btn btn-primary">
                                            <i className="fas fa-user-plus me-2"></i>
                                            Join Now
                                        </Link>
                                    )}
                                </div>
                            </div>
                        </div>
                    )}
                    
                    <div className="row">
                        {posts.map((post) => (
                            <div key={post.id} className="col-md-6 col-lg-4 mb-4">
                                <div className="card h-100 border-0 shadow-sm hover-shadow">
                                    {post.image && (
                                        <img 
                                            src={post.image} 
                                            className="card-img-top" 
                                            alt={post.title}
                                            style={{ height: '200px', objectFit: 'cover' }}
                                        />
                                    )}
                                    <div className="card-body d-flex flex-column">
                                        <div className="mb-2">
                                            <span className="badge bg-light text-dark">
                                                {post.category || 'General'}
                                            </span>
                                        </div>
                                        <h5 className="card-title fw-bold">
                                            {post.title}
                                        </h5>
                                        <p className="card-text flex-grow-1 text-muted">
                                            {post.content?.substring(0, 100) || post.description?.substring(0, 100)}...
                                        </p>
                                        <div className="mt-auto">
                                            <div className="d-flex justify-content-between align-items-center mb-3">
                                                <small className="text-muted">
                                                    <i className="fas fa-user me-1"></i>
                                                    {post.user?.username || post.author}
                                                </small>
                                                <small className="text-muted">
                                                    <i className="fas fa-calendar me-1"></i>
                                                    {new Date(post.date || post.timestamp).toLocaleDateString()}
                                                </small>
                                            </div>
                                            <Link 
                                                to={`/${post.slug}/`} 
                                                className="btn btn-outline-primary w-100"
                                            >
                                                <i className="fas fa-book-open me-2"></i>
                                                Read More
                                            </Link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Call to Action Section */}
                <section className="bg-light rounded p-5 mt-5 text-center">
                    <h3 className="fw-bold mb-3">Ready to Share Your Story?</h3>
                    <p className="text-muted mb-4">
                        Join our community of writers and start publishing your own blog posts today.
                    </p>
                    <div className="d-flex justify-content-center gap-3">
                        {isLoggedIn ? (
                            <>
                                <Link to="/add-post/" className="btn btn-primary btn-lg">
                                    <i className="fas fa-pen me-2"></i>
                                    Start Writing
                                </Link>
                                <Link to="/dashboard/" className="btn btn-outline-primary btn-lg">
                                    <i className="fas fa-tachometer-alt me-2"></i>
                                    Go to Dashboard
                                </Link>
                            </>
                        ) : (
                            <>
                                <Link to="/register/" className="btn btn-primary btn-lg">
                                    <i className="fas fa-pen me-2"></i>
                                    Start Writing
                                </Link>
                                <Link to="/login/" className="btn btn-outline-primary btn-lg">
                                    <i className="fas fa-sign-in-alt me-2"></i>
                                    Login
                                </Link>
                            </>
                        )}
                    </div>
                </section>
            </main>
            
            <Footer />
        </div>
    );
}

export default Index;
