import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Header from "../partials/Header";
import Footer from "../partials/Footer";
import apiInstance from "../../utils/axios";

function Register() {
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
        password2: "",
        first_name: "",
        last_name: "",
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [errors, setErrors] = useState({});
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
        
        // Clear field-specific error when user types
        if (errors[e.target.name]) {
            setErrors({
                ...errors,
                [e.target.name]: null,
            });
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setErrors({});

        try {
            const response = await apiInstance.post("/users/register/", formData);
            
            // Store tokens in localStorage
            localStorage.setItem("access_token", response.data.access);
            localStorage.setItem("refresh_token", response.data.refresh);
            localStorage.setItem("user", JSON.stringify(response.data.user));
            
            // Redirect to dashboard
            navigate("/dashboard/");
        } catch (err) {
            console.error("Registration error:", err);
            
            if (err.response?.data && typeof err.response.data === 'object') {
                // Handle field-specific errors
                setErrors(err.response.data);
            } else {
                // Handle general error
                setError(
                    err.response?.data?.error || 
                    "Registration failed. Please check your information and try again."
                );
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <Header />
            <main className="container py-4">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card">
                            <div className="card-body">
                                <h2 className="text-center mb-4">Register</h2>
                                
                                {error && (
                                    <div className="alert alert-danger">{error}</div>
                                )}
                                
                                <form onSubmit={handleSubmit}>
                                    <div className="row">
                                        <div className="col-md-6 mb-3">
                                            <label htmlFor="first_name" className="form-label">First Name</label>
                                            <input
                                                type="text"
                                                className={`form-control ${errors.first_name ? 'is-invalid' : ''}`}
                                                id="first_name"
                                                name="first_name"
                                                value={formData.first_name}
                                                onChange={handleChange}
                                            />
                                            {errors.first_name && (
                                                <div className="invalid-feedback">{errors.first_name}</div>
                                            )}
                                        </div>
                                        
                                        <div className="col-md-6 mb-3">
                                            <label htmlFor="last_name" className="form-label">Last Name</label>
                                            <input
                                                type="text"
                                                className={`form-control ${errors.last_name ? 'is-invalid' : ''}`}
                                                id="last_name"
                                                name="last_name"
                                                value={formData.last_name}
                                                onChange={handleChange}
                                            />
                                            {errors.last_name && (
                                                <div className="invalid-feedback">{errors.last_name}</div>
                                            )}
                                        </div>
                                    </div>
                                    
                                    <div className="mb-3">
                                        <label htmlFor="username" className="form-label">Username</label>
                                        <input
                                            type="text"
                                            className={`form-control ${errors.username ? 'is-invalid' : ''}`}
                                            id="username"
                                            name="username"
                                            value={formData.username}
                                            onChange={handleChange}
                                            required
                                        />
                                        {errors.username && (
                                            <div className="invalid-feedback">{errors.username}</div>
                                        )}
                                    </div>
                                    
                                    <div className="mb-3">
                                        <label htmlFor="email" className="form-label">Email</label>
                                        <input
                                            type="email"
                                            className={`form-control ${errors.email ? 'is-invalid' : ''}`}
                                            id="email"
                                            name="email"
                                            value={formData.email}
                                            onChange={handleChange}
                                            required
                                        />
                                        {errors.email && (
                                            <div className="invalid-feedback">{errors.email}</div>
                                        )}
                                    </div>
                                    
                                    <div className="mb-3">
                                        <label htmlFor="password" className="form-label">Password</label>
                                        <input
                                            type="password"
                                            className={`form-control ${errors.password ? 'is-invalid' : ''}`}
                                            id="password"
                                            name="password"
                                            value={formData.password}
                                            onChange={handleChange}
                                            required
                                        />
                                        {errors.password && (
                                            <div className="invalid-feedback">{errors.password}</div>
                                        )}
                                    </div>
                                    
                                    <div className="mb-3">
                                        <label htmlFor="password2" className="form-label">Confirm Password</label>
                                        <input
                                            type="password"
                                            className={`form-control ${errors.password2 ? 'is-invalid' : ''}`}
                                            id="password2"
                                            name="password2"
                                            value={formData.password2}
                                            onChange={handleChange}
                                            required
                                        />
                                        {errors.password2 && (
                                            <div className="invalid-feedback">{errors.password2}</div>
                                        )}
                                    </div>
                                    <button type="submit" className="btn btn-primary w-100">
                                        Register
                                    </button>
                                </form>
                                <div className="text-center mt-3">
                                    <Link to="/login/">Already have an account? Login</Link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default Register;
