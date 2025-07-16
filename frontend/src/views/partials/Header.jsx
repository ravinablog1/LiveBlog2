import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

function Header() {
    const [searchQuery, setSearchQuery] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const navigate = useNavigate();

    // Check login status on component mount and when localStorage changes
    useEffect(() => {
        const checkLoginStatus = () => {
            const token = localStorage.getItem("access_token");
            setIsLoggedIn(!!token);
        };

        checkLoginStatus();

        // Listen for storage changes (when user logs in/out in another tab)
        window.addEventListener('storage', checkLoginStatus);
        
        // Listen for custom login event
        window.addEventListener('userLoggedIn', checkLoginStatus);
        
        return () => {
            window.removeEventListener('storage', checkLoginStatus);
            window.removeEventListener('userLoggedIn', checkLoginStatus);
        };
    }, []);

    const handleSearch = (e) => {
        e.preventDefault();
        if (searchQuery.trim()) {
            navigate(`/search/?q=${encodeURIComponent(searchQuery)}`);
        }
    };

    const handleLogout = () => {
        // Clear authentication data
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        
        // Update state
        setIsLoggedIn(false);
        
        // Redirect to home page
        navigate("/", { replace: true });
        
        // Reload page to ensure clean state
        window.location.reload();
    };

    return (
        <nav className="navbar">
            <div className="container">
                <div className="d-flex justify-content-between align-items-center w-100">
                    <Link to="/" className="navbar-brand">
                        <h3>Django React Blog</h3>
                    </Link>
                    
                    <div className="search-container" style={{ flex: "1", margin: "0 2rem" }}>
                        <form onSubmit={handleSearch}>
                            <input
                                type="text"
                                className="search-input"
                                placeholder="Search articles..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                            <button type="submit" className="search-button">
                                <i className="fas fa-search">🔍</i>
                            </button>
                        </form>
                    </div>
                    
                    <div className="navbar-nav d-flex flex-row gap-3">
                        <Link to="/" className="nav-link">Home</Link>
                        <Link to="/about/" className="nav-link">About</Link>
                        <Link to="/contact/" className="nav-link">Contact</Link>
                        
                        {isLoggedIn ? (
                            <>
                                <Link to="/dashboard/" className="nav-link">Dashboard</Link>
                                <button 
                                    onClick={handleLogout}
                                    className="btn btn-outline-primary"
                                    style={{ background: 'none', border: '1px solid #007bff' }}
                                >
                                    Logout
                                </button>
                            </>
                        ) : (
                            <>
                                <Link to="/login/" className="btn btn-primary">Login</Link>
                                <Link to="/register/" className="btn btn-outline-primary">Register</Link>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
}

export default Header;
