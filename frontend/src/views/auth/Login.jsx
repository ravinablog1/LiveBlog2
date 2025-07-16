import React, { useState } from "react";
import Header from "../partials/Header";
import Footer from "../partials/Footer";
import { Link, useNavigate } from "react-router-dom";
import { login } from "../../utils/auth";

function Login() {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
        // Clear error when user types
        if (error) {
            setError(null);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        console.log("Login attempt with:", { email: formData.email, password: "***" });

        try {
            const { data, error: loginError } = await login(formData.email, formData.password);
            
            console.log("Login response:", { data, loginError });
            
            if (loginError) {
                setError(loginError);
            } else {
                // Login successful, redirect to dashboard
                console.log("Login successful, redirecting...");
                navigate("/dashboard/");
            }
        } catch (err) {
            console.error("Login catch error:", err);
            setError("Login failed. Please try again.");
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
                                <h2 className="text-center mb-4">Login</h2>
                                
                                {error && (
                                    <div className="alert alert-danger">{error}</div>
                                )}
                                
                                <form onSubmit={handleSubmit}>
                                    <div className="mb-3">
                                        <label className="form-label">Email</label>
                                        <input
                                            type="email"
                                            className="form-control"
                                            name="email"
                                            value={formData.email}
                                            onChange={handleChange}
                                            required
                                            disabled={loading}
                                        />
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Password</label>
                                        <input
                                            type="password"
                                            className="form-control"
                                            name="password"
                                            value={formData.password}
                                            onChange={handleChange}
                                            required
                                            disabled={loading}
                                        />
                                    </div>
                                    <button 
                                        type="submit" 
                                        className="btn btn-primary w-100"
                                        disabled={loading}
                                    >
                                        {loading ? "Logging in..." : "Login"}
                                    </button>
                                </form>
                                <div className="text-center mt-3">
                                    <Link to="/register/">Don't have an account? Register</Link>
                                </div>
                                <div className="text-center mt-2">
                                    <Link to="/forgot-password/">Forgot Password?</Link>
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

export default Login;
